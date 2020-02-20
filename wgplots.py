import scipy
import scipy.stats
import pandas as pd
import numpy as np
import os

import wg1template
from wg1template.histogram_plots import *
from wg1template.point_plots import *
from wg1template.plot_style import TangoColors
from wg1template.plot_utilities import export

directory='fancyplots/'
if not os.path.exists(directory):
    os.mkdir(directory)


df=pd.read_csv('data.csv')

electrons = df.query('antiB0_extraInfo_decayModeID == 1 and DST_pi_p < 0.35 and e_electronID > 0.85 and antiB0_foxWolframR2 <0.25 and 1.85 < D0_M < 1.88'+
    ' and 0.144 < Dst_massDifference_0 < 0.148 and e_useCMSFrame_p > 1.2')


muons = df.query('antiB0_extraInfo_decayModeID == 2 and DST_pi_p < 0.35 and e_muonID > 0.9 and antiB0_foxWolframR2 <0.25 and 1.85 < D0_M < 1.88'+
    ' and 0.144 < Dst_massDifference_0 < 0.148 and e_useCMSFrame_p > 1.2')


#print(df.head())v
def get_df_name(df):
    name =[x for x in globals() if globals()[x] is df][0]
    return name

def make_histogram_R2(var, name, df):
    bb = df[(df['MCtype'] < 2)]
    cont = df[(df['MCtype'] > 1)]

    mixed = df[(df['MCtype'] == 0)]
    charged = df[(df['MCtype'] == 1)]
    uubar = df[(df['MCtype'] == 2)]
    ddbar = df[(df['MCtype'] == 3)]
    ccbar = df[(df['MCtype'] == 4)]
    ssbar = df[(df['MCtype'] == 5)]
    taupair = df[(df['MCtype'] == 6)]

    hp = StackedHistogramPlot(var)

    hp.add_component("Continuum", cont['antiB0_foxWolframR2'], color=TangoColors.sky_blue, comp_type='stacked')
    hp.add_component(r'B$\overline{B}$', bb['antiB0_foxWolframR2'],  color=TangoColors.orange, comp_type='stacked')

    fig, ax = create_solo_figure()
    hp.plot_on(ax, ylabel="Candidates")
    add_descriptions_to_plot(ax, experiment='Belle II', luminosity=r"$\int \mathcal{L} \,dt=30\,\mathrm{fb}^{-1}$")
    plt.savefig(directory+name)
    plt.close()

    hp2 = StackedHistogramPlot(var)


    hp2.add_component("uubar", uubar['antiB0_foxWolframR2'],  color=TangoColors.chocolate, comp_type='stacked')
    hp2.add_component("ddbar", ddbar['antiB0_foxWolframR2'],  color=TangoColors.chameleon, comp_type='stacked')
    hp2.add_component("ccbar", ccbar['antiB0_foxWolframR2'],  color=TangoColors.sky_blue, comp_type='stacked')
    hp2.add_component("ssbar", ssbar['antiB0_foxWolframR2'],  color=TangoColors.aluminium, comp_type='stacked')
    hp2.add_component("taupair", taupair['antiB0_foxWolframR2'],  color=TangoColors.scarlet_red, comp_type='stacked')
    hp2.add_component("charged", charged['antiB0_foxWolframR2'],  color=TangoColors.plum, comp_type='stacked')
    hp2.add_component("mixed", mixed['antiB0_foxWolframR2'],  color=TangoColors.orange,comp_type='stacked')



    fig, ax = create_solo_figure()
    hp2.plot_on(ax, ylabel="Candidates")
    add_descriptions_to_plot(ax, experiment='Belle II', luminosity=r"$\int \mathcal{L} \,dt=30\,\mathrm{fb}^{-1}$")
    plt.savefig(directory+'R2_all.png')
    plt.close()




def make_histogram(var,name,dfvar,df=electrons,signal='antiB0_isSignalAcceptMissingNeutrino',plot_cont=True, bglabel='Background', siglabel='Signal' ):

    if not plot_cont:
        bkg = df[(df[signal] == 0)]
        sig = df[df[signal] == 1]
        cont = None

    else:
        bkg = df[(df[signal] == 0) & (df.MCtype <=1)]
        sig = df[df[signal] ==1]
        cont = df[(df[signal] == 0) & (df.MCtype >=2)]
    hp = StackedHistogramPlot(var)
    hp.add_component(bglabel, bkg[dfvar],  color=TangoColors.sky_blue,
                     comp_type='stacked')
    if cont is not None:
        hp.add_component("Continuum", cont[dfvar], color=TangoColors.slate,
                         comp_type='stacked')
    hp.add_component(siglabel, sig[dfvar],  color=TangoColors.orange, comp_type='stacked')

    fig, ax = create_solo_figure()
    hp.plot_on(ax, ylabel="Candidates")
    if "electron" in get_df_name(df):
        add_descriptions_to_plot(
            ax,
            experiment='Belle II',
            luminosity=r"$\int \mathcal{L} \,dt=30\,\mathrm{fb}^{-1}$",
            additional_info=r"MC13a - $D^{*+} \mu^- \overline{\nu}_\mu$"
        )
    if "muon" in get_df_name(df):
        add_descriptions_to_plot(
            ax,
            experiment='Belle II',
            luminosity=r"$\int \mathcal{L} \,dt=30\,\mathrm{fb}^{-1}$",
            additional_info=r"MC13a - $D^{*+} e^- \overline{\nu}_e$"
        )

    plt.savefig(directory+name)
    #export(fig, 'stacked', 'examples')
    plt.close()



electrons_dM = df.query('antiB0_extraInfo_decayModeID == 1 and DST_pi_p < 0.35 and e_electronID > 0.85 and antiB0_foxWolframR2 <0.25 and 1.85 < D0_M < 1.88'+
    ' and 0.14 < Dst_massDifference_0 < 0.154 and e_useCMSFrame_p > 1.2')
electrons_p = df.query('antiB0_extraInfo_decayModeID == 1 and DST_pi_p < 0.35 and e_electronID > 0.85 and antiB0_foxWolframR2 <0.25 and 1.85 < D0_M < 1.88'+
    ' and 0.14 < Dst_massDifference_0 < 0.154 and e_useCMSFrame_p > 0.5')

muons_dM = df.query('antiB0_extraInfo_decayModeID == 2 and DST_pi_p < 0.35 and e_muonID > 0.9 and antiB0_foxWolframR2 <0.25 and 1.85 < D0_M < 1.88'+
    ' and 0.14 < Dst_massDifference_0 < 0.154 and e_useCMSFrame_p > 1.2')
muons_p = df.query('antiB0_extraInfo_decayModeID == 2 and DST_pi_p < 0.35 and e_muonID > 0.9 and antiB0_foxWolframR2 <0.25 and 1.85 < D0_M < 1.88'+
    ' and 0.14 < Dst_massDifference_0 < 0.154 and e_useCMSFrame_p > 0.5')

costheta = HistVariable("costheta", n_bins=15, scope=(-5, 4), var_name="cos$\Theta_{BY}$", unit="")

FWR2 = HistVariable("FWR2", n_bins=40, scope=(0, 1), var_name="R2", unit="")


missM2= HistVariable("missM2", n_bins=15, scope=(-4, 4), var_name="$m^2_{miss}$", unit="$\mathrm{GeV}^2$/$c^4$")

dM = HistVariable("dM",n_bins=25, scope=(0.140, 0.154), var_name="$\Delta M$", unit="$\mathrm{GeV}$/$c^2$")

p_l = HistVariable("p_l", n_bins=17, scope=(0.5, 2.5), var_name="$p^*_\ell $", unit="$\mathrm{GeV}$/$c$")



make_histogram(costheta, 'cos_e.png', 'antiB0_cosThetaBetweenParticleAndNominalB', electrons)
make_histogram(costheta, 'cos_mu.png', 'antiB0_cosThetaBetweenParticleAndNominalB', muons)
make_histogram(missM2, 'missM2_e.png', 'antiB0_REC_MissM2', electrons)
make_histogram(missM2, 'missM2_mu.png', 'antiB0_REC_MissM2', muons)
make_histogram(dM, 'dM_e.png', 'Dst_massDifference_0', electrons_dM, signal = 'Dst_isSignal', plot_cont = False, bglabel = 'Fake D*', siglabel = 'True D*')
make_histogram(dM, 'dM_mu.png', 'Dst_massDifference_0', muons_dM, signal = 'Dst_isSignal', plot_cont = False, bglabel = 'Fake D*', siglabel = 'True D*')
make_histogram(p_l, 'p_e.png', 'e_useCMSFrame_p', electrons_p)
make_histogram(p_l, 'p_mu.png', 'e_useCMSFrame_p', muons_p)
make_histogram_R2(FWR2, 'R2.png', df )
