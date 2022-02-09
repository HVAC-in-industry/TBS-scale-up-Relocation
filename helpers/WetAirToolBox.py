"""
-------------------------------------------------------------------------------
Name:        WetAirToolBox
Purpose:     Different calculations in conjunction with humid air

Author:      Marcus Vogt

Created:     27.11.2021
Copyright:   Chair of Sustainable Manufacturing and Life Cycle Engineering, Institute of Machine Tools and Production Technology, Technische Universität Braunschweig, Langer Kamp 19b, 38106 Braunschweig, Germany
Licence:     MIT
-------------------------------------------------------------------------------
"""

import numpy as np

# Coefficients of the Magnus formula
a = 6.112
b = 17.62
c = 243.12

R_L = 287   # Gas constant air
R_WD = 461.4 # Gas constant water vapour
ratio_R = R_L/R_WD
pG = 1013 # air pressure [hPa]

def humidity_dewpoint2abs (T, T_TP):
    ps = a * np.exp((b * T) / (c + T))   # Saturation vapour pressure in [hPa]
    phi = np.exp((((T_TP*b*c)/(c+T)) - ((c*b*T)/(c+T))) / (T_TP + c))
    pD = phi * ps
    X = ratio_R * (pD / (pG - pD))
    return X

def humidity_dewpoint2abs2 (T, T_TP):
    ps = a * np.exp((b * T) / (c + T))   # Saturation vapour pressure in [hPa]
    phi = np.exp(((T_TP*b) / (T_TP+c)) - ((T*b) / (T+c)))
    pD = phi * ps
    X = ratio_R * (pD / (pG - pD))
    return X


def humidity_abs2rel(T, X):
    ps = a * np.exp((b * T) / (c + T))
    pD = pG*X/(ratio_R+X)
    phi = pD/ps
    return phi


def humidity_rel2abs(T, phi):
    phi = phi/100
    ps = a * np.exp((b * T) / (c + T))
    pD = phi * ps
    X = ratio_R * (pD / (pG - pD))
    return X

def WaterVapurePartialPressure(X):
    pD = pG*X/(ratio_R+X) # R_L/R_D = 0.622   p_D: Water vapour partial pressure in hPa
    return pD # Water vapour partial pressure in hPa

def humidity_abs2dewpoint(X):
    pD = X*pG/(ratio_R+X)
    T_TP = (c*np.log(pD/a)) / (b - np.log(pD/a))
    return T_TP

def relHumidity_Temp2dewPoint(T, phi):
    """Calculate dew point from temperature (°C) and relative humidity (%, e.g. 77 % => 0.77 as input)"""
    return (109.8 + T) * (phi**(1/8.02)) - 109.8