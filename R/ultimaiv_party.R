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
raw = read.csv('../csv/ultimaiv_party.csv', header= T, sep =",")

# Save non-numeric data.
characters <- raw$Character
classes <- raw$Class
weapons <- raw$Weapon
armors <- raw$Armor
gender <- raw$Gender

# Remove non-numeric data.
data <- raw[, -which(names(raw) %in% c("Character","Class","Weapon","Armor","Gender"))]

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
params <- t(parameters(model))
params.table <- xtable(params)


# Barplot of the archetypes in the model.
barplot(model, data, percentiles=T)

# Get the alpha coefficients of the data.
alphas <- cbind(cbind(data.frame(characters), classes), model$alphas)
alphas_table <- xtable(alphas)

# Sorted alphas
sort1 <- alphas[order(-alphas$'1'),]

# Graph the ternary-plot.
ternaryplot(coef(model, 'alphas'), col = 6*as.numeric(gender), id = characters, dimnames=c("1","2", "3"), cex=0.8, dimnames_position = c('corner'), labels = c('inside'), main="Archetypal Party Members in Ultima IV")

# Graph the Parallel Coordinates plot.
pcplot(model, data)

# End PDF output
# dev.off()