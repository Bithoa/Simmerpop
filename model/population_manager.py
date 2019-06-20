# population_manager.py
from . import global_variables
from . import analytics
from .organism import organism
import random
import os
import re

__author__ = 'Yuta A. Takagi (2016) & Diep H. Nguyen (2018)'


# defines the organism population, and actions that apply to the ecosystem as a whole (all the organisms, as opposed to
# individual organisms)



# a list storing all the organisms. its the ecosystem!
organisms = None


# initialize the population manager
def init_population_manager():
	global organisms
	# populate the ecosystem
	organisms = []
	for i in range(global_variables.START_POPULATION):
		organisms.append(organism.Organism())
	for org in organisms:
		org.id = organism.make_id('0-God*')

	# organism
	organism.init_script()


# remove dead organisms
def clean_carcasses():
	global organisms
	temp_organisms = []
	for org in organisms:
		if org.alive:
			temp_organisms.append(org)
	organisms = temp_organisms


# replicate organisms with enough energy
def replicate_organisms():
	global organisms
	temp_organisms = []
	for org in organisms:
		if org.replicate_me:
			temp1 = org.replicate()
			temp2 = org.replicate()
			temp_organisms.append(temp1)
			temp_organisms.append(temp2)
		else:
			temp_organisms.append(org)
	organisms = temp_organisms


# gain/lose energy parcels
def transfer_energy():
	global organisms
	for org in organisms:
		org.gain_energy()
	for org in organisms:
		org.lose_energy()


# gain/lose genome fragments
def transfer_genes():
	global organisms
	for org in organisms:
		org.gain_genes()
	for org in organisms:
		org.lose_genes()


# mutate genes
def mutate_organism_genomes():
	global organisms
	for org in organisms:
		org.mutate()


# actions for genome changes
def recalculate_mutated_organisms():
	global organisms
	for org in organisms:
		if org.mutated:
			org.calc_cellularity()
			org.calc_metabolic_efficiency()


# kill random organisms if over population cap
def cull_organisms():
	global organisms
	if len(organisms) > global_variables.POPULATION_CAP:
		if len(organisms) - global_variables.POPULATION_CAP >= 500:
			i = 0
			while i < 500:
				remove_me = random.randint(0, len(organisms) - 1)
				organisms.pop(remove_me)
				i = i + 1
		else:
			i = 0
			diff = len(organisms) - global_variables.POPULATION_CAP
			while i < diff:
				remove_me = random.randint(0, len(organisms) - 1)
				organisms.pop(remove_me)
				i = i + 1


# run next step for each organism
def organisms_next_step():
	global organisms
	for org in organisms:
		org.step()
