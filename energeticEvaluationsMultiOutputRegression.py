"""
-------------------------------------------------------------------------------
Name:        energeticEvaluationsMultiOutputRegression.py
Purpose:     Evaluation of energetic impact of HVAC system based on multi-output regression model using the static data set

Author:      Marcus Vogt

Created:     10.12.2021
Copyright:   Chair of Sustainable Manufacturing and Life Cycle Engineering, Institute of Machine Tools and Production Technology, Technische Universität Braunschweig, Langer Kamp 19b, 38106 Braunschweig, Germany
Licence:     MIT
-------------------------------------------------------------------------------
"""

import os
import pandas as pd
import energeticEvaluations as enEval
import numpy as np
import helpers.helperFuncs as helperFuncs
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from sklearn.multioutput import RegressorChain
from xgboost import XGBRegressor
from helpers.stackingEstimator import StackingEstimator
from sklearn.feature_selection import VarianceThreshold
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import FunctionTransformer
from sklearn.ensemble import AdaBoostRegressor
from copy import copy

def interpolateScalingFactorAndInternalLoadsMultiOutputRegression(dfStaticResults: pd.DataFrame, averageOutsideRelativeHumidity: float,
                                             averageOutsideTemperature: float, scalingFactorS: float,
                                                                  maxWasteHeatRoomW: float, maxMoistureLoad: float):
    """
    This function interpolates the scaling factor and internal loads of the static result data set
    :param dfStaticResults: pd.DataFrame: static results data set
    :param averageOutsideRelativeHumidity: float: average outside relative humidity in %
    :param averageOutsideTemperature: float: average outside temperature in °C
    :param scalingFactorS: float: calculated scaling factor s
    :param maxWasteHeatRoomW: float: max. waste heat in Watt
    :param maxMoistureLoad: float: max. moisture load in room in kg/s
    :return: dictionary of interpolated results based on static result data set using multi-output regression model.
             Furthermore, 10-fold cross validation with 3 repetitions is performed for the model to compute uncertainties
             as mean absolute error with unit of the predicted variable (kWh)
    """

    evaluateResultsKFold = True
    # create datasets
    X_columnNames = ["ScalingFactorS","DryRoomHeatLoad","DryRoomMoistureLoad","OutsideRelativeHumidity","OutsideTemperatureDegrees"]
    y_columnNames = ["electricEnergyKwh","naturalGasEnergyKwh","districtHeatingEnergyKwh"]

    X = dfStaticResults[X_columnNames].to_numpy()
    y = dfStaticResults[y_columnNames].to_numpy()

    XGBSingleOutput = make_pipeline(
        make_union(
            FunctionTransformer(copy),
            FunctionTransformer(copy)
        ),
        StackingEstimator(
            estimator=XGBRegressor(learning_rate=0.1, max_depth=3, min_child_weight=1, n_estimators=100, n_jobs=1,
                                   objective="reg:squarederror", subsample=1.0, verbosity=0)),
        StackingEstimator(estimator=AdaBoostRegressor(learning_rate=1.0, loss="exponential", n_estimators=100)),
        VarianceThreshold(threshold=0.01),
        XGBRegressor(learning_rate=0.1, max_depth=10, min_child_weight=1, n_estimators=100, n_jobs=1,
                     objective="reg:squarederror", subsample=1.0, verbosity=0)
    )
    # Fix random state for all the steps in exported pipeline: with 5 inputs and trained with 100 tpot generations and populations
    helperFuncs.set_param_recursive(XGBSingleOutput.steps, 'random_state', 42)
    # define the chained multi-output wrapper model
    model = RegressorChain(XGBSingleOutput)
    model.fit(X, y)
    # make a prediction (in the same order as X_columnNames)
    row = [scalingFactorS, maxWasteHeatRoomW, maxMoistureLoad, averageOutsideRelativeHumidity/100, averageOutsideTemperature]
    yhat = model.predict(np.asarray([row]))
    # organize predicted output as dictionary
    d = {}
    for A, B in zip(np.array(y_columnNames), yhat[0]):
        d[A] = B
    # just define n_scores dummy output if evaluateResultsKFold=False
    n_scores = np.ones(5)
    if evaluateResultsKFold:
        # define the evaluation procedure to quantify model uncertainty
        cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
        # evaluate the model and collect the scores. Available scoring for model evaluation: https://scikit-learn.org/stable/modules/model_evaluation.html
        n_scores = cross_val_score(model, X, y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
        # force the scores to be positive => because mean absolute error is computed this n_scores has the unit of predicted values (kWh)
        n_scores = np.absolute(n_scores)

    return d, n_scores


if __name__ == "__main__":

      ########### read in data set ############
      current_dir = os.path.dirname(os.path.realpath(__file__))
      staticResultPath = os.path.join(current_dir, "data", "automateSimulationStaticResults.csv")
      dfStaticResults = pd.read_csv(staticResultPath, index_col=0)
      # currently the locations "DU" and "LV" are outliers, thus exclude them:
      dfStaticResults = helperFuncs.extendStaticDF(dfStaticResults)

      ########### boundary parameters ############
      averageOutsideRelativeHumidity = 77.77662949012851 
      averageOutsideTemperatureDegrees = 27.769243088784297
      maxHumansInAirFlow = 3 # maximum number of humans in air flow zones in room
      maxHumansInRoom = 6 # total maximum amount of humans in room
      maxWasteHeatRoomW = 4000 # max waste heat in W
      roomDewPointDegrees = -50 # dew point temperature in °C
      inletDewPointDegrees = -60 # dew point temperature in °C
      inletTemperatureDegrees = 20 # inlet temperature in °C
      leakagesSuctionVolumeFlowM3H = 700 # volume flow in m^3/h

      ########### evaluations ############
      scalingFactorS, maxMoistureLoad = enEval.boundaryParameters2scalingFactorMoistureLoad(maxHumansInAirFlow=maxHumansInAirFlow,
                                                                                     maxHumansInRoom=maxHumansInRoom,
                                                                                     roomDewPointDegrees=roomDewPointDegrees,
                                                                                     inletDewPointDegrees=inletDewPointDegrees,
                                                                                     inletTemperatureDegrees=inletTemperatureDegrees,
                                                                                     leakagesSuctionVolumeFlowM3H=leakagesSuctionVolumeFlowM3H)
      print("The scaling factor S is: {}, volume flow is: {} m^3/h, max. moisture load is: {} kg/s"
            .format(round(scalingFactorS, 3), round(scalingFactorS*11000, 3), round(maxMoistureLoad, 7)))

      d, n_scores = interpolateScalingFactorAndInternalLoadsMultiOutputRegression(dfStaticResults,
                                    averageOutsideRelativeHumidity=averageOutsideRelativeHumidity,
                                    averageOutsideTemperature=averageOutsideTemperatureDegrees, scalingFactorS=scalingFactorS,
                                    maxWasteHeatRoomW=maxWasteHeatRoomW, maxMoistureLoad=maxMoistureLoad)
      print("The final results of the interpolation based on multi-output regression model are:")
      print(d)
      # summarize performance
      print("Mean Absolute Error: %.3f kWh. Standard deviation: (%.3f) kWh" % (np.mean(n_scores), np.std(n_scores)))

