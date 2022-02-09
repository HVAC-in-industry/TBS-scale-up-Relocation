"""
-------------------------------------------------------------------------------
Name:        manualPlotting
Purpose:     Manual data analytics of generated results by automateSimulation script

Author:      Marcus Vogt

Created:     17.11.2021
Copyright:   Chair of Sustainable Manufacturing and Life Cycle Engineering, Institute of Machine Tools and Production Technology, Technische Universität Braunschweig, Langer Kamp 19b, 38106 Braunschweig, Germany
Licence:     MIT
-------------------------------------------------------------------------------

"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import helpers.helperFuncs as helperFuncs

if __name__ == "__main__":
    ########### input declarations ############
    createPublicationPlots = True
    savePlots = True
    withDynamic = False
    current_dir = os.path.dirname(os.path.realpath(__file__))
    staticResultPath = os.path.join(current_dir, "data", "automateSimulationStaticResults.csv")
    dynamicResultPath = os.path.join(current_dir, "data", "automateSimulationDynamicResults.csv")
    dfStaticResults = pd.read_csv(staticResultPath, index_col=0)
    # Todo: 1) First download automateSimulationDynamicResults.csv from Mendeley data and insert into the data folder
    #  2) Adapt the list below for other values to be plotted over time from this data set
    columnList2PlotDynamic = ["JK-1-electricEnergyKwh", "JK-7-naturalGasEnergyKwh"]
    nrowsDynamicDataSet = 10000
    ########### boxplot generation ############
    if createPublicationPlots:
        import helpers.rc_parameters_matplotlib as rc_params
        plt.rcParams.update(rc_params.latex_largeColumn)

    dfStaticResults = helperFuncs.extendStaticDF(dfStaticResults)
    # get DataFrames per group of LoadScalingFactor
    dfStaticResultsGrouped = dfStaticResults.groupby(by="LoadScalingFactor")

    figDict = {}
    for name, groupDF in dfStaticResultsGrouped:
        # order data set from cool to warm regions
        groupDF.sort_values(by=['OutsideDewPointTemperatureDegrees'], inplace=True, ascending=True) # "OutsideDewPointTemperatureDegrees" or "OutsideTemperatureDegrees"
        fig = plt.figure()
        sns.boxplot(x="location", y="electricEnergyKwh", data=groupDF, palette="coolwarm") #y="electricEnergyKwh" or "finalEnergy"
        fig.suptitle(r"LoadScalingFactor: {}".format(name))
        plt.xlabel(r'Location')
        plt.ylabel(r'Electric energy demand [$kWh$]') #r'Electric energy demand [$kWh$]' or r'Final energy demand [$kWh$]'
        plt.tight_layout()
        figDict[name] = fig

    ########### plotting of temporal results ############
    if withDynamic:
        dfDynamicResults = pd.read_csv(dynamicResultPath, index_col=0, nrows=nrowsDynamicDataSet)
        fig2, ax2 = plt.subplots()
        sns.lineplot(data=dfDynamicResults[columnList2PlotDynamic], ax=ax2)
        plt.tight_layout()

    plt.show()

    if savePlots:
        for name in figDict:
            nameWithoutPoint = str(name).replace(".", ",")
            helperFuncs.save_plot_to_file(file_name="LoadScaling{}EnergyDemandLocations".format(nameWithoutPoint),
                                          fig=figDict[name],
                                          savedir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "images"))