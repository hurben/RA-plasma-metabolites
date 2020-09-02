#!/usr/bin/env python
# coding: utf-8

# In[48]:

import pandas as pd
from scipy import stats
import seaborn as sns
from pylab import savefig
import matplotlib.pyplot as plt
import math

data_file = '/Users/m221138/RA_plasma_metabolites/data/51_features_dataprofile.csv'
data_df = pd.read_csv(data_file)
r, c = data_df.shape


# In[17]:

chem_interest_list = ['bilirubin (E,E)*', 'linolenoylcarnitine (C18:3)*']
for i in range(1, r):

	das28_list = list(data_df.iloc[0,1:])
	chem_name = data_df.iloc[i,0]

	if chem_name in chem_interest_list:
		chem_list = list(data_df.iloc[i,1:])
		output_pdf = '%s%s.pdf' % ('/Users/m221138/RA_plasma_metabolites/code/figures/', chem_name)
		print (output_pdf)
		corr, pvalue = stats.spearmanr(chem_list, das28_list)

		#confidence interval
		num_observe = c
		r = corr
		stderr = 1.0 / math.sqrt(num_observe - 3)
		delta = 1.96 * (stderr)
		lower = math.tanh(math.atanh(r) - delta)
		upper = math.tanh(math.atanh(r) + delta)
		print ("lower %.6f upper %.6f" % (lower, upper))

		print (pvalue)

		
		output_plot = sns.regplot(chem_list, das28_list)
		output_plot.set(ylabel='DAS28', xlabel='Scaled Chemical Abundance')
		output_plot.set_title('%s\n corr: %s pval: %s\n %s ~ %s' % (chem_name ,round(corr,3), round(pvalue, 5), round(lower, 5), round(upper,5)))
		output_plot.get_figure()
		output_plot.figure.savefig(output_pdf)
		output_plot.get_figure().clf()



# In[ ]:




