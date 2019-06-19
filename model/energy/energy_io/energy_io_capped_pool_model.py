from ... import global_variables
from ... import population_manager
from ... import analytics
from . import cd_energy_io
import random
import os
import math

__author__ = 'Yuta A. Takagi (2016) & Diep H. Nguyen (2018)'

# this energy In/Out is designed for Yuta's model
#
# it maintains a pool of loose energy parcels outside of organisms. energy parcels can passively move in and out of
# organisms from this pool if the organism has a low cellularity value


# ====================================================================================================
# ****************************************************************************************************
LOOSE_ENERGY_POOL_CAP = math.inf
ENERGY_LIMIT = 0
# ****************************************************************************************************
# ====================================================================================================


class EnergyIO(cd_energy_io.EnergyIO):  # this class name cannot be altered. Leave as 'EnergyIO'
    def __init__(self):
        self.loose_energy_parcels = []
        # else:
        #     # load save line
        #     save_file = open(os.path.join(analytics.OUTPUT_DIRECTORY, 'save_points.txt'), 'r')
        #     for line in save_file:
        #         save_line = line
        #     saved_params = save_line.split('\t')
        #     if saved_params[3] == '[]':
        #         self.loose_energy_parcels = []
        #     else:
        #         self.loose_energy_parcels = \
        #             [float(energy_parcel_as_string)
        #              for energy_parcel_as_string in saved_params[3].strip().strip('[]').split(', ')]

        if 'energy_limit' in global_variables.parameters.keys():
            ENERGY_LIMIT = global_variables.parameters.get('energy_limit')
        else:
            ENERGY_LIMIT = 0
        if ENERGY_LIMIT == 1:
            LOOSE_ENERGY_POOL_CAP = 0.25*population_manager.POPULATION_CAP

    # adds energy to the environment
    def add_energy(self):
      # if energy is unlimited
      if ENERGY_LIMIT == 0:
        # add energy at a regular intervals
        if global_variables.step_num % global_variables.MUTATION_INTERVAL == 0:
            for i in range(population_manager.POPULATION_CAP):
                self.loose_energy_parcels.append(500)

      # if energy is limited, add energy at start, then cull the energy pool every step
      elif ENERGY_LIMIT == 1:
        # add energy at step 0
        if global_variables.step_num == 0:
            for i in range(population_manager.POPULATION_CAP):
                self.loose_energy_parcels.append(500)
        # limit energy abundance to the capacity at every step
        self.cull_energy_pool()
      # if there is only a burst of energy at step 0, add energy at stepelse:
      else:
        if global_variables.step_num == 0:
          for i in range(population_manager.POPULATION_CAP):
           	self.loose_energy_parcels.append(500)


    def get_energy(self, organism):
        temp = len(self.loose_energy_parcels)
        if temp > 0:  # if energy is gained
            return self.loose_energy_parcels.pop(random.randint(0, temp - 1))
        else:
            return 0

    def discard_energy(self, organism):
        # returns a random amount of energy up to half of the organism's energy stock
        maximum = organism.energy / 2
        to_lose = maximum*random.random()
        self.loose_energy_parcels.append(to_lose)
        return to_lose

    def cull_energy_pool(self):
        # remove random energy parcels if over energy pool cap
        while len(self.loose_energy_parcels) > LOOSE_ENERGY_POOL_CAP:
            remove_me = random.randint(0, len(self.loose_energy_parcels) - 1)
            self.loose_energy_parcels.pop(remove_me)
