import pandas as pd
import numpy as np
import sympy as sp

# DEFINE DEMAND
d_01, d_02, d_03, d_04 = sp.symbols('d0(1:5)')
d_12, d_13, d_14 = sp.symbols('d1(2:5)')
d_23, d_24 = sp.symbols('d2(3:5)')
d_34 = sp.symbols('d34')
d = sp.Matrix([[0, d_01, d_02, d_03, d_04],
               [0, 0,    d_12, d_13, d_14], 
               [0, 0,    0,    d_23, d_24],
               [0, 0,    0,    0,    d_34],
               [0, 0,    0,    0,    0]])

# Define Step Goals for first Matrix
d_1_goal = sp.Matrix([[0, d_02, d_04],
                      [0, 0,    d_24],
                      [0, 0,    0   ]])
d_2_goal = sp.Matrix([[0, d_02+d_01, d_03+d_04],
                      [0, 0,         d_24+d_23],
                      [0, 0,         0        ]])
d_3_goal = sp.Matrix([[0, d_02+d_01+d_12, d_03+d_04+d_14],
                      [0, 0,              d_24+d_23+d_34],
                      [0, 0,              0             ]])
d_4_goal = sp.Matrix([[0, d_01 + d_02 + d_12, d_03 + d_04 + d_13 + d_14],
                      [0, 0,                  d_23 + d_24 + d_34       ],
                      [0, 0,                  0                        ]])

# Define Step Goals for second Matrix
d_01, d_02, d_03, d_04, d_05, d_06 = sp.symbols('d0(1:7)')
d_12, d_13, d_14, d_15, d_16 = sp.symbols('d1(2:7)')
d_23, d_24, d_25, d_26 = sp.symbols('d2(3:7)')
d_34, d_35, d_36 = sp.symbols('d3(4:7)')
d_45, d_46 = sp.symbols('d4(5:7)')
d_56 = sp.symbols('d56')
d_test = sp.Matrix([[0, d_01, d_02, d_03, d_04, d_05, d_06],
                    [0, 0,    d_12, d_13, d_14, d_15, d_16], 
                    [0, 0,    0,    d_23, d_24, d_25, d_26],
                    [0, 0,    0,    0,    d_34, d_35, d_36],
                    [0, 0,    0,    0,    0,    d_45, d_46],
                    [0, 0,    0,    0,    0,    0,    d_56],
                    [0, 0,    0,    0,    0,    0,    0   ]])
d_test_1_goal = sp.Matrix([[0, d_03, d_06],
                           [0, 0,    d_36],
                           [0, 0,    0   ]])
d_test_2_goal = sp.Matrix([[0, d_03+d_01+d_02, d_06+d_04+d_05],
                           [0, 0,              d_36+d_34+d_35],
                           [0, 0,              0             ]])
d_test_3_goal = sp.Matrix([[0, d_03+d_01+d_02+d_13+d_23, d_06+d_04+d_05+d_16+d_26],
                           [0, 0,                        d_36+d_34+d_35+d_46+d_56],
                           [0, 0,                        0                       ]])
d_test_4_goal = sp.Matrix([[0, d_03+d_01+d_02+d_13+d_23+d_12, d_06+d_04+d_05+d_16+d_26+d_14+d_15+d_24+d_25],
                           [0, 0,                             d_36+d_34+d_35+d_46+d_56+d_45               ],
                           [0, 0,                             0                                           ]])

# COMPRESS DEMAND FUNCTION
def compress_demand(d, major_stations:list):
    """
    Take inputs:
        d: demand matrix,
        major_stations: list of major stations, inclusive of start/finish or not

    Return:
        new_d: new compressed demand matrix
    """
    rows, cols = d.shape
    if rows != cols:
        print("Rows and columns are different sizes")
        return None
    # Handle major stations list to include start and end stations (maybe?)
    sorted(major_stations)
    if major_stations[0] != 0:
        major_stations.insert(0, 0)
    if major_stations[-1] != cols - 1:
        major_stations.insert(len(major_stations), cols - 1)
    
    # n is the length of the new demand matrix
    n = len(major_stations)

    if n > 8:
        print("There can be at most 6 remote stations, currently there are {n-2}.")
        return

    # Create new demand matrix new_d
    new_d = sp.zeros(n, n)
    minor_stations = [station for station in range(major_stations[-1]) if station not in major_stations]
    for row in range(n):
        for col in range(n):
            if col > row:
                # List of code for loop

                # STEP 1
                new_d[row, col] += d[major_stations[row], major_stations[col]]

                # STEP 2
                for i in major_stations[:-1]:
                    for j in minor_stations:
                        if i < major_stations[row+1] \
                        and i >= major_stations[row] \
                        and j < major_stations[col] \
                        and j > major_stations[col-1] \
                        and i < j:
                            new_d[row, col] += d[i, j]

                # STEP 3
                for i in minor_stations:
                    if i < major_stations[row+1] \
                    and i > major_stations[row]:
                        j = major_stations[col]
                        new_d[row, col] += d[i, j]

                # STEP 4
                for i in minor_stations:
                    for j in minor_stations:
                        if i > major_stations[row] \
                        and i < major_stations[row+1] \
                        and j > major_stations[col-1] \
                        and j < major_stations[col] \
                        and i < j:
                            new_d[row, col] += d[i, j]
    return new_d

# FINAL ASSERT
assert compress_demand(d, [2]) == compress_demand(d, [0, 2]), "Failed Assertion 1"
assert compress_demand(d, [2]) == compress_demand(d, [0,2,4]) , "Failed Assertion 2"
assert compress_demand(d, [2]) == d_4_goal, "Failed Goal Assertion"
assert compress_demand(d_test, [3]) == d_test_4_goal, "Failed Goal Assertion 2"

# Testing new demands
sp.pprint(compress_demand(d,[2]))

sp.pprint(compress_demand(d_test, [3]))