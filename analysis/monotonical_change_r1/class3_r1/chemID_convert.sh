while read p
do
	python /Users/m221138/RA_project/code/qc_raw_data/hd4_convert_chemID.py $p $p.converted
done<summary.list


