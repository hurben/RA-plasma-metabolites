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

if __name__ == '__main__':

	import sys
	sys.path.insert(1, '/Users/m221138/RA_project/code/machine_learning_r1/')
	sys.path.insert(1,'/Users/m221138/RA_project/code')
	sys.path.insert(1, '/Users/m221138/RA_project/code/feature_selection')
	import os
	import FL
	import MLFL_CV
	import MLFL_main
	import MLFL_plots
	import LINEAR_MODEL_FL as LMFL
	import numpy as np
	import statistics

	#MANUAL INFORMATION REQUIRED
	file_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix', 'hd4_qc_matrix']
	summary_folder = 'fs_summary'
	skip_preprocess = 0
	skip_2nd_preprocess = 0
	data_splits = 64
	#MANUAL INFORMATION REQUIRED
	
	if skip_preprocess == 0:
		for file_name in file_list:
			print  ("Preprocess to feature selection step #1  > %s" % file_name)
			preprocess(file_name, 1, 1)
		summarize_features(summary_folder)

	if skip_2nd_preprocess == 0:
		clp_only_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(clp_only_list, 'clp_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(clp_only_list, 'clp_only', data_splits)

		clp_only_list = ['clp_fac_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(clp_only_list, 'clp_fac_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(clp_only_list, 'clp_fac_only', data_splits)

		clp_only_list = ['clp_lc_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(clp_only_list, 'clp_lc_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(clp_only_list, 'clp_lc_only', data_splits)

		hd4_only_list = ['hd4_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(hd4_only_list, 'hd4_only', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(hd4_only_list, 'hd4_only', data_splits)

		hd4_clp_list = ['clp_fac_qc_matrix', 'clp_lc_qc_matrix', 'clp_sc_qc_matrix', 'hd4_qc_matrix']
		MLFL_main.feature_selection().cv_ready_matrix_step_a(hd4_clp_list, 'hd4_clp', data_splits)
		MLFL_main.feature_selection().cv_ready_matrix_step_b(hd4_clp_list, 'hd4_clp', data_splits)

		#none feature selection
		clp_only_list = ['clp_fac_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection(clp_only_list, 'clp_fac_full', data_splits)
		clp_only_list = ['clp_sc_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection(clp_only_list, 'clp_sc_full', data_splits)
		clp_only_list = ['clp_lc_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection(clp_only_list, 'clp_lc_full', data_splits)
		hd4_only_list = ['hd4_qc_matrix']
		MLFL_main.feature_selection().full_feature_selection(hd4_only_list, 'hd4_full', data_splits)

	#MANUAL INFORMATION REQUIRED
	ml_ready_folders = ['clp_only','hd4_only','hd4_clp', 'clp_fac_only','clp_sc_only', 'hd4_full', 'clp_fac_full', 'clp_sc_full', 'clp_lc_full']

	from sklearn.linear_model import LinearRegression

	loo_cv_dict = {}
	for folder in ml_ready_folders:
		ml_result_folder = '%s/ml_results' % folder

		loo_cv_mae_list = []
		loo_cv_stdv_list = []

		if os.path.isdir(ml_result_folder) == True:
			os.system('rm -r %s' % ml_result_folder)
			os.system('mkdir %s' % ml_result_folder)
		else:
			os.system('mkdir %s' % ml_result_folder)

		for index in range(1, data_splits + 1):
			ml_ready_file = '%s/%s.ml.ready.txt' % (folder, index)
			X, y = MLFL_CV.cross_validation().get_X_y(ml_ready_file)

			X = np.array(X)
			y = np.array(y)
			lr = LinearRegression()
			data_point_for_plot_dict, loo_cv_mae, loo_cv_stdv, loo_MAE_list = MLFL_CV.cross_validation().model_learning_and_prediction(lr, X, y)
			#currently data_point_for_plot_dict is not in use.
			#might have to plot every prediction points...?
			loo_cv_mae_list.append(loo_cv_mae)
			loo_cv_stdv_list.append(loo_cv_stdv)
			
		loo_cv_dict[folder] = loo_MAE_list
		print ('----------------------------')
		print ('%s' % folder)
		print ('DataSplits: %s' % data_splits)
		print ('means of MAE: %s' % statistics.mean(loo_cv_mae_list))
		print ('stdvs of MAE: %s' % statistics.mean(loo_cv_stdv_list))
		print ('----------------------------')

	MLFL_plots.plots().plot_loo_mae_variance_plot(loo_cv_dict, './mae.summary.pdf')

else:
	None
