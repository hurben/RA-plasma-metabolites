file_dir=/Users/m221138/RA_project/analysis/differential_abundance/calculation/
while read p;
do
	cat $file_dir$p.padj | grep -v 'error' >  $file_dir/rm_error_padj/$p.rm.error_padj
done<pvalue.list

