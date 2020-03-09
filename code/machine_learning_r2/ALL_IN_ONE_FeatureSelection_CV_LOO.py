#ALL_IN_ONE_FeatureSelection_CV_LOO.py						20.02.07
#hur.benjamin@mayo.edu
#
#Do every process at once.
#
#[1] From the dataset of interest (i.e hd4, clp_only, clp_sc.... etc)
#    Divide each dataset into 64 data points (using it for CV)
#    at each data folder, we will have 64 subsets of training set, test set
#[2] feature selection 
#	while i <= 64
#		run mixed effect linear model
#		create GLM with the significant features
#		(note: each iterations might have different set of features)
#		summarize multiple significant features if the iteration contains multiple condition(i.e clp_only: clp_sc + clp_fac + clp_lc)
#		measure performance
#
#[3] final model
#	use every dataset
#	feature selection
#	measure performance
#
#[4] Plot things....


def preprocess (file_name, do_lmer, do_feature_selection):

	data_profile = MLFL_main.access_data().get_dir(file_name)
	
	#run R for those seperated files
	if do_lmer == 1:
		#create folder to store
		MLFL_main.feature_selection().do_lmer(file_name, data_profile)

	if do_feature_selection == 1:
		MLFL_main.feature_selection().extract_sig_features(file_name)

			
def summarize_features(fs_summary_folder):

	if os.path.isdir(fs_summary_folder) == True:
		os.system('rm -r %s' % fs_summary_folder)
		os.system('mkdir %s' % fs_summary_folder)
	else:
		os.system('mkdir %s' % fs_summary_folder)

	hd4_dir = './hd4_qc_matrix/feature_selection'
	clp_fac_dir = './clp_fac_qc_matrix/feature_selection'
	clp_sc_dir = './clp_sc_qc_matrix/feature_selection'
	clp_lc_dir = './clp_lc_qc_matrix/feature_selection'

	clp_only_list = [clp_fac_dir, clp_sc_dir, clp_lc_dir]
	integrate_features(fs_summary_folder, clp_only_list, 'clp_only', 64)

	clp_hd4_list = [clp_fac_dir, clp_sc_dir, clp_lc_dir, hd4_dir]
	integrate_features(fs_summary_folder, clp_hd4_list, 'clp_hd4', 64)

	hd4_only_list = [hd4_dir]
	integrate_features(fs_summary_folder, hd4_only_list, 'hd4_only', 64)


def integrate_features(fs_summary_folder, file_list, fs_choice, file_splits):
	
	for i in range(1, file_splits + 1):
		for ith_file in file_list:
			cmd = 'cat %s/%s.lmer.out.sig.features >> ./%s/%s.%s.fs' % (ith_file, i, fs_summary_folder, i, fs_choice)
			os.system(cmd)

def preprocess_full_dataset (file_name, do_lmer, do_feature_selection):

	data_profile = MLFL_main.access_data().get_dir(file_name)
	
	#run R for those seperated files
	if do_lmer == 1:
		#create folder to store
		MLFL_validation.do_lmer_full_dataset(file_name, data_profile)

	if do_feature_selection == 1:
		MLFL_validation.extract_sig_features_full_dataset(file_name)


if __name__ == '__main__':

	import sys
	sys.path.insert(1, '../code/machine_learning_r2/')
	sys.path.insert(1,'../code')
	sys.path.insert(1, '../code/feature_selection')
	import os
	import FL
	import MLFL_CV
	import MLFL_main
	import MLFL_plots
	import MLFL_validation
	import LINEAR_MODEL_FL as LMFL
	import numpy as np
	import statistics

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
	skip_preprocess = 0
	skip_2nd_preprocess = 0
	skip_model_performance = 0

	#Testing the performance of "Feature selection" with full dataset (sample size 140 = patients 76)
	#Model will use 128 samples to create a model
	#Model will predict DAS28 score using 12 samples
	skip_full_model_preprocess = 0
	skip_full_model_2nd_preprocess = 0
	skip_final_model_performance = 0
	
	if skip_preprocess == 0:

		for file_name in file_list:
			print  ("Preprocess to feature selection step #1  > %s" % file_name)
			preprocess(file_name, 1, 1)
		summarize_features(summary_folder)

	if skip_2nd_preprocess == 0:

		#with feature selection
		clp_only_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(clp_only_list, 'clp_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(clp_only_list, 'clp_only', data_splits)

		clp_only_list = ['clp_fac_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(clp_only_list, 'clp_fac_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(clp_only_list, 'clp_fac_only', data_splits)

		clp_only_list = ['clp_lc_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(clp_only_list, 'clp_lc_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(clp_only_list, 'clp_lc_only', data_splits)

		clp_only_list = ['clp_sc_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(clp_only_list, 'clp_sc_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(clp_only_list, 'clp_sc_only', data_splits)

		hd4_only_list = ['hd4_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(hd4_only_list, 'hd4_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(hd4_only_list, 'hd4_only', data_splits)

		hd4_clp_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix', 'hd4_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(hd4_clp_list, 'hd4_clp', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(hd4_clp_list, 'hd4_clp', data_splits)

		#without feature selection
		clp_only_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection_v2(clp_only_list, 'clp_only_full', data_splits)
		clp_only_list = ['clp_fac_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection_v2(clp_only_list, 'clp_fac_full', data_splits)
		clp_only_list = ['clp_sc_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection_v2(clp_only_list, 'clp_sc_full', data_splits)
		clp_only_list = ['clp_lc_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection_v2(clp_only_list, 'clp_lc_full', data_splits)

		hd4_only_list = ['hd4_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection_v2(hd4_only_list, 'hd4_full', data_splits)

		hd4_clp_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix', 'hd4_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection_v2(hd4_clp_list, 'hd4_clp_full', data_splits)

	#MANUAL INFORMATION REQUIRED
	ml_ready_folders = ['clp_only','hd4_only','hd4_clp', 'clp_fac_only','clp_sc_only', 'hd4_full', 'clp_fac_full', 'clp_sc_full', 'clp_lc_full', 'clp_only_full','hd4_clp_full']

	from sklearn.linear_model import LinearRegression

	if skip_model_performance == 0:

		loo_cv_dict = {}

		for folder in ml_ready_folders:
			ml_result_folder = '%s/ml_results' % folder

			loo_cv_mae_list = []

			if os.path.isdir(ml_result_folder) == True:
				os.system('rm -r %s' % ml_result_folder)
				os.system('mkdir %s' % ml_result_folder)
			else:
				os.system('mkdir %s' % ml_result_folder)

			for index in range(1, data_splits + 1):
				ml_ready_file = '%s/%s.ml.ready.txt' % (folder, index)
				ml_ready_test_file = '%s/%s.ml.ready.test.txt' % (folder, index)

				X_train, y_train = MLFL_CV.cross_validation().get_X_y(ml_ready_file)
				X_test, y_test = MLFL_CV.cross_validation().get_test_X_y(ml_ready_test_file)

				X_train = np.array(X_train)
				y_train = np.array(y_train)
				X_test = np.array(X_test)
				y_test = np.array(y_test)

				lr = LinearRegression()
				data_point_for_plot_dict, loo_cv_mae, loo_MAE_list = MLFL_CV.cross_validation().model_learning_and_prediction(lr, X_train, y_train, X_test, y_test)
				loo_cv_mae_list.append(loo_cv_mae)
				
			loo_cv_dict[folder] = loo_cv_mae_list
			print ('----------------------------')
			print ('%s' % folder)
			print ('DataSplits: %s' % data_splits)
			print ('means of MAE: %s' % statistics.mean(loo_cv_mae_list))
			print ('stdvs of MAE: %s' % statistics.stdev(loo_cv_mae_list))
			print ('----------------------------')

		MLFL_plots.plots().plot_loo_mae_variance_plot(loo_cv_dict, './mae.summary.pdf', "Indexs of test data", "Mean Absolute Error")


	if skip_full_model_preprocess == 0:
		for file_name in file_list:
			print  ("Preprocess [full dataset] to feature selection step #1  > %s" % file_name)
			preprocess_full_dataset(file_name, 1, 1)

	if skip_full_model_2nd_preprocess == 0:

		#with feature selection
		hd4_only_list = ['hd4_qc_matrix']
		hd4_test_only_list = ['hd4_qc_nan_matrix']
		MLFL_validation.create_full_model_ready_matrix(hd4_only_list, 'hd4_only', hd4_test_only_list)

		clp_only_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix']
		clp_test_only_list = ['clp_fac_qc_nan_matrix', 'clp_lc_qc_nan_matrix', 'clp_sc_qc_nan_matrix']
		MLFL_validation.create_full_model_ready_matrix(clp_only_list, 'clp_only', clp_test_only_list)

		clp_only_list = ['clp_fac_qc_matrix']
		clp_test_only_list = ['clp_fac_qc_nan_matrix']
		MLFL_validation.create_full_model_ready_matrix(clp_only_list, 'clp_fac_only', clp_test_only_list)

		clp_only_list = ['clp_lc_qc_matrix']
		clp_test_only_list = ['clp_lc_qc_nan_matrix']
		MLFL_validation.create_full_model_ready_matrix(clp_only_list, 'clp_lc_only', clp_test_only_list)

		clp_only_list = ['clp_sc_qc_matrix']
		clp_test_only_list = ['clp_sc_qc_nan_matrix']
		MLFL_validation.create_full_model_ready_matrix(clp_only_list, 'clp_sc_only', clp_test_only_list)

		hd4_clp_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix', 'hd4_qc_matrix']
		clp_test_only_list = ['clp_fac_qc_nan_matrix', 'clp_lc_qc_nan_matrix', 'clp_sc_qc_nan_matrix', 'hd4_qc_nan_matrix']
		MLFL_validation.create_full_model_ready_matrix(hd4_clp_list, 'hd4_clp', clp_test_only_list)

		#without feature selection
		clp_only_list = ['clp_fac_qc_matrix']
		clp_test_only_list = ['clp_fac_qc_nan_matrix']
		MLFL_validation.full_data_full_feature_selection(clp_only_list, 'clp_fac_full', clp_test_only_list)

		clp_only_list = ['clp_sc_qc_matrix']
		clp_test_only_list = ['clp_sc_qc_nan_matrix']
		MLFL_validation.full_data_full_feature_selection(clp_only_list, 'clp_sc_full', clp_test_only_list)

		clp_only_list = ['clp_lc_qc_matrix']
		clp_test_only_list = ['clp_lc_qc_nan_matrix']
		MLFL_validation.full_data_full_feature_selection(clp_only_list, 'clp_lc_full', clp_test_only_list)

		hd4_only_list = ['hd4_qc_matrix']
		hd4_test_only_list = ['hd4_qc_nan_matrix']
		MLFL_validation.full_data_full_feature_selection(hd4_only_list, 'hd4_full', hd4_test_only_list)

		clp_only_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix']
		clp_test_only_list = ['clp_fac_qc_nan_matrix', 'clp_lc_qc_nan_matrix', 'clp_sc_qc_nan_matrix']
		MLFL_validation.full_data_full_feature_selection(clp_only_list, 'clp_only_full', clp_test_only_list)

		hd4_clp_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix', 'hd4_qc_matrix']
		hd4_clp_test_list = ['clp_fac_qc_nan_matrix', 'clp_lc_qc_nan_matrix', 'clp_sc_qc_nan_matrix', 'hd4_qc_nan_matrix']
		MLFL_validation.full_data_full_feature_selection(hd4_clp_list, 'hd4_clp_full', hd4_clp_test_list)


	ml_ready_folders = ['clp_only','hd4_only','hd4_clp', 'clp_fac_only','clp_sc_only', 'hd4_full', 'clp_fac_full', 'clp_sc_full', 'clp_lc_full', 'clp_only_full','hd4_clp_full']

	if skip_final_model_performance == 0:
		final_model_dict = {}

		for folder in ml_ready_folders:
			print ("Final Model Validation > %s" % folder)
			#ml_result_folder = '%s/ml_results' % folder

			loo_cv_mae_list = []

			ml_ready_file = '%s/full.ml.ready.txt' % (folder)
			ml_ready_test_file = '%s/full.ml.ready.test.txt' % (folder)

			X_train, y_train = MLFL_CV.cross_validation().get_X_y(ml_ready_file)
			X_test, y_test = MLFL_CV.cross_validation().get_test_X_y(ml_ready_test_file)

			X_train = np.array(X_train)
			y_train = np.array(y_train)
			X_test = np.array(X_test)
			y_test = np.array(y_test)

			lr = LinearRegression()
			data_point_for_plot_dict, MAE, AE_list = MLFL_CV.cross_validation().validation_model_learning_and_prediction(lr, X_train, y_train, X_test, y_test)
			
			final_model_dict[folder] = AE_list
			print (data_point_for_plot_dict)
			print ('----------------------------')
			print ('%s' % folder)
			print ('MAE: %s' % MAE)
			print (AE_list)
			print ('----------------------------')

			MLFL_plots.plots().draw_pre_observ_scatter_plot(data_point_for_plot_dict, folder)
		MLFL_plots.plots().plot_loo_mae_variance_plot(final_model_dict, './final_model.mae.summary.pdf', "Test Data (patient's single data point)", "Absolute Error |observation - prediction|")

else:
	None