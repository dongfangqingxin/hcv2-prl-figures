from hepdata_lib import Submission, Table, RootFileReader, Variable, Uncertainty


def fig1():

    print('\n### HeP data for Fig 1')
    path = "../input-data/lc-d0-data/"
    readerFig1_Dzero = RootFileReader(path + "v2_prompt_wsyst_D0_3050_finer_updated_x.root")
    readerFig1_Dplus = RootFileReader(path + "v2_prompt_wsyst_Dplus_3050_updated_x.root")
    readerFig1_Ds = RootFileReader(path + "v2_prompt_wsyst_Ds_3050_updated_x.root")
    readerFig1_Lc = RootFileReader(path + "v2_prompt_wsyst_Lc_3050_updated_x.root")
    statName = "gvn_prompt_stat"
    systName = "tot_syst"
    round_digits = 5

    ########################
    ### D0 PbPb 5.36 TeV ###
    ########################

    tableFig1_Dzero = Table("Figure 1 Dzero PbPb 5.36 TeV")
    description_Dzero = "$p_{\mathrm{T}}$-differential prompt $\mathrm{D}^{0}$ ${v}_{2}$\{SP\} at midrapidity ($|y|<0.8$) in PbPb collisions at $\sqrt{s_{NN}}$ = 5.36 TeV"
    tableFig1_Dzero.description = description_Dzero
    tableFig1_Dzero.location = "Data from Figure 1 $\mathrm{D}^{0}$, PbPb collisions at $\sqrt{s_{NN}}$ = 5.36 TeV"
    tableFig1_Dzero.keywords["observables"] = ["${v}_{2}(\mathrm{D}^{0})$ in $|y|<0.8$"]
    tableFig1_Dzero.keywords["cmenergies"] = ["5360.0"]
    tableFig1_Dzero.keywords["reactions"] = ['PbPb --> D0 + X']
    Dzero = readerFig1_Dzero.read_graph(statName)
    Dzero_syst = readerFig1_Dzero.read_graph(systName)

    # x axis
    xDzero = Variable("$p_{\mathrm{T}}$", is_independent=True, is_binned=True, units="GeV/$c$")
    xDzero.values = [(num+err_low, num+err_high) for (num, (err_low, err_high)) in zip(Dzero['x'], Dzero['dx']) ]
    # y axis
    yDzero = Variable("${v}_{2}{SP}^{\mathrm{D}^{0}}/()|_{|y|<0.8}$", is_independent=False, is_binned=False, units="")
    yDzero.add_qualifier('REACTION', 'PbPb --> D0 + X')
    yDzero.add_qualifier('SQRT(S)', '5360 GEV')
    yDzero.add_qualifier('YRAP', '-0.8 TO 0.8')
    yDzero.values = [round(num, round_digits) for num in Dzero["y"]]

    # statistical uncertainty
    yerrDzero = Uncertainty("stat", is_symmetric=True)
    yerrDzero.values = [round(num[0], round_digits) for num in Dzero["dy"]]
    yDzero.add_uncertainty(yerrDzero)

    # systematics
    yerrsysDzero = Uncertainty("syst", is_symmetric=False)
    yerrsysDzero.values = [(round(num[0], round_digits), round(num[1], round_digits)) for num in Dzero_syst["dy"]]
    yDzero.add_uncertainty(yerrsysDzero)

    # Adding variables to table
    tableFig1_Dzero.add_variable(xDzero)
    tableFig1_Dzero.add_variable(yDzero)


    ########################
    ### D+ PbPb 5.36 TeV ###
    ########################

    tableFig1_Dplus = Table("Figure 1 Dplus PbPb 5.36 TeV")
    description_Dplus = "$p_{\mathrm{T}}$-differential prompt $\mathrm{D}^{+}$ ${v}_{2}$\{SP\} at midrapidity ($|y|<0.8$) in PbPb collisions at $\sqrt{s_{NN}}$ = 5.36 TeV"
    tableFig1_Dplus.description = description_Dplus
    tableFig1_Dplus.location = "Data from Figure 1 $\mathrm{D}^{+}$, PbPb collisions at $\sqrt{s_{NN}}$ = 5.36 TeV"
    tableFig1_Dplus.keywords["observables"] = ["${v}_{2}(\mathrm{D}^{+})$ in $|y|<0.8$"]
    tableFig1_Dplus.keywords["cmenergies"] = ["5360.0"]
    tableFig1_Dplus.keywords["reactions"] = ['PbPb -->D+ + X']

    Dplus = readerFig1_Dplus.read_graph(statName)
    Dplus_syst = readerFig1_Dplus.read_graph(systName)

    # x axis
    xDplus = Variable("$p_{\mathrm{T}}$", is_independent=True, is_binned=True, units="GeV/$c$")
    xDplus.values = [(num-err_low, num+err_high) for (num, (err_low, err_high)) in zip(Dplus['x'], Dplus['dx']) ]

    # y axis
    yDplus = Variable("$v_2^{\mathrm{D}^{+}}|_{|y|<0.8}$", is_independent=False, is_binned=False, units="")
    yDplus.add_qualifier('REACTION', 'PbPb -->D+ + X')
    yDplus.add_qualifier('SQRT(S)', '5360 GEV')
    yDplus.add_qualifier('YRAP', '-0.8 TO 0.8')
    yDplus.values = [round(num, round_digits) for num in Dplus["y"]]

    # statistical uncertainty
    yerrDplus = Uncertainty("stat", is_symmetric=True)
    yerrDplus.values = [round(num[0], round_digits) for num in Dplus["dy"]]
    yDplus.add_uncertainty(yerrDplus)

    # systematics
    yerrsysDplus = Uncertainty("syst", is_symmetric=False)
    yerrsysDplus.values = [(round(num[0], round_digits), round(num[1], round_digits)) for num in Dplus_syst["dy"]]
    yDplus.add_uncertainty(yerrsysDplus)

    # Adding variables to table
    tableFig1_Dplus.add_variable(xDplus)
    tableFig1_Dplus.add_variable(yDplus)


    #########################
    ### Ds+ PbPb 5.36 TeV ###
    #########################

    tableFig1_Ds = Table("Figure 1 Ds PbPb 5.36 TeV")
    description_Ds = "$p_{\mathrm{T}}$-differential prompt $\mathrm{D}^{+}_\mathrm{s}$ ${v}_{2}$\{SP\} at midrapidity ($|y|<0.8$) in PbPb collisions at $\sqrt{s_{NN}}$ = 5.36 TeV"
    tableFig1_Ds.description = description_Ds
    tableFig1_Ds.location = "Data from Figure 1 $\mathrm{D}^{+}_\mathrm{s}$, PbPb collisions at $\sqrt{s_{NN}}$ = 5.36 TeV"
    tableFig1_Ds.keywords["observables"] = ["${v}_{2}(\mathrm{D}_{\mathrm{s}}^{+})$ in $|y|<0.8$"]
    tableFig1_Ds.keywords["cmenergies"] = ["5360.0"]
    tableFig1_Ds.keywords["reactions"] = ['PbPb -->Ds+ + X']

    Ds = readerFig1_Ds.read_graph(statName)
    Ds_syst = readerFig1_Ds.read_graph(systName)

    # x axis
    xDs = Variable("$p_{\mathrm{T}}$", is_independent=True, is_binned=True, units="GeV/$c$")
    xDs.values = [(num-err_low, num+err_high) for (num, (err_low, err_high)) in zip(Ds['x'], Ds['dx']) ]

    # y axis
    yDs = Variable("$v_2^{\mathrm{D}^{+}_\mathrm{s}}|_{|y|<0.8}$", is_independent=False, is_binned=False, units="")
    yDs.add_qualifier('REACTION', 'PbPb -->Ds+ + X')
    yDs.add_qualifier('SQRT(S)', '5360 GEV')
    yDs.add_qualifier('YRAP', '-0.8 TO 0.8')
    yDs.values = [round(num, round_digits) for num in Ds["y"]]

    # statistical uncertainty
    yerrDs = Uncertainty("stat", is_symmetric=True)
    yerrDs.values = [round(num[0], round_digits) for num in Ds["dy"]]
    yDs.add_uncertainty(yerrDs)

    # systematics
    yerrsysDs = Uncertainty("syst", is_symmetric=False)
    yerrsysDs.values = [(round(num[0], round_digits), round(num[1], round_digits)) for num in Ds_syst["dy"]]
    yDs.add_uncertainty(yerrsysDs)

    # Adding variables to table
    tableFig1_Ds.add_variable(xDs)
    tableFig1_Ds.add_variable(yDs)

    #########################
    ### Lc PbPb 5.36 TeV ###
    #########################
    tableFig1_Lc = Table("Figure 1 Lc PbPb 5.36 TeV")
    description_Lc = "$p_{\mathrm{T}}$-differential prompt $\Lambda^+_\mathrm{c}$ ${v}_{2}$\{SP\} at midrapidity ($|y|<0.8$) in PbPb collisions at $\sqrt{s_{NN}}$ = 5.36 TeV"
    tableFig1_Lc.description = description_Lc
    tableFig1_Lc.location = "Data from Figure 1 $\Lambda^+_\mathrm{c}$, PbPb collisions at $\sqrt{s_{NN}}$ = 5.36 TeV"
    tableFig1_Lc.keywords["observables"] = ["${v}_{2}(\Lambda^+_\mathrm{c})$ in $|y|<0.8$"]
    tableFig1_Lc.keywords["cmenergies"] = ["5360.0"]
    tableFig1_Lc.keywords["reactions"] = ['PbPb --> Lc + X']

    Lc = readerFig1_Lc.read_graph(statName)
    Lc_syst = readerFig1_Lc.read_graph(systName)

    # x axis
    xLc = Variable("$p_{\mathrm{T}}$", is_independent=True, is_binned=True, units="GeV/$c$")
    xLc.values = [(num-err_low, num+err_high) for (num, (err_low, err_high)) in zip(Lc['x'], Lc['dx']) ]

    # y axis
    yLc = Variable("$v_2^{\Lambda^+_\mathrm{c}}|_{|y|<0.8}$", is_independent=False, is_binned=False, units="")
    yLc.add_qualifier('REACTION', 'PbPb -->Lc + X')
    yLc.add_qualifier('SQRT(S)', '5360 GEV')
    yLc.add_qualifier('YRAP', '-0.8 TO 0.8')
    yLc.values = [round(num, round_digits) for num in Lc["y"]]

    # statistical uncertainty
    yerrLc = Uncertainty("stat", is_symmetric=True)
    yerrLc.values = [round(num[0], round_digits) for num in Lc["dy"]]
    yLc.add_uncertainty(yerrLc)

    # systematics
    yerrsysLc = Uncertainty("syst", is_symmetric=False)
    yerrsysLc.values = [(round(num[0], round_digits), round(num[1], round_digits)) for num in Lc_syst["dy"]]
    yLc.add_uncertainty(yerrsysLc)
    
    # Adding variables to table
    tableFig1_Lc.add_variable(xLc)
    tableFig1_Lc.add_variable(yLc)

    return tableFig1_Dzero, tableFig1_Dplus, tableFig1_Ds, tableFig1_Lc


def sub():
    submission = Submission()

    # submission.comment = "Measurements of the  elliptic flow of prompt $\mathrm{D}^0$, $\mathrm{D}^+$, $\mathrm{D}^+_\mathrm{s}$, and $\Lambda^+_\mathrm{c}$, at  midrapidity in Pb$-$Pb collisions at $\sqrt{s}=5.36$ TeV with the ALICE detector are presented. The D-meson  elliptic flow as a function of transverse momentum (p_\mathrm{T}) are provided with improved precision and granularity. The ratios of p_\mathrm{T}-differential meson  elliptic flow based on this publication and on measurements at different rapidity and collision energy provide a constraint on gluon parton distribution functions at low values of Bjorken-$x$ ($10^{-5}-10^{-4}$). The measurements of $\Lambda^+_\mathrm{c}$ ($\Xi^+_\mathrm{c}$) baryon production extend the measured p_\mathrm{T} intervals down to $p_\mathrm{T}=0(3)$~GeV$/c$. These measurements are used to determine the charm-quark fragmentation fractions and the $\mathrm{c}\\bar{\mathrm{c}}$ production cross section at midrapidity ($|y|<0.8$) based on the sum of the  elliptic flow of the weakly-decaying ground-state charm hadrons $\mathrm{D}^0$, $\mathrm{D}^+$, $\mathrm{D}^+_\mathrm{c}$, $\Lambda^+_\mathrm{c}$, $\Xi^0_\mathrm{c}$ and, for the first time, $\Xi^+_\mathrm{c}$, and of the strongly-decaying $J/\psi$ mesons. The first measurements of $\Xi^+_\mathrm{c}$ and $\Sigma_\mathrm{c}^{0,+,++}$ fragmentation fractions at midrapidity are also reported. A significantly larger fraction of charm quarks hadronising to baryons is found compared to $\mathrm{e}^+\mathrm{e}^-$ and ep collisions. The $\mathrm{c}\\bar{\mathrm{c}}$ production cross section at midrapidity is found to be at the upper bound of state-of-the-art perturbative QCD calculations."
    submission.comment = "The ALICE collaboration reports the azimuthal-anisotropy coefficient $\mathrm{v}_2$ of prompt $\mathrm{D}^0$, $\mathrm{D}^+$, $\mathrm{D}^+_\mathrm{s}$ mesons and the first measurement of $\mathrm{v}_2$ of prompt $\Lambda^+_\mathrm{c}$ baryons in semicentral PbPb collisions at a center-of-mass energy per nucleon pair of $\sqrt{s_{NN}}=5.36$ TeV. The D mesons and $\Lambda^+_\mathrm{c}$baryons are reconstructed in their hadronic decays at midrapidity ($|y|<0.8$) in the transverse-momentum interval 0.5 $< p_\mathrm{T} <$ 24 GeV/c. Similar $\mathrm{v}_2$ values are measured for $\mathrm{D}^0$ and $\mathrm{D}^+$, while a hint of a difference ($2.6\sigma$) emerges between $\mathrm{D}^0$ and $\mathrm{D}^+_\mathrm{s}$ mesons in the $1 <p_\mathrm{T} < 5~GeV/c$ interval. A larger $\mathrm{v}_2$ for $\Lambda^+_\mathrm{c}$ baryons with respect to $\mathrm{D}^0$ mesons is observed with $3.7\sigma$ significance for $4 < p_\mathrm{T} < 12~GeV/c$, providing evidence for the partonic origin of charm-hadron $\mathrm{v}_2$ and hadron formation via quark coalescence. This interpretation is further supported by comparisons with theoretical calculations of charm-quark transport in a hydrodynamically expanding medium. "
    ### figure 1
    tableFig1_Dzero, tableFig1_Dplus, tableFig1_Ds, tableFig1_Lc = fig1()
    submission.add_table(tableFig1_Dzero)
    submission.add_table(tableFig1_Dplus)
    submission.add_table(tableFig1_Ds)
    submission.add_table(tableFig1_Lc)

    #Creates submission
    submission.create_files("charmV2PbPb536TeVPaper")


if __name__ == "__main__":
    #this will be executed if run like a script
    sub()
