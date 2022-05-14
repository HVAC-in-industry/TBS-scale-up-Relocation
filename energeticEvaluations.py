"""
-------------------------------------------------------------------------------
Name:        energeticEvaluations
Purpose:     Evaluation of energetic impact of HVAC system based on provided static data set

Author:      Marcus Vogt

Created:     27.11.2021
Copyright:   Chair of Sustainable Manufacturing and Life Cycle Engineering, Institute of Machine Tools and Production Technology, Technische Universität Braunschweig, Langer Kamp 19b, 38106 Braunschweig, Germany
Licence:     CC BY-SA 4.0
-------------------------------------------------------------------------------
"""

import os
import pandas as pd
import helpers.WetAirToolBox as WetAirToolBox
import helpers.helperFuncs as helperFuncs

def boundaryParameters2scalingFactorMoistureLoad(maxHumansInAirFlow: int, maxHumansInRoom: int,
                                                 roomDewPointDegrees: float,
                                                 inletDewPointDegrees: float, inletTemperatureDegrees: float,
                                                 leakagesSuctionVolumeFlowM3H: float):
      """
      This functions translates the boundary parameter input to the corresponding scaling factor S and
      calculates the occurring moisture load in kg/s
      :param maxHumansInAirFlow: maximum number of humans in air flow zones in room
      :param maxHumansInRoom: total maximum amount of humans in room
      :param roomDewPointDegrees: desired dew point temperature inside room in °C
      :param inletDewPointDegrees: dew point temperature of supply air into room in °C
      :param inletTemperatureDegrees: supply air temperature in °C
      :param leakagesSuctionVolumeFlowM3H: volume flow escaping through leakages and technical suction out of room in m^3/h
      :return: scaling factor s & moisture load in kg/s
      """
      ### constants ###
      densityAirkgm3 = 1.17343
      moistureInputPerHumankgH = 0.113
      volumeFlowInRefM3H = 11000
      ### calculations ###
      roomDewPointAbsHumidity = WetAirToolBox.humidity_dewpoint2abs(inletTemperatureDegrees, roomDewPointDegrees)
      inletDewPointDegreesAbsHumidity = WetAirToolBox.humidity_dewpoint2abs(inletTemperatureDegrees,
                                                                            inletDewPointDegrees)
      volumeFlowInAir = (maxHumansInAirFlow * moistureInputPerHumankgH) / (
                    densityAirkgm3 * (roomDewPointAbsHumidity - inletDewPointDegreesAbsHumidity))
      volumeFlowInAirMax = volumeFlowInAir + leakagesSuctionVolumeFlowM3H
      scalingFactorS = volumeFlowInAirMax / volumeFlowInRefM3H
      maxMoistureLoad = moistureInputPerHumankgH * maxHumansInRoom / 3600
      return scalingFactorS, maxMoistureLoad

def interpolateScalingFactorAndInternalLoads(dfStaticResults: pd.DataFrame, consideredLocation: str,
                                             scalingFactorS: float, maxWasteHeatRoomW: float, maxMoistureLoad: float):
      """
      This function interpolates the scaling factor and internal loads of the static result data set
      :param dfStaticResults: static results data set
      :param consideredLocation: considered available location without case number e.g. "OS"
      :param scalingFactorS: calculated scaling factor s
      :param maxWasteHeatRoomW: max. waste heat in Watt
      :param maxMoistureLoad: max. moisture load in room in kg/s
      :return: interpolated results based on static result data set
      """
      dfStaticResults = helperFuncs.extendStaticDF(dfStaticResults)
      dfStaticResultsLocation = dfStaticResults[dfStaticResults['location'] == consideredLocation]
      dfStaticResultsLocationGrouped = dfStaticResultsLocation.groupby(by="LoadScalingFactor")
      resultSeriesList = []
      for name, groupDF in dfStaticResultsLocationGrouped:
            groupDF = helperFuncs.interpolateDataFrameBasedOnIndex(groupDF, column="ScalingFactorS",
                                                                   value=scalingFactorS)
            resultRowSeries = groupDF.loc[scalingFactorS]
            resultRowSeries.name = name
            resultSeriesList.append(resultRowSeries)

      resultDF = pd.concat(resultSeriesList, axis=1)
      resultDFTransposed = resultDF.T
      # assure dTypes due to concat operation
      for col in resultDFTransposed:
            resultDFTransposed[col] = pd.to_numeric(resultDFTransposed[col], errors='ignore')

      # interpolate results regarding moisture load
      resultDFTransposed = helperFuncs.interpolateDataFrameBasedOnIndex(resultDFTransposed,
                                                                        column="DryRoomMoistureLoad",
                                                                        value=maxMoistureLoad)
      # interpolate results regarding heat load last (more significant impact on energy consumption)
      resultDFTransposed = helperFuncs.interpolateDataFrameBasedOnIndex(resultDFTransposed, column="DryRoomHeatLoad",
                                                                        value=maxWasteHeatRoomW)
      finalResultsOfInterpolation = resultDFTransposed.loc[maxWasteHeatRoomW]
      return finalResultsOfInterpolation


if __name__ == "__main__":

      ########### read in data set ############
      current_dir = os.path.dirname(os.path.realpath(__file__))
      staticResultPath = os.path.join(current_dir, "data", "automateSimulationStaticResults.csv")
      dfStaticResults = pd.read_csv(staticResultPath, index_col=0)

      ########### boundary parameters ############
      consideredLocation = "OS" # considered available location without case number e.g. "OS"
      useBoundaryParameters = False
      if useBoundaryParameters:
          maxHumansInAirFlow = 4 # maximum number of humans in air flow zones in room
          maxHumansInRoom = 6 # total maximum amount of humans in room
          maxWasteHeatRoomW = 3000 # max waste heat in W
          roomDewPointDegrees = -50 # dew point temperature in °C
          inletDewPointDegrees = -60 # dew point temperature in °C
          inletTemperatureDegrees = 20 # inlet temperature in °C
          leakagesSuctionVolumeFlowM3H = 500 # volume flow in m^3/h
      else:  # this approach can be used if the boundary conditions below are known
          scalingFactorS = 1.1  # scaling factor calculated from necessary air flow
          maxMoistureLoad = 0.5  # max. moisture load in kg/s
          maxWasteHeatRoomW = 3000  # max waste heat in W


      ########### evaluations ############
      if useBoundaryParameters:
          scalingFactorS, maxMoistureLoad = boundaryParameters2scalingFactorMoistureLoad(maxHumansInAirFlow= maxHumansInAirFlow,
                                                                                     maxHumansInRoom=maxHumansInRoom,
                                                                                     roomDewPointDegrees=roomDewPointDegrees,
                                                                                     inletDewPointDegrees=inletDewPointDegrees,
                                                                                     inletTemperatureDegrees=inletTemperatureDegrees,
                                                                                     leakagesSuctionVolumeFlowM3H=leakagesSuctionVolumeFlowM3H)
      print("The scaling factor S is: {}, volume flow is: {} m^3/h, max. moisture load is: {} kg/s"
            .format(round(scalingFactorS, 3), round(scalingFactorS*11000, 3), round(maxMoistureLoad, 7)))

      finalResultsOfInterpolation = interpolateScalingFactorAndInternalLoads(dfStaticResults,
                                    consideredLocation=consideredLocation, scalingFactorS=scalingFactorS,
                                    maxWasteHeatRoomW=maxWasteHeatRoomW, maxMoistureLoad=maxMoistureLoad)
      print("The final results of the interpolation are:")
      print(finalResultsOfInterpolation)

