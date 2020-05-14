#file_dir='/Users/m221138/RA_project/analysis/differential_abundance/calculation/rm_error'
while read p;
do
	input=$p
	output=$input.converted
	python /Users/m221138/RA_project/code/qc_raw_data/hd4_convert_chemID.py $input $output
done<hd4.list
