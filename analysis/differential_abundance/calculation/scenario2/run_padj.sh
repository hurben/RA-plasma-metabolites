file_dir=/Users/m221138/RA_project/analysis/differential_abundance/calculation/scenario2/
while read p;
do
	Rscript /Users/m221138/RA_project/code/linear_model_r1/diff_abundance_adjpvalue_r.r $filedir$p $filedir$p.padj
done <pvalue.list
