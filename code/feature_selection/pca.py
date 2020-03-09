#pca.py		`			#20.03.02?
#hur.benjamin@mayo.edu
#
#Designed to perform pca for "full.ml.ready.txt"
#
#

import sys
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

data_profile = sys.argv[1]
data_df = pd.read_csv(data_profile, sep='\t', index_col=0, header=0)
#data_df = data_df.T
data_df_array = np.array(data_df)
pca = PCA(n_components = 3)
pca.fit(data_df_array)

print (pca)
print (pca.explained_variance_ratio_)


pca_results = pd.DataFrame(pca.components_, columns= data_df.columns,index = ['PC-1','PC-2','PC-3'])

print (pca_results)
