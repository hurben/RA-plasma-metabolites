#ALL_IN_ONE_FeatureSelection_CV_LOO_label.py						20.03.16
#hur.benjamin@mayo.edu
#
#This script is inherited from "ALL_IN_ONE_FeatureSelection_CV_LOO.py"
#
#**Assuming the feature selection if done by "ALL_IN_ONE_FeatureSelection_CV_LOO.py"
#
#[1] Performance measuring with trainging set (splitted 64 times)
#
#[2] final model
#	use every dataset
#	feature selection
#	measure performance
#
#[3] Plot things....



def labeling_das28score(das28_df, label_number):

	r = das28_df.shape[0]
	labelized_list = []

	for i in range(r):
		das28 = das28_df.iloc[i]

		if label_number == 2:
			if das28 < 2.6:
				label = 'R'
			else:
				label = 'notR'

		if label_number == 3:
			if das28 <= 3.2:
				label = 'L'
			if das28 > 3.2 and das28 <= 5.1:
				label = 'M'
			if das28 > 5.1:
				label = 'H'

		if label_number == 4:
			if das28 < 2.6:
				label = 'R'
			if das28 >= 2.6 and das28 <= 3.2:
				label = 'L'
			if das28 > 3.2 and das28 <= 5.1:
				label = 'M'
			if das28 > 5.1:
				label = 'H'
		labelized_list.append(label)
	return labelized_list

def performance_dict_to_text(performance_dict, output_txt, model_str_list, folder_list, label_num_list):
	
	output_txt = open(output_txt,'w')

	output_txt.write('data\tnum_of_labels\tmodel\tacc\n')
	for folder_idx in folder_list:
		for label_num_idx in label_num_list:
			for model_str_idx in model_str_list:
				acc = performance_dict[model_str_idx, folder_idx, label_num_idx]
				output_txt.write('%s\t%s\t%s\t%s\n' % (folder_idx, label_num_idx, model_str_idx, acc))

	output_txt.close()

if __name__ == '__main__':

	import sys
	sys.path.insert(1, '/Users/m221138/RA_project/code/machine_learning_r2')
	sys.path.insert(1,'/Users/m221138/RA_project/code')
	sys.path.insert(1, '/Users/m221138/RA_project/code/feature_selection')
	import os
	import FL
	import MLFL_CV
	import MLFL_main
	import MLFL_plots
	import MLFL_validation
	import LINEAR_MODEL_FL as LMFL
	import numpy as np
	import statistics
	from sklearn import metrics

	#MANUAL INFORMATION REQUIRED
	file_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix', 'hd4_qc_matrix']
	summary_folder = 'fs_summary'
	data_splits = 64

	#DEBUG Thresholds
	#1 = skip process
	#0 = Do process

	#Testing the performance of "Feature selection" (sample size 128 = patients 64)
	#Model will use 126 samples to create a model
	#Model will predict DAS28 score using 2 samples
	#Repeating this 64 times
	skip_model_performance = 0

	#Testing the performance of "Feature selection" with full dataset (sample size 140 = patients 76)
	#Model will use 128 samples to create a model
	#Model will predict DAS28 score using 12 samples
	skip_final_model_performance = 1
	
	#MANUAL INFORMATION REQUIRED
	ml_ready_folders = ['hd4_only','clp_only','hd4_clp', 'clp_fac_only','clp_sc_only', 'hd4_full', 'clp_fac_full', 'clp_sc_full', 'clp_lc_full', 'clp_only_full','hd4_clp_full']

	#from sklearn.linear_model import LinearRegression
	from sklearn.ensemble import RandomForestClassifier
	from sklearn.linear_model import LogisticRegression
	from sklearn.svm import SVC
	import warnings
	warnings.filterwarnings("ignore")
	rf = RandomForestClassifier()
	logr = LogisticRegression()
	svm = SVC()

	training_performance_dict = {}
	final_performance_dict = {}

	model_list = [rf, logr, svm]
	model_str_list = ['rf', 'logr', 'svm']


	if skip_model_performance == 0:

		for i in range(len(model_list)):
			model_idx = model_list[i]
			model_str = model_str_list[i]

			label_list = [2,3,4]

			for folder in ml_ready_folders:
				print (">>> %s" % folder)
				ml_result_folder = '%s' % folder

				if os.path.isdir(ml_result_folder) == True:
					os.system('rm -r %s' % ml_result_folder)
					os.system('mkdir %s' % ml_result_folder)
				else:
					os.system('mkdir %s' % ml_result_folder)

				for label_num in label_list:

					y_test_list = []
					y_predict_list = []

					for index in range(1, data_splits + 1):
						ml_ready_file = '../%s/%s.ml.ready.txt' % (folder, index)
						ml_ready_test_file = '../%s/%s.ml.ready.test.txt' % (folder, index)

						X_train, y_train = MLFL_CV.cross_validation().get_X_y(ml_ready_file)
						y_train = labeling_das28score(y_train, label_num)
						X_test, y_test = MLFL_CV.cross_validation().get_test_X_y(ml_ready_test_file)
						y_test = labeling_das28score(y_test, label_num)

						X_train = np.array(X_train)
						y_train = np.array(y_train)
						X_test = np.array(X_test)
						y_test = np.array(y_test)

						clf = model_idx
						pred_y = MLFL_CV.cross_validation().model_learning_and_prediction_vlabel(clf, X_train, y_train, X_test, y_test)

						for element in pred_y:
							y_predict_list.append(element)
						for element in y_test:
							y_test_list.append(element)

					acc = metrics.accuracy_score(y_test_list, y_predict_list)

					print ('----------------------------')
					print (model_str)
					print ('Number of Labels: %s' % label_num)
					print ('%s' % folder)
					print ('DataSplits: %s' % data_splits)
					print ('acc : %s' % acc)
					print ('Observation : %s' % y_test_list)
					print ('Prediction : %s' % y_predict_list)
					print ('----------------------------')
					training_performance_dict[model_str, folder, label_num] = acc


		performance_dict_to_text(training_performance_dict, '/Users/m221138/RA_project/analysis/all_in_one_r2/analysis_with_labels/training.performance.txt', model_str_list, ml_ready_folders, label_list)

	ml_ready_folders = ['clp_only','hd4_only','hd4_clp', 'clp_fac_only','clp_sc_only', 'hd4_full', 'clp_fac_full', 'clp_sc_full', 'clp_lc_full', 'clp_only_full','hd4_clp_full']

	if skip_final_model_performance == 0:

		for i in range(len(model_list)):
			model_idx = model_list[i]
			model_str = model_str_list[i]
			label_list = [2,3,4]

			for folder in ml_ready_folders:
				print ("Final Model Validation > %s" % folder)

				ml_ready_file = '../%s/full.ml.ready.txt' % (folder)
				ml_ready_test_file = '../%s/full.ml.ready.test.txt' % (folder)

				for label_num in label_list:

					X_train, y_train = MLFL_CV.cross_validation().get_X_y(ml_ready_file)
					y_train = labeling_das28score(y_train, label_num)
					X_test, y_test = MLFL_CV.cross_validation().get_test_X_y(ml_ready_test_file)
					y_test = labeling_das28score(y_test, label_num)

					X_train = np.array(X_train)
					y_train = np.array(y_train)
					X_test = np.array(X_test)
					y_test = np.array(y_test)

					clf = model_idx
					pred_y = MLFL_CV.cross_validation().model_learning_and_prediction_vlabel(clf, X_train, y_train, X_test, y_test)

					acc = metrics.accuracy_score(y_test, pred_y)

					print ('----------------------------')
					print (model_str)
					print ('Number of Labels: %s' % label_num)
					print ('%s' % folder)
					print ('acc : %s' % acc)
					print ("Observation: %s" % y_test)
					print ("Prediction: %s" % pred_y)
					print ('----------------------------')
					final_performance_dict[model_str, folder, label_num] = acc

		performance_dict_to_text(final_performance_dict, '/Users/m221138/RA_project/analysis/all_in_one_r2/analysis_with_labels/final.performance.txt', model_str_list, ml_ready_folders, label_list)



else:
	None
