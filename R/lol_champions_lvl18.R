#############################
# Set the working directory #
############################# 
setwd('~/Dropbox/videogame-archetypes/R')

###################
# Import libraries.
###################
library('archetypes')
library('vcd')			# for ternaryplot
library('foreign')		# Used to read .arff files.
library('xtable')		

###################
# Tutorial
###################

# vignette("archetypes", package = "archetypes")
# edit(vignette("archetypes", package = "archetypes"))

###################
# Main Code
###################

# Read the raw ARFF file.
raw <- read.arff(file='../arff/lol_champions_lvl18.arff') 

# Separate out names.
names <- raw[, c('Name')]

# Construct reduced data, without names.
data <- subset(raw, select=-c(Name))	

# Remove any columns with zero standard-deviation.
data <- subset(data, select = sapply(data,sd)!=0)

# Set seed.
set.seed(2014)

# Perform AA.
as <- stepArchetypes(data, k=1:10, verbose =T, nrep = 3)

# Scree-plot
screeplot(as, main="RSS Values Across Varying Number of Archetypes", cex.main=1.5, cex.axis=1.2, cex.lab=1.5)

# Start PDF output
# pdf('../pdf/lol_champions_base.pdf')

# Select the best model.
model <- bestModel(as[[4]])

# Transpose the representation of the model for readibility.
params = t(parameters(model))
params.table <- xtable(params)

# Barplot of the archetypes in the model.
barplot(model, data, percentiles=T)

# Get the alpha coefficients of the data.
alphas = cbind(names, model$alphas)
alphas <- model$alphas

# Graph the ternary-plot.
# ternaryplot(coef(model, 'alphas'), col = as.numeric(names), id = names, dimnames=c("1","2", "3"), cex=0.8, dimnames_position = c('corner'), labels = c('inside'), main="Archetypal Champions (Level 18) in League of Legends")

# Graph the Parallel Coordinates plot.
pcplot(model, data)

# End PDF output
# dev.off()
