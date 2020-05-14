class plots:

	def draw_density_plot(self, pre_y, y, output):
		
		density_plot = sns.distplot(pre_y, rug=True, hist=False, label="Full Dataset")
		density_plot = sns.distplot(y, rug=True, hist=False, label="Pooled dataset (DAS28 <= 5.1)")
		density_plot = density_plot.get_figure()
		density_plot.savefig(output)
		
	def plot_prediction_differences(self, data_point_for_plot_dict, plot_output, mean, sd):

		plot_output = '%s.pdf'% plot_output
		
		palette = sns.color_palette()
		
		observed_value = data_point_for_plot_dict['observe']
		prediction = data_point_for_plot_dict['predict']  
		sns_plot = sns.regplot(prediction, observed_value)
		sns_plot.set(xlabel='DAS28 (Prediction)', ylabel='DAS28 (Observation)')
		sns_plot.get_figure()
		sns_plot.figure.savefig(plot_output)
		sns_plot.get_figure().clf()
		
	def plot_prediction_differences_v2(self, plot_1_dict, plot_2_dict, plot_output):
		

		plot_output = '%s.prediction.summary.pdf'% plot_output
		
		palette = sns.color_palette()
		
		observed_value = plot_1_dict['observe']
		prediction = plot_1_dict['predict'] 
		sns_plot = sns.regplot(prediction, observed_value, ci=None, label="full", scatter_kws={'s':10})
		
		observed_value = plot_2_dict['observe']
		prediction = plot_2_dict['predict'] 
		sns_plot = sns.regplot(prediction, observed_value, ci=None, label="pooled", scatter_kws={'s':10})
		sns_plot = sns.regplot(observed_value, observed_value, ci=None, label="Perfect model", scatter_kws={'s':10})
		
		sns_plot.set(xlabel='DAS28 (Prediction)', ylabel='DAS28 (Observation)')
		sns_plot.set_ylim(0,7)
		sns_plot.set_xlim(0,7)
		sns_plot.legend()
		sns_plot.get_figure()
		sns_plot.figure.savefig(plot_output)
		sns_plot.get_figure().clf()
		
	def plot_loo_mae_variance_plot(self, loo_mae_dict, summary_file, label_x, label_y):
		
		for folder in list(loo_mae_dict.keys()):
			loo_mae_list = loo_mae_dict[folder]
			mean_mae = round(statistics.mean(loo_mae_list),2)

			plot_output = './%s/ml_results/macro_mae.pdf' % folder
			
			set_index_list = self.get_index_list(loo_mae_list)
			
			loo_mae_list.sort(reverse=True)

			sns_plot = sns.lineplot(set_index_list, loo_mae_list, label=folder)
			
			sns_plot.set(xlabel='Index of sample set', ylabel='Mean Absolute Error')
			sns_plot.set_ylim(0,5)
			sns_plot.get_figure()
			sns_plot.figure.savefig(plot_output)
			sns_plot.get_figure().clf()


		NUM_CONDITIONS = len(list(loo_mae_dict.keys()))
		print (NUM_CONDITIONS)

		#Manual color changes
		#normal color-color paltted will have light color in the middle (which is not very visualable)
		color_list = sns.color_palette("RdBu_r", 5)
		color_list.pop(2)

		for i in range(len(list(loo_mae_dict.keys()))):
			folder = list(loo_mae_dict.keys())[i]
			loo_mae_list = loo_mae_dict[folder]
			set_index_list = self.get_index_list(loo_mae_list)
			loo_mae_list.sort(reverse=True)

			print (i)
			print (loo_mae_list)
			print (set_index_list)

			summary_sns_plot = sns.lineplot(set_index_list, loo_mae_list, label=folder, color=color_list[i])
			#summary_sns_plot = sns.lineplot(set_index_list, loo_mae_list, label=folder, color=color_list[i])

		summary_sns_plot.set(xlabel=label_x, ylabel=label_y)
		summary_sns_plot.set_ylim(0,5)
		summary_sns_plot.get_figure()
		summary_sns_plot.figure.savefig(summary_file)
		summary_sns_plot.get_figure().clf()


	def draw_pre_observ_scatter_plot(self, data_point_dict, folder_name):
	#keys = observation, prediction

		output_name = './%s.final_model.prediction.pdf' % folder_name

		theoretical_X = list(range(0,7))
		theoretical_y = list(range(0,7))

		corr, pvalue = spearmanr(data_point_dict["predict"], data_point_dict["observe"])

		preobs_plot = sns.lineplot(theoretical_X, theoretical_y, label="Therotical Perfect Model")
		preobs_plot = sns.regplot(data_point_dict["predict"], data_point_dict["observe"], truncate=False, label="DAS28-crp correlated features")

		preobs_plot.set(xlabel="prediction", ylabel="observation")
		preobs_plot.legend()
		preobs_plot.set_title('%s\ncorr: %s pval: %s' % (folder_name, round(corr,3), round(pvalue, 3)))
		preobs_plot.get_figure()
		preobs_plot.figure.savefig(output_name)
		preobs_plot.get_figure().clf()


	def get_index_list(self, loo_mae_list):
		set_index_list = []
		for i in range(len(loo_mae_list)):
			set_index_list.append(i+1)
		return set_index_list

if __name__ == "__main__":
	print ("Not meant to be run")
else:
	import os
	import seaborn as sns
	import statistics
	from scipy.stats import spearmanr
	from pylab import savefig
	import matplotlib.pyplot as plt
	from matplotlib.pyplot import axes
	print ("Loading MLFL_plots")
