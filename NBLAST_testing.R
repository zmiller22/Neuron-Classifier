library(nat)
library(nat.nblast)
library(dendroextras)

gad_dir = "/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/labeled_kunst_data_aligned/data/Gad1b"
glut_dir = "/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/labeled_kunst_data_aligned/data/VGlut2a"
unlabeled_dir = "/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/unlabeled_kunst_data_aligned/data/Original"


# load neurons
gad_nrns <- read.neurons(gad_dir, format="swc")
glut_nrns <- read.neurons(glut_dir, format="swc")
unlabeled_nrns <- read.neurons(unlabeled_dir, format="swc")


# get all-by-all clustering scores
gad_aba_scores <- nblast_allbyall(gad_nrns)
glut_aba_scores <- nblast_allbyall(glut_nrns)
unlabeled_aba_scores <- nblast_allbyall(unlabeled_nrns)

#gad_to_unlabeled_scores_df = data.frame(nblast(gad_nrns, unlabeled_nrns))
#glut_to_unlabeled_scores_df = data.frame(nblast(glut_nrns, unlabeled_nrns))

# apply(gad_to_unlabeled_scores_df, 2, which.max) # gets the row index of the max for each column,
# these would be the index of the most matching neuron

open3d()
plot3d(gad_clusters, k=3, db=gad_nrns, soma=T)
plot3d(glut_nrns, soma=TRUE)
#all_neurons <- c(gad_nrns, glut_nrns, unlabeled_nrns)

plot3d(unlabeled_nrns[[1212]], col="red", soma=TRUE)
plot3d(gad_nrns[[10]], col="blue", soma=TRUE)


