file_dir=/Users/m221138/RA_project/analysis/differential_abundance/calculation/
while read p;
do
	cat $file_dir$p | grep -v 'error' >  $file_dir/rm_error/$p.rm.error
done<pvalue.list

