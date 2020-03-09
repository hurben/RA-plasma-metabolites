#heatmap_fulldataset             20.02.18
#hur.benjamin@mayo.edu
#
#[1] Draw heatmap from given matrix
#[2] Designed to run this script for feature selected dataset.

 
library(gplots)
library(pheatmap)
library(RColorBrewer)
library(matrixStats)

#for cut-tree, currently not in use
#library(dendextend)

input_data <- '/Users/m221138/RA_project/analysis/all_in_one_r2/hd4_only/full.ml.ready.txt'
input_df <- read.csv(input_data, header=TRUE, row.names=1, sep="\t")

NUM_ROW = nrow(input_df)
NUM_COL = ncol(input_df)

das28_list <- input_df[1,]

for (i in 1:NUM_COL){
	das28 = das28_list[i]
	if (das28 < 2.6){
		category = 'nearRemission'
	}
	if (das28 <= 3.2 & das28 >= 2.6){
		category = 'low'
	}
	if (das28 > 3.2 & das28 <= 5.1){
		category = 'med'
	}
	if (das28 > 5.1 ){
		category = 'high'
	}

	das28_list[i] <- category
}
das28_meta <- data.frame(t(das28_list))



input_df <- as.matrix(input_df[2:NUM_ROW,])
col_names <- colnames(input_df)
row_names <- rownames(input_df)

rank_df <- rowRanks(-input_df)
colnames(rank_df) <- col_names
rownames(rank_df) <- row_names

pal <- colorRampPalette(c("yellow","red"))
pal <- pal(128)

pdf("/Users/m221138/RA_project/analysis/51_feature_selection.pdf", width=20, height=10)
heatmap_results <- pheatmap(rank_df, color=pal, annotation_col = das28_meta)
dev.off()

sorted_patientID_list <- colnames(rank_df[,heatmap_results$tree_col[["order"]]])
sorted_das28_list <- as.matrix(das28_list[,heatmap_results$tree_col[["order"]]])


