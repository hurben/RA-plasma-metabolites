def convert_das28_to_label(das28_list, label_num):

	das28_label_list = []

	for value in das28_list:
		if value != 'DAS':
			label = define_label(label_num, float(value))
		if value == 'DAS':
			label = 'DAS28'
		das28_label_list.append(label)

	return das28_label_list


def define_label(label_num, value):

	if label_num == 3:

		if value <= 3.2:
			label = 'l'
		if value > 3.2 and value <= 5.1:
			label = 'm'
		if value > 5.1:
			label = 'h'
	
	if label_num == 4:
		if value < 2.6:
			label = 'r'
		if value >= 2.6 and value <= 3.2:
			label = 'l'
		if value > 3.2 and value <= 5.1:
			label = 'm'
		if value > 5.1:
			label = 'h'

	return label

def monotonic_change(file_i_df, file_i, output_dir, batch_num, fc_batch, label_list, data_location_dir):

	FC_1_list = [0.1, 0.2]
	FC_2_list = [0.3, 0.4]

	output_token = file_i.split('.')

	output_str = '%s.%s.%s' % (output_token[0], output_token[1], output_token[2])

	if fc_batch == 1:
		FC_list = FC_1_list
	if fc_batch == 2:
		FC_list = FC_2_list

	for FC in FC_list:

		print ('2nd stage: %s' % FC)
		monotonic_dict, data_dict, chemID_list = calculation(file_i_df, FC, label_list)
		parsed_df_str, monotonic_change_chemID_list  = create_up_down_df(monotonic_dict, data_dict, chemID_list, label_list, output_dir, output_str, FC, file_i, data_location_dir)

		parsed_df = pd.read_csv(parsed_df_str, header=0, sep="\t")
		pvalue_dict = calculate_pvalue(parsed_df, monotonic_dict, monotonic_change_chemID_list, FC, label_list)

		output_file_str = '%s/%s.monotonic_profile_%s.tsv' % (output_dir, output_str, FC)
		dict_to_text(output_file_str, monotonic_dict, data_dict, label_list, monotonic_change_chemID_list, pvalue_dict)


def create_up_down_df(monotonic_dict, data_dict, chemID_list, label_list, output_dir, output_str, FC, file_i, data_location_dir):
	#data_dict contains mean
	#test_mean = statistics.mean(data_dict['h','100021136'])

	mid_summary_txt = open('%s/%s_%s.mid.summary.tsv' % (output_dir, output_str, FC),'w')
	monotonic_change_chemID_list = []

	num_label = len(label_list)
	if label_num == 3:
		mid_summary_txt.write('chemID\tl_mean\tm_mean\th_mean\tmonotonic_status\n')
	if label_num == 4:
		mid_summary_txt.write('chemID\tr_mean\tl_mean\tm_mean\th_mean\tmonotonic_status\n')

	for chemID in chemID_list:
		monotonic_status = monotonic_dict[chemID]
		if monotonic_status == 'up' or monotonic_status == 'down':
			mid_summary_txt.write('%s' % chemID)
			monotonic_change_chemID_list.append(chemID)

			for label in label_list:
				chemID_mean = statistics.mean(data_dict[label,chemID])
				mid_summary_txt.write('\t%s' % chemID_mean)

			mid_summary_txt.write('\t%s\n' % monotonic_status)
	
	mid_summary_txt.close()

	file_i_str = file_i.replace('.tsv','.monotonic')
	parsed_df_str = '%s/%s_%s.tsv' % (output_dir, file_i_str, FC)
	parsed_df_file = open(parsed_df_str,'w')

	file_i_str = '%s%s' % (data_location_dir, file_i)
	file_i = open(file_i_str, 'r')
	file_i_readlines = file_i.readlines()

	for i in range(len(file_i_readlines)):
		read = file_i_readlines[i]

		if i == 0:
			parsed_df_file.write(read)
		if i == 4: 
			read = read.replace('\n','')
			label_list = read.split('\t')
			label_list = convert_das28_to_label(label_list, num_label)

			for label in (label_list):
				if label == 'DAS28':
					parsed_df_file.write(label)
				else:
					parsed_df_file.write('\t%s' % label)
			parsed_df_file.write('\n')

		if i > 4:
			token = read.split('\t')
			chemID = token[0]

			if chemID in monotonic_change_chemID_list:
				parsed_df_file.write(read)
	
	parsed_df_file.close()
	
	return parsed_df_str, monotonic_change_chemID_list

def calculate_pvalue(file_i_df, monotonic_dict, monotonic_change_chemID_list, FC, label_list):

#	print ('100000257', monotonic_dict['100000257'])
	das28_label_list = list(file_i_df.iloc[0,1:])
	random_status_summary_dict = {}
	pvalue_dict = {}

	random_sampling = 10000
	for i in range(random_sampling):
#		print ("simulation step: %s" % i)
		
		random_das28_label_list = list(das28_label_list)
		random.shuffle(random_das28_label_list)
		random_das28_label_list.insert(0, "DAS28")

		file_i_df.iloc[0,:] = random_das28_label_list
		random_monotonic_dict, _, _ = calculation(file_i_df, FC, label_list)

		for chemID in monotonic_change_chemID_list:

			random_monotonic_status = random_monotonic_dict[chemID]
			try: random_status_summary_dict[chemID].append(random_monotonic_status)
			except KeyError: random_status_summary_dict[chemID] = [random_monotonic_status]

#			if chemID == '100000257':
#				if random_monotonic_status != 'dynamic':
#					print ('100000257',random_monotonic_status)
	
	for chemID in monotonic_change_chemID_list:
		real_status = monotonic_dict[chemID]
		random_status_list = random_status_summary_dict[chemID]

		random_count = random_status_list.count(real_status)
		random_chance = random_count / random_sampling
		
		#print ('%s : %s / %s = %s' % (chemID, random_count, random_sampling, random_chance))
		pvalue_dict[chemID] = random_chance

	return pvalue_dict


def calculation(file_i_df, FC, label_list):

	data_dict, chemID_list, num_labels = file_df_to_data_dict(file_i_df)
	monotonic_status_dict = {}

	for chemID in chemID_list:
		status_list = []
		prev_chem_mean = 0

		for label in label_list:

			chem_mean = statistics.mean(data_dict[label, chemID])
			this_chem_mean = chem_mean
			change_status = '-'

			if prev_chem_mean != 0:
				foldchange = math.log(this_chem_mean / prev_chem_mean, 2)

				if foldchange >= FC:
					change_status = 'up'
				if foldchange <= -FC:
					change_status = 'down'

				status_list.append(change_status)
				prev_chem_mean = this_chem_mean
				
			if prev_chem_mean == 0:
				prev_chem_mean = this_chem_mean
				status_list.append(change_status)

#		if chemID == '100000257':
#			print ('%s : %s' % (chemID, status_list))

		monotonic_status = 'dynamic'

		up_count = status_list.count('up')
		down_count = status_list.count('down')
		stable_count = status_list.count('-')

		if up_count == num_labels - 1:
			monotonic_status = 'up'
		if down_count == num_labels - 1:
			monotonic_status = 'down'
		if stable_count == num_labels:
			monotonic_status = 'stable'

		monotonic_status_dict[chemID] = monotonic_status

	return monotonic_status_dict, data_dict, chemID_list

def file_df_to_data_dict(file_i_df):

	data_dict = {}
	label_count_dict = {}
	chemID_list = []

	r, c = file_i_df.shape

	for i in range(r):

		if i == 0:
			das28_label_list = file_i_df.iloc[i,]
			for das28_label_i in range(1, len(das28_label_list)):
				label = das28_label_list[das28_label_i]
				try: label_count_dict[label] += 1
				except KeyError: label_count_dict[label] = 1

		if i != 0:
			chemID = file_i_df.iloc[i,0]
			chemID_list.append(chemID)

			for j in range(1, c):
				
				chem_value = float(file_i_df.iloc[i,j])
				das28_label = das28_label_list[j]

				try: data_dict[das28_label, chemID].append(chem_value)
				except KeyError: data_dict[das28_label, chemID] = [chem_value]

	label_list = list(label_count_dict.keys())
	num_labels = len(label_list)

	return data_dict, chemID_list, num_labels


def dict_to_text(output_txt, monotonic_dict, data_dict, label_list, chemID_list, pvalue_dict):
	
	output_txt = open(output_txt,'w')
	output_txt.write('chemID')
	for label in label_list:
		output_txt.write('\t%s_mean' % label)
	output_txt.write('\tmonotonic_status\tpval\tendpoint_log2fc\n')
	
	for chemID in chemID_list:
		output_txt.write('%s' % chemID)
		for label in label_list:
			mean = statistics.mean(data_dict[label, chemID])
			output_txt.write('\t%s' % mean)

		endpoint_fc = statistics.mean(data_dict[label_list[0], chemID]) / statistics.mean(data_dict[label_list[-1], chemID])
		endpoint_fc = math.log(endpoint_fc, 2)
		endpoint_fc = abs(endpoint_fc)

		output_txt.write('\t%s' % monotonic_dict[chemID])
		output_txt.write('\t%s' % pvalue_dict[chemID])
		output_txt.write('\t%s' % endpoint_fc)
		output_txt.write('\n')

	output_txt.close()



def main(data_location_dir, file_list, label_num, output_dir, batch_num, fc_batch):

	if label_num == 3:
		label_list = ['l','m','h']
	if label_num == 4:
		label_list = ['r','l','m','h']

	for file_i in file_list:
		file_i_dir = '%s%s' % (data_location_dir, file_i)
		file_i_df = pd.read_csv(file_i_dir, sep="\t", header=0)
		print ('Stage: %s, Label: %s' % (file_i, label_num))

		das28_list = file_i_df.iloc[3,:]
		das28_label_list = convert_das28_to_label(das28_list, label_num)
		file_i_df.iloc[3,:] = das28_label_list
		file_i_df = file_i_df.iloc[3:,:]

		monotonic_change(file_i_df, file_i, output_dir, batch_num, fc_batch, label_list, data_location_dir)



#
import sys
import pandas as pd
import statistics
import math
import random

label_num = sys.argv[1]
label_num = int(label_num)
output_dir = sys.argv[2]

batch_num = sys.argv[3]
fc_batch = sys.argv[4]
fc_batch = int(fc_batch)

rlmh_data_location_dir = './filled_qc_data/'
lmh_data_location_dir = './filled_qc_data/scenario2/'

#file_list = ['MLR.clp.fac.ready.ignor.norm.qc.fillna.tsv','MLR.clp.lc.ready.ignor.norm.qc.fillna.tsv','MLR.clp.sc.ready.ignor.norm.qc.fillna.tsv','MLR.hd4.ready.ignor.norm.qc.fillna.tsv']
batch_num = int(batch_num)
if batch_num == 1:
	file_list = ['MLR.clp.fac.ready.ignor.norm.qc.fillna.tsv']
if batch_num == 2:
	file_list = ['MLR.clp.lc.ready.ignor.norm.qc.fillna.tsv','MLR.clp.sc.ready.ignor.norm.qc.fillna.tsv']
if batch_num == 3:
	file_list = ['MLR.hd4.ready.ignor.norm.qc.fillna.tsv']

main(rlmh_data_location_dir, file_list, label_num, output_dir, batch_num, fc_batch)





#
