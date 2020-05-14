file_dir=/Users/m221138/RA_project/analysis/differential_abundance/calculation/scenario2
while read p;
do
	Rscript /Users/m221138/RA_project/code/figures/DAM_to_VolcanoPlot.r $file_dir/rm_error/$p.rm.error $file_dir/volcano/$p.volcano
done<pvalue.list

