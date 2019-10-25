"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function

import numpy as np
import sys
import pandas as pd

################################

# original code was returning file not found error for files clearly present in this folder
# think we have atom running the code from D:\Dropbox\Dropbox\GitHub\ThinkStats2 rather than ...\code
# confirmatory test as follows proved this:
import os
# print(os.getcwd())

# workaround, probably needed for all these codes
os.chdir('D:\Dropbox\Dropbox\GitHub\ThinkStats2\code')

###############################

import nsfg
import thinkstats2


def main(script):
    """Tests the functions in this module.

    script: string script name
    """
    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)

################## EXERCISE 1.2 ####################
# In the repository you downloaded, you should find a file named chap01ex.py; using this file as a starting place, write a function that reads the respondent file, 2002FemResp.dat.gz.

# respondent data is in the file 2002FemResp.dat.gz, it's a gzip-compressed file in plain text with fixed width columns
# format of the file is stored in 2002FemResp.dct, a stata dictionary file containing a list of the variable names, types, and indices identifying where to find them

# thinkstats2.py contains defined classes, and functions for them, that interpret these file types, such as:
# ReadStataDct, for reading in the .dct file
# ReadFixedWidth, for reading in the .dat file, using the .dct file to interpret its format
## the latter is a function defined for the class FixedWidthVariables defined in thinkstats2.py, based on pandas.read_fwf()

# The way to use them is presumably similar to that for ReadFemPreg, as shown in chapter 1.3

def ReadFemResp(dct_file='2002FemResp.dct', dat_file='2002FemResp.dat.gz'):
    dct = thinkstats2.ReadStataDct(dct_file)
    df = dct.ReadFixedWidth(dat_file, compression='gzip')
    return df

resp = ReadFemResp()

resp.head() # seems to work?

# The variable pregnum is a recode that indicates how many times each respondent has been pregnant. Print the value counts for this variable and compare them to the published results in the NSFG codebook.

# found codebook data at https://www.icpsr.umich.edu/nsfg6/Controller?displayPage=labelDetails&fileCode=FEM&section=R&subSec=7869&srtLabel=606835

resp.pregnum.value_counts().sort_index()

# codebook collects 7 or more pregnancies as one entry
resp.pregnum.value_counts()[7:].sum() # equals 158

# our imported data does match the codebook data

# You can also cross-validate the respondent and pregnancy files by comparing pregnum for each respondent with the number of records in the pregnancy file.

resp.pregnum.sum() # 13593 total pregnancies in resp file
preg = nsfg.ReadFemPreg()
preg.shape # 13593 total pregnancies (rows) in preg file, matches resp file

# You can use nsfg.MakePregMap to make a dictionary that maps from each caseid to a list of indices into the pregnancy DataFrame.

preg_map = nsfg.MakePregMap(preg)

############# EXERCISE 1.3 ################

# The best way to learn about statistics is to work on a project you are interested in. Is there a question like, "Do first babies arrive late?" that you want to investigate?
# Think about questions you find personally interesting, or items of conventional wisdom, or controversial topics, or questions that have political consequences, and see if you can formulate a question that lends itself to statistical inquiry.

# Had a brief look through the respondent codebook for controversial variables
# People often say that immigrants and religious people have more babies. Is that actually true, or is it made up (perhaps for political purposes)? How big is the difference, if there is one?
# To be exact in terms of what we can get from this dataset, are higher numbers of pregnancies per woman linked to their religion or place of birth?
# - obviously we cannot tell from this dataset whether political reasons may be involved in the public perception of this politically charged statistic -

# relevant variable names are preg.pregnum, resp.brnout, and resp.relcurr
# preg.pregnum is number of pregnancies, value matches actual number of pregnancies
# resp.brnout is 1 for born outside US, 5 for born in the US, 8 for refused to answer, and 9 for don't know
# resp.relcurr is 1 for no religion, 2-7 for various christian sects, 8 for non-christian religion, 98 for refused, and 99 for don't know
# probably want to drop the entries for refused to answer, and don't know

# extract caseids of resps born out/inside the US
born_out = resp.caseid[resp.brnout == 1]
born_in = resp.caseid[resp.brnout == 5]

# extract caseids of resps based on religion
# will, for the sake of simplicity in this exercise, collect the various christian sects as one (this is an assumption on behaviour you would not make in a serious investigation...)
no_rel = resp.caseid[resp.relcurr == 1]
christ_rel = resp[resp.relcurr >= 2]
christ_rel = christ_rel.caseid[christ_rel.relcurr <= 7]
non_christ_rel = resp.caseid[resp.relcurr == 8]

# compare these caseids with pregnum in preg for total number of pregnancies

def preg_count(caseids_list):
    # given a list of caseids, this function returns a pandas Series containing the number of respondents who had certain numbers of pregnancies

    pregnancies_list = []
    for i in caseids_list:
        pregnancies_list.append(len(preg.pregnum[preg.caseid == i].values))

    pregnancies_series = pd.Series(pregnancies_list)

    return pregnancies_series.value_counts()

born_out_preg = preg_count(born_out)
born_in_preg = preg_count(born_in)
no_rel_preg = preg_count(no_rel)
christ_rel_preg = preg_count(christ_rel)
non_christ_rel_preg = preg_count(non_christ_rel)

# combine results into one DataFrame
frames = [born_out_preg, born_in_preg, no_rel_preg, christ_rel_preg, non_christ_rel_preg]
preg_frame = pd.concat(frames, axis = 1).rename({0: 'Born Out', 1: 'Born in', 2: 'No Rel.', 3: 'Christ.', 4: 'Non Christ.'}, axis = 1)

preg_frame # number of respondents who had different numbers of pregnancies (index), separated by religion and birth location

# unsure why one column is dtype int and the rest float... must be in the raw data as were treated the same way here


preg_frame.sum()

# convert results to a percentage of overall respondents for that group
prob_frame = preg_frame.divide(preg_frame.sum()).multiply(100)
prob_frame

# if wanted to, could analyse further by combining the tests for religion and birth location (eg. non-religious born in US vs outside) - didn't here for sake of simplicity

# either way, there is a lot to unpack in these results, as a quick summary:

# roughly 9% more respondents born in the US have never been pregnant compared to immigrants
# approx. 3-5% more respondents born outside the US had 2-3 pregnancies compared to those born within
# this increase mostly accounted for the prior difference, as the relative probabilties for 1 pregnancy, as well as for 4+, were very similar (< 1%) regardless of birth location

# for religion, non christian religious respondents were the least likely to have pregnancies
# christian religious respondents were the most likely, with a ~ 9% decrease in zero-pregnancy respondents compared to non-christian religious, and a ~ 5% decrease compared to non-religious
# non religious respondents were the most likely to have only one pregnancy, by 2-4%.

# christian religious respondents tended towards having the most numbers of pregnancies - which goes against the narrative!
