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
# import os
# print(os.getcwd())
#
# # workaround, probably needed for all these codes
# os.chdir('D:\Dropbox\Dropbox\GitHub\ThinkStats2\code')
#
# ###############################

import sys
from operator import itemgetter

import first
import thinkstats2
import pandas as pd
import numpy as np
import nsfg

################################################### EXERCISES ######################################################################

# 2.1: Based on the results in this chapter, suppose you were asked to summarize what you learned about whether first babies arrive late. Which summary statistics would you use if you wanted to get a story on the evening news? Which ones would you use if you wanted to reassure an anxious patient?

# To get a story on the evening news, you (unethically) would make the effect size seem bigger, by showing the histogram of pregnancy lengths that does not take into account sample size differences
# Even then, there isn't a huge difference - and any of the summary statistics would show this...
# To reassure an anxious woman that there is not much of a difference, the Cohen's d (effect size) of 0.029 standard deviations would suit, assuming you highlight the std. dev. of 2.7 weeks for all live births

# 2.1.b: Finally, imagine that you are Cecil Adams, author of The Straight Dope (http://straightdope.com), and your job is to answer the question, "Do first babies arrive late?" Write a paragraph that uses the results in this chapter to answer the question clearly, precisely, and honestly.

# The mean pregnancy length for first babies is 38.601 weeks, and for further babies it is 38.523 weeks. That's a difference of 0.078 weeks, or about 13 hours (~ 0.2%), so very small. Additionally, in comparing the variability in pregnancy lengths between babies in each group, the Cohen's d test shows a difference in means of 0.029 standard deviations - also extremely small. As such, we can safely say that there is almost no difference in pregnancy length depending on baby number, as such a tiny difference is very likely due to sample size, and would get averaged out with more testing.

# 2.2: is on the jupyter notebook

# 2.3: - define Mode(hist) and ALlModes(hist), below

# 2.4: is also on the jupyter notebook

def Mode(hist):
    """Returns the value with the highest frequency.

    hist: Hist object

    returns: value from Hist
    """
    hist_list = list(hist.Items())
    sorted_list = sorted(hist_list, key = lambda x: x[1], reverse = True)

    return sorted_list[0][0]

def AllModes(hist):
    """Returns value-freq pairs in decreasing order of frequency.

    hist: Hist object

    returns: iterator of value-freq pairs
    """
    hist_list = list(hist.Items())
    sorted_list = sorted(hist_list, key = lambda x: x[1], reverse = True)

    return sorted_list

def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    live, firsts, others = first.MakeFrames()
    hist = thinkstats2.Hist(live.prglngth)

    # test Mode
    mode = Mode(hist)
    print('Mode of preg length', mode)
    assert mode == 39, mode

    # test AllModes
    modes = AllModes(hist)
    assert modes[0][1] == 4693, modes[0][1]

    for value, freq in modes[:5]:
        print(value, freq)

    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)















#
