"""
This script verifies the HEPData extraction for Figure 1 by comparing the original ROOT graphs with the graphs created from HEPData histograms. 
It processes each particle type (D0, Dplus, Ds, LambdaC) and saves the comparison results in a new ROOT file for further analysis and visualization.
"""
import ROOT
import sys
from ROOT import TFile, TGraphAsymmErrors, TCanvas, TLegend
sys.path.append('../code')
from plot_untils import (
    SetObjectStyle, SetGlobalStyle
)
SetGlobalStyle(padleftmargin=0.15, padrightmargin=0.08, padbottommargin=0.16, padtopmargin=0.075,
               titleoffset=1.3, palette=ROOT.kRainBow, titlesize=0.06, labelsize=0.055, maxdigits=4)


def reset_graph_x_to_bin_center(graph):
    """
    Reset TGraphAsymmErrors X values to bin center (ignore shift) and set symmetric X errors
    Args:
        graph (TGraphAsymmErrors): Input graph to modify
    Returns:
        TGraphAsymmErrors: Modified graph (for compatibility with your call logic)
    """
    n_points = graph.GetN()
    for i in range(n_points):
        # Get original X errors (left/right) and calculate bin boundaries
        x_err_low = graph.GetErrorXlow(i)
        x_err_high = graph.GetErrorXhigh(i)
        bin_left = graph.GetX()[i] - x_err_low  # Original bin left boundary
        bin_right = graph.GetX()[i] + x_err_high # Original bin right boundary
        
        # Reset X to bin center (ignore shift)
        bin_center = (bin_left + bin_right) / 2.0
        graph.SetPointX(i, bin_center)
        
        # Set symmetric X errors (TGraphAsymmErrors requires separate low/high)
        sym_x_err = (bin_right - bin_left) / 2.0
        # Get current Y errors to preserve them
        y_err_low = graph.GetErrorYlow(i)
        y_err_high = graph.GetErrorYhigh(i)
        # Update point error (X low/high = sym_x_err, Y keep original)
        graph.SetPointError(i, sym_x_err, sym_x_err, y_err_low, y_err_high)
    
    return graph  # Return graph to match your call logic

def set_graph_x_to_weighted_bin_center(graph, target_graph):
    """
    Reset TGraphAsymmErrors X values to weighted bin center (consider pT shift) 
    by getting asymmetric X errors from target_graph, set asymmetric X errors
    Args:
        graph (TGraphAsymmErrors): Input graph to modify
        target_graph (TGraphAsymmErrors): Graph to get shifted X & asymmetric X errors
    Returns:
        TGraphAsymmErrors: Modified graph with pT shift considered
    """
    n_points = graph.GetN()
    # Ensure point number matches between two graphs
    if target_graph.GetN() != n_points:
        raise ValueError("Graph and target_graph have different point counts!")
    
    for i in range(n_points):
        # Get shifted X and asymmetric X errors from target_graph (consider pT shift)
        shifted_x = target_graph.GetX()[i]
        x_err_low = target_graph.GetErrorXlow(i)
        x_err_high = target_graph.GetErrorXhigh(i)
        graph.SetPointX(i, shifted_x)
        y_err_low = graph.GetErrorYlow(i)
        y_err_high = graph.GetErrorYhigh(i)
        graph.SetPointError(i, x_err_low, x_err_high, y_err_low, y_err_high)
    
    return graph

def create_graph_with_errors(central_hist, error_hist):
    """
    Create TGraphAsymmErrors from central value and error histograms
    Args:
        central_hist (TH1F): Histogram with central values
        error_hist (TH1F): Histogram with error values (stat/syst)
    Returns:
        TGraphAsymmErrors: Graph with x/y values and asymmetric errors
    """
    # Initialize graph with same bin count as input histograms
    error_name = error_hist.GetName() if not isinstance(error_hist, list) else error_hist[0].GetName()
    graph = TGraphAsymmErrors(central_hist.GetNbinsX())
    graph.SetName(f"{central_hist.GetName()}_with_{error_name.split('_')[-1]}")
    graph.SetTitle(f"{central_hist.GetTitle()};p_{{T}} (GeV/c);v_{2}")

    # Fill graph points and errors (ROOT bins start from 1)
    for i in range(central_hist.GetNbinsX()):
        bin_idx = i + 1
        x = central_hist.GetBinCenter(bin_idx)
        x_err = central_hist.GetBinWidth(bin_idx) / 2.0  # X error: half bin width
        y = central_hist.GetBinContent(bin_idx)
        if isinstance(error_hist, list):
            y_err_plus = error_hist[0].GetBinContent(bin_idx)  # Syst error plus
            y_err_minus = error_hist[1].GetBinContent(bin_idx)  # Syst error minus
            y_err_minus = abs(y_err_minus)  # Ensure error is positive for graph
        else:
            y_err_plus = error_hist.GetBinContent(bin_idx)       # Y error from error hist
            y_err_minus = error_hist.GetBinContent(bin_idx)      # Assuming symmetric errors if not separate
        graph.SetPoint(i, x, y)
        graph.SetPointError(i, x_err, x_err, y_err_minus, y_err_plus)  # Asymmetric errors

    return graph

def get_graphs_compare(origin_file, hep_dir, no_ptshift=False):
    """
    Compare original graphs with HEPData-derived graphs
    Args:
        origin_file (TFile): Original input ROOT file
        hep_dir (TDirectoryFile): HEPData directory with histograms
    Returns:
        tuple: (stat_graph, syst_graph, canvas)
    """
    # Get original stat/syst graphs
    origin_graph_stat = origin_file.Get("gvn_prompt_stat")
    origin_graph_syst = origin_file.Get("tot_syst")

    # Get HEPData histograms (central/stat/syst)
    hist_central = hep_dir.Get("Hist1D_y1")
    hist_stat_err = hep_dir.Get("Hist1D_y1_e1")
    hist_syst_err = hep_dir.Get("Hist1D_y1_e2")
    graph_tot_err = hep_dir.Get("Graph1D_y1")
    if not hist_syst_err:
        print(str(hep_dir.GetName()) + ": No single syst error histogram found, checking for separate plus/minus histograms...")
        hist_syst_err_plus = hep_dir.Get("Hist1D_y1_e2plus")
        hist_syst_err_minus = hep_dir.Get("Hist1D_y1_e2minus")
        hist_syst_err = [hist_syst_err_plus, hist_syst_err_minus]  # Handle separate syst error histograms

    # Create HEPData graphs with errors
    graph_stat = create_graph_with_errors(hist_central, hist_stat_err)
    graph_syst = create_graph_with_errors(hist_central, hist_syst_err)
    
    if no_ptshift:
        origin_graph_stat = reset_graph_x_to_bin_center(origin_graph_stat)
        origin_graph_syst = reset_graph_x_to_bin_center(origin_graph_syst)
    else:
        graph_stat = set_graph_x_to_weighted_bin_center(graph_stat, graph_tot_err) 
        graph_syst = set_graph_x_to_weighted_bin_center(graph_syst, graph_tot_err)
    SetObjectStyle(graph_stat, color=ROOT.kRed, linewidth=2)
    SetObjectStyle(graph_syst, color=ROOT.kRed, linewidth=2, fillstyle=0)
    SetObjectStyle(origin_graph_stat, color=ROOT.kBlack, linewidth=2)
    SetObjectStyle(origin_graph_syst, color=ROOT.kBlack, linewidth=2, fillstyle=0)
    # Create canvas and plot
    canvas = TCanvas("canvas", f"{hep_dir.GetName()} v2 comparison", 1200, 600)
    canvas.Divide(2, 1, 0, 0)  # Divide canvas into 2 pads for stat and syst comparison
    pad1 = canvas.cd(1)
    frame = pad1.DrawFrame(0.455, -0.01, 27.7, 0.43,
                            ';#it{p}_{T} (GeV/#it{c});#it{v}_{2}')
    # Draw graphs (pe=point+error, e2=error band)
    graph_stat.Draw("pez SAME")
    origin_graph_stat.Draw("pez SAME")
    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.DrawLatex(0.4, 0.9, "Statistical Uncertainty")
    pad2 = canvas.cd(2)
    frame = pad2.DrawFrame(0.455, -0.01, 27.7, 0.43,
                            ';#it{p}_{T} (GeV/#it{c});#it{v}_{2}')
    latex.DrawLatex(0.3, 0.9, "Systematic Uncertainty")
    graph_syst.Draw("pez SAME")
    origin_graph_syst.Draw("pez SAME")

    # Add legend
    legend = TLegend(0.6, 0.7, 0.85, 0.85)
    legend.AddEntry(graph_stat, "HEPData", "ep")
    legend.AddEntry(origin_graph_stat, "Original", "ep")
    legend.Draw('SAME')
    canvas.Update()
    canvas.Modified()
    collect = [graph_stat, graph_syst, canvas, legend, latex]  # Collect objects to prevent garbage collection
    canvas.SaveAs(f"{hep_dir.GetName()}_comparison.pdf")  # Save canvas as image for quick check

    return graph_stat, graph_syst, canvas

def process_fig1(no_ptshift=False):
    """Process Figure 1 data: compare original vs HEPData and save results"""
    print('\n### Processing HEPData for Fig 1 ###')
    
    # Input file paths
    input_path = "../input-data/lc-d0-data/"
    origin_files_info = [
        ("v2_prompt_wsyst_D0_3050_finer_updated_x.root", "Dzero"),
        ("v2_prompt_wsyst_Dplus_3050_updated_x.root", "Dplus"),
        ("v2_prompt_wsyst_Ds_3050_updated_x.root", "Ds"),
        ("v2_prompt_wsyst_Lc_3050_updated_x.root", "LambdaC")
    ]

    # Open HEPData file (with context-like memory management)
    hep_file = TFile.Open('HEPData-1773329189-v1-root.root', "READ")
    if not hep_file or hep_file.IsZombie():
        print("Error: Failed to open HEPData file!")
        return

    # Open output file
    output_file = TFile.Open('verify_hep_data_fig1.root', "RECREATE")
    if not output_file or output_file.IsZombie():
        print("Error: Failed to create output file!")
        hep_file.Close()
        return

    # Process each particle type
    for file_name, particle in origin_files_info:
        # Open original file (per iteration, close after use)
        origin_file = TFile.Open(input_path + file_name, "READ")
        if not origin_file or origin_file.IsZombie():
            print(f"Warning: Failed to open original file {file_name}, skip!")
            continue
        
        # Get HEPData directory
        hep_dir = hep_file.Get(f"Figure 1 {particle} 30-50% PbPb 5.36 TeV")
        if not hep_dir:
            print(f"Warning: HEPData dir for {particle} not found, skip!")
            origin_file.Close()
            continue

        # Generate comparison graphs/canvas
        graph_stat, graph_syst, canvas = get_graphs_compare(origin_file, hep_dir, no_ptshift)
        output_file.cd()  # Ensure we're in the output file context for writing
        # Save to output file
        canvas_name = f"{hep_dir.GetName()}_canvas"
        stat_name = f"{hep_dir.GetName()}_stat"
        syst_name = f"{hep_dir.GetName()}_syst"
        
        canvas.Write(canvas_name)
        graph_stat.Write(stat_name)
        graph_syst.Write(syst_name)

        # Clean up per-iteration objects (memory management)
        origin_file.Close()
        del graph_stat, graph_syst, canvas  # Explicit delete to free memory

    # Final clean up
    output_file.Close()
    hep_file.Close()
    print("### Fig 1 processing completed. Output saved to verify_hep_data_fig1.root ###")

if __name__ == "__main__":
    # Disable ROOT batch mode to show plots (comment if running in batch)
    # ROOT.gROOT.SetBatch(True)
    no_ptshift = False  # Set to True to ignore pT shift and use bin center, False to consider pT shift (weighted bin center)
    process_fig1(no_ptshift)