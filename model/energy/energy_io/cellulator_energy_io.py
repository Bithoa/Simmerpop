from ... import global_variables
from ... import population_manager
from . import cd_energy_io
import random
import os
import math

__author__ = 'Yuta A. Takagi (2016) & Diep H. Nguyen (2018)'

# this energy In/Out is designed for Cellulator study
#
# it maintains a pool of loose energy parcels outside of organisms. energy parcels can passively move in and out of
# organisms from this pool if the organism has a low cellularity value


# the ENERGY_LIMIT is a flag indicating the behavior of the energy IO. 
# 0 = regular addition of energy and no energy pool cap
# 1 = a single burst of energy at the start and an energy pool size limited to the ENERGY_CAP_PROPORTION*POPULATION_CAP
# 2 = a single burst of energy at the start and no energy pool cap
ENERGY_LIMIT = 0
# a proportion multiplied by the POPULATION_CAP to determine the energy pool cap limit if the ENERGY_LIMIT flag is set to 1
LOOSE_ENERGY_POOL_CAP_SIZE_PROPORTION = 0.25
# the maximum size of the energy pool
LOOSE_ENERGY_POOL_CAP = math.inf 
# the amount of energy in newly added energy parcels 
NEW_ENERGY_PARCEL_SIZE = 500


# the EnergyIO class for the cellulator study
class EnergyIO(cd_energy_io.EnergyIO):  # this class name cannot be altered. Leave as 'EnergyIO'
	# initializes the class instance
	def __init__(self):
        self.loose_energy_parcels = []
		
        if 'ENERGY_LIMIT' in global_variables.parameters.keys():
        	ENERGY_LIMIT = global_variables.parameters.get('ENERGY_LIMIT')
		if 'ENERGY_CAP_PROPORTION' in global_variables.parameters.keys():
			LOOSE_ENERGY_POOL_CAP_SIZE_PROPORTION = float(global_variables.parameters.get('ENERGY_CAP_PROPORTION'))
		if ENERGY_LIMIT == 1:
			LOOSE_ENERGY_POOL_CAP = LOOSE_ENERGY_POOL_CAP_SIZE_PROPORTION*population_manager.POPULATION_CAP
		
        if 'NEW_ENERGY_PARCEL_SIZE' in global_variables.parameters.keys():
			NEW_ENERGY_PARCEL_SIZE = global_variables.parameters.get('NEW_ENERGY_PARCEL_SIZE')

	# adds energy to the environment
	def add_energy(self):
		# if energy is unlimited
		if ENERGY_LIMIT == 0:
			# add energy at a regular intervals
			if global_variables.step_num % global_variables.MUTATION_INTERVAL == 0:
				for i in range(population_manager.POPULATION_CAP):
					self.loose_energy_parcels.append(NEW_ENERGY_PARCEL_SIZE)
		# if energy is limited, add energy at start, then cull the energy pool every step
		elif ENERGY_LIMIT == 1:
			# add energy at step 0
			if global_variables.step_num == 0:
				for i in range(population_manager.POPULATION_CAP):
					self.loose_energy_parcels.append(NEW_ENERGY_PARCEL_SIZE)
			# limit energy abundance to the capacity at every step
        	self.cull_energy_pool()
		# if there is only a burst of energy at step 0, add energy at step 0
		else:
			if global_variables.step_num == 0:
				for i in range(population_manager.POPULATION_CAP):
				self.loose_energy_parcels.append(NEW_ENERGY_PARCEL_SIZE)
          
	# returns a random energy parcel from the energy pool
    def get_energy(self, organism):
        temp = len(self.loose_energy_parcels)
        if temp > 0:  # if energy is gained
            return self.loose_energy_parcels.pop(random.randint(0, temp - 1))
        else:
            return 0
          
	# removes a random amount of energy from an organism up to half its currently stored amount, and adds it as a parcel to the energy pool
    def discard_energy(self, organism):
        # returns a random amount of energy up to half of the organism's energy stock
        maximum = organism.energy / 2
        to_lose = maximum*random.random()
        self.loose_energy_parcels.append(to_lose)
        return to_lose

	# removes random energy parcels if over energy pool cap
    def cull_energy_pool(self):
        while len(self.loose_energy_parcels) > LOOSE_ENERGY_POOL_CAP:
            remove_me = random.randint(0, len(self.loose_energy_parcels) - 1)
            self.loose_energy_parcels.pop(remove_me)

