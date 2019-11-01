"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function

################################
#
# # original code was returning file not found error for files clearly present in this folder
# # think we have atom running the code from D:\Dropbox\Dropbox\GitHub\ThinkStats2 rather than ...\code
# # confirmatory test as follows proved this:
import os
# print(os.getcwd())
#
# # workaround, probably needed for all these codes
os.chdir('D:\Dropbox\Dropbox\GitHub\ThinkStats2\code')
# print(os.getcwd())

# ###############################

import numpy as np
import sys

import nsfg
import first
import thinkstats2
import thinkplot
import pandas as pd

#### EXERCISES ####

# EXERCISE 3.1 is on the .ipynb for this chapter

# EXERCISE 3.2: Write functions called PmfMean and PmfVar that take a Pmf object and compute the mean and variance. To test these methods, check that they are consistent with the methods Mean and Var provided by Pmf.

# get a test Pmf object (similar to a dictionary, with keys and values)
live, firsts, others = first.MakeFrames()
prglngth = live.prglngth
pmf = thinkstats2.Pmf(prglngth)

pmf

def PmfMean(pmf):
    # given a Pmf object, returns the mean

    mean = 0
    for key, val in pmf.Items(): # Items() is like items() for dictionaries, but for Pmfs
        mean += (key * val)

    return mean

PmfMean(pmf) == pmf.Mean() # True

def PmfVar(pmf):
    # given a Pmf object, returns the variance
    # assumes PmfMean already defined

    variance = 0
    mean = PmfMean(pmf)

    for key, val in pmf.Items():
        square = (key - mean)**2
        product = val * square
        variance += product

    return variance

PmfVar(pmf) == pmf.Var() # True

# EXERCISES 3.3 and 3.4 are on the .ipynb for this chapter

def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    live, firsts, others = first.MakeFrames()
    # PairWiseDifferences(live)

    # test PmfMean and PmfVar
    prglngth = live.prglngth
    pmf = thinkstats2.Pmf(prglngth)
    mean = PmfMean(pmf)
    var = PmfVar(pmf)

    assert(mean == pmf.Mean())
    assert(var == pmf.Var())
    print('mean/var preg length', mean, var)

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
