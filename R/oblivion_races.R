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
races = read.csv('../csv/oblivion_races.csv', header= T, sep =",")
races.table <- xtable(races)

races_male = subset(races, data$Gender == 'Male')
races_female = subset(races, data$Gender == 'Female')

races_data = races[,3:12][-8] # Get rid of 'luck'.

set.seed(2013)
as <- stepArchetypes(races_data, k=1:10, verbose =F, nrep = 3)

pdf('../pdf/results.pdf')
screeplot(as, main="RSS Values Across Varying Number of Archetypes", cex.main=1.5, cex.axis=1.2, cex.lab=1.5)

a3 <- bestModel(as[[3]])

paramaters = t(parameters(a3))
paramaters.table <- xtable(paramaters)

barplot(a3, races_data, percentiles=T)

alphas = cbind(races[,1:2], a3$alphas)
alphas_table <- xtable(alphas)

ternaryplot(coef(a3, 'alphas'), col = 6*as.numeric(races$Gender), id = races$Race, dimnames=c("\n\nArchetype 1\n(Fighter)","\n\nArchetype 2\n(Mage)", "Archetype 3 (Thief)"), cex=0.8, dimnames_position = c('corner'), labels = c('inside'), main="Archetypes by Attributes in TES IV: Oblivion")

pcplot(a3, races_data, data.col = as.numeric(races$Race))
dev.off()
