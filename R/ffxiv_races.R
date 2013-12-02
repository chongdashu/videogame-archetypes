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
library('xtable')		# Used to convert tables to LaTex

###################
# Tutorial
###################

# vignette("archetypes", package = "archetypes")
# edit(vignette("archetypes", package = "archetypes"))

###################
# Main Code
###################

# Read the raw ARFF file.
raw <- read.arff(file='../arff/ffxiv_races.arff') 
raw.table <- xtable(raw)

# Separate out names.
race <- raw[, c('Race')]
subrace <- raw[, c('Subrace')]

# Construct reduced data, without names.
data <- raw[, -which(names(raw) %in% c("Race","Subrace"))]

# Remove any columns with zero standard-deviation.
data <- subset(data, select = sapply(data,sd)!=0)

# Set seed.
set.seed(2013)

# Perform AA.
as <- stepArchetypes(data, k=1:10, verbose =T, nrep = 3)

# Scree-plot
screeplot(as, main="RSS Values Across Varying Number of Archetypes", cex.main=1.5, cex.axis=1.2, cex.lab=1.5)

# Start PDF output
# pdf('../pdf/lol_champions_base.pdf')

# Select the best model.
model <- bestModel(as[[3]])

# Transpose the representation of the model for readibility.
paramaters = t(parameters(model))
paramaters.table <- xtable(paramaters)

# Barplot of the archetypes in the model.
barplot(model, data, percentiles=T)

# Get the alpha coefficients of the data.
alphas <- cbind(cbind(data.frame(race),subrace), model$alphas)
alphas_table <- xtable(alphas)

# Sorted alphas
sort1 <- alphas[order(-alphas$'1'),]

# Graph the ternary-plot.
ternaryplot(coef(model, 'alphas'), id = subrace, dimnames=c("\n\nArchetype 1\n(Healer)","\n\nArchetype 2 \n(Support)", "Archetype 3 (Tank)"), cex=0.8, dimnames_position = c('corner'), labels = c('inside'), main="Archetypal Races/Sub-Races in FF XIV")

# Graph the Parallel Coordinates plot.
pcplot(model, data)

# End PDF output
# dev.off()
