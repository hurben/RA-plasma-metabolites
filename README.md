Plasma Metabolomic Profiling in Patients with Rheumatoid Arthritis Identifies Biochemical Features Indicative of Disease Activity
=========================

DOI : TBD

Benjamin Hur, Kerry A. Wright, Vinod K. Gupta, Harvey Huang, Kenneth J. Warrington, Veena Taneja, John M. Davis III, and Jaeyun Sung

Contact: hur.benjamin@mayo.edu
Corresponding Author : sung.jaeyun@mayo.edu


##### 1. Differentially Abundant metabolites

>code/linear_model_r1/MLR_R_categorical_diff_2class_v2.r

>analysis/differential_abundance_v2/2class_v2/run.sh

##### 2. Feature selection for quantitative disease activity of RA

>code/machine_learning_r7/All_IN_ONE_FeatureSelection_CV_LOO.py

>analysis/selection_scheme_r7/run.sh

##### 3. Other statistics

Investigation of drugs (csDMARD, TNFi-bDMARD, non-TNFi-bDMARD, MTX, PRED) that affected the abundance of metabolites.
>code/statistics/drug_effect_lmer_R.ipynb

Differentially abundant metabolites specific test; confounding effect (drug, smoke, age, etc) difference between higher and lower disease activity.
>code/statistics/ftest_comfounds.ipynb

Investigation of prescription (csDMARD, TNFi-bDMARD, non-TNFi-bDMARD, MTX, PRED) differences between visit 1 and visit 2.
>code/statistics/mcnemar_test_R.ipynb


#### DATA

preprocessed data: Training datset (n=128)
>data/filled_qc_data

preprocessed data: Test dataset (n=12)
>data/filled_qc_data_nan/

