# running inline with hydrogen in atom

import os

# change dir
os.chdir('D:\Dropbox\Dropbox\GitHub\ThinkStats2\code')

# import custom packages from dir
import nsfg

df = nsfg.ReadFemPreg()
df

df.columns

df.columns[1]

pregordr = df['pregordr']
type(pregordr)

pregordr

pregordr[0]
pregordr[2:5]

df.birthwgt_lb.value_counts().sort_index()

# number of birth weights under 6 lb
df.birthwgt_lb.value_counts().sort_index()[:5].sum()

# number of birth weights over 9 lb
df.birthwgt_lb.value_counts().sort_index()[9:].sum()

# return series of df.birthwgt_lb where the only rows shown are those where the birthwgt_lb is less than or equal to 5
df.loc[df.birthwgt_lb <= 5, 'birthwgt_lb']

# MakePregMap collects all of the pregnancies for each respondent (df.caseid is the respondent id, df.index is the pregnancy)
test = nsfg.MakePregMap(df)
# it is stored as a dictionary mapping each caseid to a list of indices (pregnancies)

# example, caseid 2 had 3 pregnancies
test[6]
df[df.caseid == 6]

# look up a particular respondent and print the list of outcomes for all of her pregnancies
caseid = 10229
preg_map = nsfg.MakePregMap(df)
indices = preg_map[caseid]
df.outcome[indices].values
# 4 represents miscarriages, 1 a live birth











































#
