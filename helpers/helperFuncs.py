"""
-------------------------------------------------------------------------------
Name:        helperFuncs
Purpose:     Collection of helper functions for evaluation scripts

Author:      Marcus Vogt

Created:     27.11.2021
Copyright:   Chair of Sustainable Manufacturing and Life Cycle Engineering, Institute of Machine Tools and Production Technology, Technische Universität Braunschweig, Langer Kamp 19b, 38106 Braunschweig, Germany
Licence:     MIT
-------------------------------------------------------------------------------
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import helpers.WetAirToolBox as wetTB

def interpolateDataFrameBasedOnIndex(df: pd.DataFrame, column: str, value: float,
                                     fillnaMethod: str = "backfill"):
    """
    Based on a given pandas DataFrame (df) this function inserts a value to the relevant column of the df
    and interpolates linearly on the given index
    :param df: pd.DataFrame to be interpolated
    :param column: name of column of the value
    :param value: numeric value to be inserted
    :param rowIndex: index of row to be replaced
    :param fillnaMethod: Fill
    :return: df
    """
    df.loc[-1, column] = value
    df.sort_values(by=column, inplace=True)
    df.index = df[column].values
    df.interpolate(method='index', axis=0, inplace=True)
    df.fillna(method=fillnaMethod, inplace=True)
    return df

def extendStaticDF(dfStaticResults: pd.DataFrame):
    """
    This small helper functions extends the values of the static result DataFrame
    :param dfStaticResults: result data set
    :return: dfStaticResults: extended result data set
    """
    def getLocation(row):
        return row['locationVariant'][:2]

    def calculateDewPoint(row):
        return wetTB.relHumidity_Temp2dewPoint(row["OutsideTemperatureDegrees"], row["OutsideRelativeHumidity"])

    dfStaticResults["location"] = dfStaticResults.apply(lambda row: getLocation(row), axis=1)
    dfStaticResults["finalEnergy"] = dfStaticResults["electricEnergyKwh"] + dfStaticResults["naturalGasEnergyKwh"] + \
                                     dfStaticResults["districtHeatingEnergyKwh"]
    dfStaticResults["OutsideDewPointTemperatureDegrees"] = dfStaticResults.apply(lambda row: calculateDewPoint(row),
                                                                                 axis=1)
    return dfStaticResults

# save plot to local file
def save_plot_to_file(file_name, fig, savedir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")):
    """ This method saves the plot to a specified location.
     Parameters:
            ----------
            file_name: str
                The name of the file the plot should be saved in.

            fig: matplotlib figure
                Matplotlib figure instance to be saved.

            savedir : str
                path were results/figures etc. should be saved, defaults to output folder.

            Returns:
            ----------
            None
                saves image to given local path location.
    """
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    fig.savefig(os.path.join(savedir, file_name))
    plt.close('all')  # close all current open figures to avoid memory overload

def set_param_recursive(pipeline_steps, parameter, value):
    """Recursively iterate through all objects in the pipeline and set a given parameter.

    Parameters
    ----------
    pipeline_steps: array-like
        List of (str, obj) tuples from a scikit-learn pipeline or related object
    parameter: str
        The parameter to assign a value for in each pipeline object
    value: any
        The value to assign the parameter to in each pipeline object
    Returns
    -------
    None

    """
    for (_, obj) in pipeline_steps:
        recursive_attrs = ["steps", "transformer_list", "estimators"]
        for attr in recursive_attrs:
            if hasattr(obj, attr):
                set_param_recursive(getattr(obj, attr), parameter, value)
        if hasattr(obj, "estimator"):  # nested estimator
            est = getattr(obj, "estimator")
            if hasattr(est, parameter):
                setattr(est, parameter, value)
        if hasattr(obj, parameter):
            setattr(obj, parameter, value)