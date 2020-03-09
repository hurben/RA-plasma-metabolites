class cross_validation:

	def get_X_y(self, input_file):
		import pandas as pd
		
		data_df = pd.read_csv(input_file,sep="\t", index_col=0)
		data_df = data_df.T  #tilt data
		data_df.fillna(data_df.mean(), inplace=True)

		y = data_df.iloc[:,0]
		X = data_df.iloc[:,1:]
		return X, y

	def model_learning_and_prediction(self, model, X, y):

		import numpy as np
		from sklearn.model_selection import LeaveOneOut
		from sklearn.metrics import mean_absolute_error
		import statistics

		ran_num = np.random
		loo = LeaveOneOut()
		loo.get_n_splits(X)
		
		loo_MAE_list = []
		test_count = 1
		
		data_point_for_plot_dict = {}
		
		for train_i, test_i in loo.split(X):
			#print (test_i)

			X_train, X_test = X[train_i], X[test_i]
			y_train, y_test = y[train_i], y[test_i]

			model_fit = model.fit(X_train, y_train)
			prediction = model_fit.predict(X_test)
			observed_value = y_test
			
			MAE = mean_absolute_error(observed_value, prediction)

			#print ("FOLD #%s MAE: %s" % (test_count, MAE))
			
			observed_value = y_test[0]
			prediction = prediction[0]

			try :
				data_point_for_plot_dict['observe'].append(observed_value)
				data_point_for_plot_dict['predict'].append(prediction)
			except KeyError:
				data_point_for_plot_dict['observe'] = [observed_value]
				data_point_for_plot_dict['predict'] = [prediction]
				
			test_count = test_count + 1
			loo_MAE_list.append(MAE)

		#print ("MAE of LOO:", loo_MAE_list)
		#print ("MEANS of LOO MAE:",statistics.mean(loo_MAE_list))
		#print ("STANDARD DEVIATIONs of LOO MAE:",statistics.stdev(loo_MAE_list))
		
		return data_point_for_plot_dict, statistics.mean(loo_MAE_list), statistics.stdev(loo_MAE_list), loo_MAE_list

	def model_learning_and_prediction_v2(self, model, X, y):

		import numpy as np
		from sklearn.model_selection import LeaveOneOut
		from sklearn.metrics import mean_absolute_error
		import statistics

		ran_num = np.random
		loo = LeaveOneOut()
		loo.get_n_splits(X)
		
		loo_MAE_list = []
		test_count = 1
		
		data_point_for_plot_dict = {}
		
		for train_i, test_i in loo.split(X):
			#print (test_i)

			X_train, X_test = X[train_i], X[test_i]
			y_train, y_test = y[train_i], y[test_i]

			model_fit = model.fit(X_train, y_train)
			prediction = model_fit.predict(X_test)
			observed_value = y_test
			
			MAE = mean_absolute_error(observed_value, prediction)

			#print ("FOLD #%s MAE: %s" % (test_count, MAE))
			
			observed_value = y_test[0]
			prediction = prediction[0]

			try :
				data_point_for_plot_dict['observe'].append(observed_value)
				data_point_for_plot_dict['predict'].append(prediction)
			except KeyError:
				data_point_for_plot_dict['observe'] = [observed_value]
				data_point_for_plot_dict['predict'] = [prediction]
				
			test_count = test_count + 1
			loo_MAE_list.append(MAE)

		#print ("MAE of LOO:", loo_MAE_list)
		#print ("MEANS of LOO MAE:",statistics.mean(loo_MAE_list))
		#print ("STANDARD DEVIATIONs of LOO MAE:",statistics.stdev(loo_MAE_list))
		
		return data_point_for_plot_dict, statistics.mean(loo_MAE_list), statistics.stdev(loo_MAE_list), loo_MAE_list




	def remove_samples(self, X, y):
		#X = Sample Matrix
		#Y = Vector Sample Label Matrix

		available_patient_index_list = []
		refined_y = [] 
		refined_X = []
		
		for i in range(len(y)):
			
			label = y[i]
			
			if label <= 5.1:
			   
				available_patient_index_list.append(i)
				refined_y.append(label)
				
		for i in available_patient_index_list:
			refined_X.append(X[i])
			
		print ("Number Entries in Refined X: %s" % len(refined_X))
		print ("Number Entries in Refined y: %s" % len(refined_y))
		refined_X = np.array(refined_X)
		refined_y = np.array(refined_y)
		
		return refined_X, refined_y

	def get_index_list(self, loo_mae_list):
		set_index_list = []
		for i in range(len(loo_mae_list)):
			set_index_list.append(i+1)
		return set_index_list

if __name__ == '__main__':

	print ('Not meant to be run')
else:

	print ('Loading MLFL_CV')
