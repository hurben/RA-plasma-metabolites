import sys
import os
sys.path.insert(1, '/Users/m221138/RA_project/code')
import FL

def manage_feature_profiles(feature_list_file):

	feature_dict = {}
	feature_file_list = open(feature_list_file,'r')
	feature_file_list_readlines = feature_file_list.readlines()

	for i in range(len(feature_file_list_readlines)):
		each_file = feature_file_list_readlines[i]
		each_file = each_file.replace('\n','')

		feature_file_name = each_file.split('.')[0]
		if feature_file_name == "clp":
			feature_file_name = "%s.%s" % (each_file.split('.')[0], each_file.split('.')[1])

		each_file = open(each_file,'r')
		file_readlines = each_file.readlines()

		for j in range(len(file_readlines)):
			chem_name = file_readlines[j]
			chem_name = chem_name.replace('\n','')

			try: feature_dict[feature_file_name].append(chem_name)
			except KeyError: feature_dict[feature_file_name] = [chem_name]

	return feature_dict

def manage_data_profile(data_profile_list_file, feature_dict):

	data_dict = {}
	data_index_dict = {}

	data_profile_list_file = open(data_profile_list_file,'r')
	data_profile_list_readlines = data_profile_list_file.readlines()

	for i in range(len(data_profile_list_readlines)):
		each_file = data_profile_list_readlines[i]
		each_file = each_file.replace('\n','')

		if each_file[0:3] == 'clp':
			data_profile_name = "%s.%s" % (each_file.split("_")[0], each_file.split("_")[1])

		else:
			data_profile_name = "hd4"

		data_profile_dict, chemID_list, patientID_list = FL.data_profile_manage(each_file)

		data_dict[data_profile_name] = data_profile_dict
		data_index_dict[data_profile_name] = [chemID_list, patientID_list]

	return data_dict, data_index_dict

def patient_intersection(data_index_dict):


	for i in range(len(data_index_dict.keys())):

		feature = list(data_index_dict.keys())[i]
		print ('Considering Feature: %s' %feature)

		if i == 0:
			common_pateintID_list = data_index_dict[feature][1]
			print ('Initializing patient lists.. total: %s' %len(common_pateintID_list))
		else:
			patientID_list = data_index_dict[feature][1]
			common_patientID_list = set(common_pateintID_list).intersection(set(patientID_list))
			print ('Intersection with patient lists.. total: %s' %len(common_pateintID_list))

	return common_patientID_list


if __name__ == "__main__":

	feature_list_file = sys.argv[1]
	data_profile_list_file = sys.argv[2]
	output_txt = open('feature.selection.data.matrix.tsv','w')

	feature_dict = manage_feature_profiles(feature_list_file)
	data_profile_dict, data_index_dict = manage_data_profile(data_profile_list_file, feature_dict)
	#dict[A][B,C] = [participantID, chem_t1, chem_t2, fc_chem, das_t1, das_t2, fc_das, das_label, sex, age_t1, age_t2]
	
	patientID_list = patient_intersection(data_index_dict)

	feature_list = list(data_profile_dict.keys())

	for patientID in patientID_list:
		output_txt.write('\t%s_t1\t%s_t2' % (patientID, patientID))
	output_txt.write('\n')

	#Lazy method
	#>>>>>>>>>>>>>>>>>>>>
	for feature in feature_dict.keys():
		chemID_list = feature_dict[feature]
		for chemID in chemID_list:
			output_txt.write('DAS')
			for patientID in patientID_list:
				das_t1 = data_profile_dict[feature][chemID, patientID][4]
				das_t2 = data_profile_dict[feature][chemID, patientID][5]
				output_txt.write('\t%s\t%s' % (das_t1, das_t2))
			output_txt.write('\n')
			break
		break
	#<<<<<<<<<<<<<<<<<<<

	for feature in feature_dict.keys():
		chemID_list = feature_dict[feature]
		for chemID in chemID_list:
			output_txt.write(chemID)
			for patientID in patientID_list:
				try: 
					chem_t1 = data_profile_dict[feature][chemID, patientID][1]
					chem_t2 = data_profile_dict[feature][chemID, patientID][2]
				except KeyError:
					chem_t1 = 'nan'
					chem_t2 = 'nan'
				output_txt.write('\t%s\t%s' % (chem_t1, chem_t2))
			output_txt.write('\n')
	output_txt.close()

else:
	print ("Loading create_parsed_matrix.py")




