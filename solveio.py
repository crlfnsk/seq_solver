"""
Routines for file I/O:
"""

import os.path
import numpy as np


def read_input(inputdir):
    """Reads in the data for a given quantum system.

    Args:
        directory: Directory containing the file with the QM-system details.

    Returns:
        Value (mass, points, numberinterpolation) the mass,
        number of points in-between the x-limits
        and the number of interpolation points.
        Tuple ( )
        Array (xx, potential) the x-coordinates and the potential.
        String (InterpType) the type of interpolation.
    """
    inputfile = os.path.join(inputdir)
    input = open(inputfile, "r")
    seperatedinput = input.read().splitlines()
    mass = float(seperatedinput[0])
    xinfo = seperatedinput[1].split()
    xinfo = list(map(float, xinfo))
    eigenvalues = seperatedinput[2].split()
    eigenvalues = list(map(int, eigenvalues))
    interptype = str(seperatedinput[3])
    numinterp = float(seperatedinput[4])
    xandpot = np.empty((len(seperatedinput) - 5, 2), dtype=float)
    for ii in range(5, len(seperatedinput)):
        xxandpotentialunorganized = seperatedinput[ii].split()
        xandpot[ii - 5, 0] = xxandpotentialunorganized[0]
        xandpot[ii - 5, 1] = xxandpotentialunorganized[1]
    input.close()
    return mass, xinfo, eigenvalues, interptype, numinterp, xandpot


def write_output(energies, xx, wavefunc, expval, pot, inputdir):
    """Creates files of solver results.

    Args:
        arrays: energies, xx, wavefunc, expval
        xx dependent array: pot

    Returns:
        files: energies.dat, potential.dat, wavefuncs.dat, expvalues.dat
        potential.dat and wavefuncs.dat include xx in the first row.
        saves files into seq_solver directory for visualization.
    """
    np.savetxt("energies.dat", energies)
    solvedpot = np.empty((len(xx), 2), dtype=float)
    for ii in range(0, len(xx)):
        solvedpot[ii, 0] = xx[ii]
        solvedpot[ii, 1] = pot(xx[ii])
    np.savetxt("potential.dat", solvedpot)
    solvedwavefuncs = np.empty((len(xx), len(wavefunc[0]) + 1), dtype=float)
    for jj in range(0, len(xx)):
        solvedwavefuncs[jj, 0] = xx[jj]
        for kk in range(0, len(wavefunc[0])):
            solvedwavefuncs[jj, kk + 1] = wavefunc[jj, kk]
    np.savetxt("wavefuncs.dat", solvedwavefuncs)
    np.savetxt("expvalues.dat", expval)


def _read_testdata(filename):
    """ Reads refernce data fur unit testing.
    Args:
        filename (str): name of the reference file
    Returns:
        pot: array containing theinterpolated  potential
        expval: array containg the expected values

    """
    potpath = os.path.join(filename, ".pot")
    potpath = potpath.replace("/", "")
    potpath = os.path.join("testdata", potpath)
    expvalpath = os.path.join(filename, ".expval")
    expvalpath = expvalpath.replace("/", "")
    expvalpath = os.path.join("testdata", expvalpath)
    energypath = os.path.join(filename, ".energy")
    energypath = energypath.replace("/", "")
    energypath = os.path.join("testdata", energypath)
    pot = np.loadtxt(potpath)[:, 1]
    expval = np.loadtxt(expvalpath)
    energy = np.loadtxt(energypath)
    return pot, expval, energy

# _read_testdata("double_well_lin")
