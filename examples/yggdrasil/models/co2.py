import argparse
import numpy as np


def calculate_concentration(doy, dist, height, offset=60.0):
    r"""Function that calculates the concentration of CO2.

    Args:
        doy (float): Day of year.
        dist (float): Distance from the plant in cm.
        height (float): Distance from the ground in cm.
        offset (float, optional): Offset in the year in days. Defaults to 60.

    Returns:
        float: CO2 concentration in cm^-3

    """
    return np.sin(2.0 * np.pi * (doy + offset) / 365) / (dist * dist * height)


# Parse command-line arguments
parser = argparse.ArgumentParser("Calculate the co2 concentration at a given distance from a plant.")
parser.add_argument('dist', help='Distance from the plant (cm)', type=float)
parser.add_argument('height', help='Distance from the ground (cm)', type=float)
parser.add_argument('doy', help='Day of year', type=float)
args = parser.parse_args()
dist = args.dist
height = args.height
doy = args.doy
offset = 60.0

# Compute concentration
conc = calculate_concentration(doy, dist, height, offset=offset)
print('Concentration', conc)
