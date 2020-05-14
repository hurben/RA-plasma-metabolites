file_dir=/Users/m221138/RA_project/analysis/differential_abundance/calculation
while read p;
do
	Rscript /Users/m221138/RA_project/code/figures/DAM_to_VolcanoPlot.r $file_dir/rm_error/$p.rm.error $file_dir/volcano/$p.volcano
done<pvalue.clp.list

while read p;
do
	Rscript /Users/m221138/RA_project/code/figures/DAM_to_VolcanoPlot.r $file_dir/rm_error/$p.rm.error.converted $file_dir/volcano/$p.volcano
done<pvalue.hd4.list

