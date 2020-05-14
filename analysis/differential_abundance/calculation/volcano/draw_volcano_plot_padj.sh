file_dir=/Users/m221138/RA_project/analysis/differential_abundance/calculation/
while read p;
do
	Rscript /Users/m221138/RA_project/code/figures/DAM_to_VolcanoPlot_padj.r $file_dir/rm_error/$p.rm.error_padj $file_dir/volcano/padj/$p.volcano
done<pvalue.list

