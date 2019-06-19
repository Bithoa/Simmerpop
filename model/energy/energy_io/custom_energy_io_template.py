from ... import global_variables
from ... import population_manager
from ... import analytics
from . import cd_energy_io
import random

__author__ = 'Yuta A. Takagi'


# a energy In/Out manages the global aspects of energy and interfaces between the population portion of the model.
# having a separate set of modules for energy allows for the mechanics of this part of the model to be independently
# changed without a need to alter the rest of the model.


# ====================================================================================================
# ****************************************************************************************************


# ****************************************************************************************************
# ====================================================================================================


# all energy In/Outs should be child classes to the 'EnergyIO' class defined in the 'cd_energy_io' module
class EnergyIO(cd_energy_io.EnergyIO):  # this class name cannot be altered. Leave as 'EnergyIO'
    def __init__(self):
        # only one 'EnergyIO' instance is created. any custom variables can be defined here.
        # make sure to initialize from saved settings here if you'd like to add custom save functionality

        # the following example line creates a variable to store the discarded energy
        self.trash = 0

    def get_energy(self, organism):
        # this method is called when an organism requires environmental energy and should return a float representing
        # the energy. note that this is energy acquired passively from the environment, not the energy rewarded for
        # solving food. as such, it should generally be set to 0 unless you are implementing a specific model for
        # passive energy acquisition.

        # this example line returns 2.0 energy
        return 2.0

    def discard_energy(self, organism):
        # this method is called when an organism must lose energy to the environment and should return a float
        # representing the magnitude of the lost energy. note that this is energy lost passively to the environment, and
        # as such, it should generally be set to 0 unless you are implementing a specific model for passive energy loss.

        # the following example lines returns a random amount of energy less than the organism's energy stock.
        # 'organism.energy' accesses the 'Organism's current energy stock. then this energy is added to the custom
        # variable self.trash.
        to_lose = organism.energy*random.random()
        self.trash += to_lose
        return to_lose
