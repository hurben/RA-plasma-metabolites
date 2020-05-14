file_dir=/Users/m221138/RA_project/analysis/differential_abundance/calculation/
while read p;
do
	Rscript /Users/m221138/RA_project/code/figures/DAM_to_VolcanoPlot.r $file_dir$p $file_dir$p.volcano
done<pvalue.list

mv *.volcano.* volcano/
