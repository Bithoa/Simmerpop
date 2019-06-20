# run_simmerpop.py
"""
This is the master program for the simmerpop.

comment out certain lines to skip the actions performed by that method. for example removing the line
'end_conditions.check_max_step()' will make it so the model doesn't stop on account of reaching a certain step count

to run the model, simply run this python script!
to change default variables to custom values, include the tag for the variable followed by the value in the arguments.
python3 run_simmerpop.py argument1 value1 argument2 value2 etc

E.g: python3 run_simmerpop.py OUTPUT_FOLDER_NAME my_run POPULATION_CAP 1000 MUTATION_PROB 0.005 ENERGY_LIM 2


"""
__author__ = 'Yuta A. Takagi (2016) & Diep H. Nguyen (2018)'
__version__ = '0.0.1'
__email__ = 'agoldman@oberlin.edu'

from model import global_variables
from model import population_manager
from model import analytics
from model import end_conditions
import sys

def main():

    # initialize the end conditions
    end_conditions.init_end_conditions()

    # initialize the global variables
    global_variables.init_global_variables(sys.argv)

    # initialize the analytics
    analytics.init_analytics()

    # initialize the population manager
    population_manager.init_population_manager()


    # run model, each loop is one step
    while end_conditions.continue_run:
        global_variables.step_num += 1  # increment the step_num variable

        # stops the model if it exceeds a maximum step count
        end_conditions.check_max_step()

        # stops the model if it exceeds a maximum runtime
        end_conditions.check_timeout()

        # disposes of dead organisms
        population_manager.clean_carcasses()

        # perform the next step for the energy in/out
        global_variables.ENERGY_IO.next_step()

        # replicates organisms with enough energy
        population_manager.replicate_organisms()

        # do mutation actions at a regular interval
        if global_variables.step_num % global_variables.MUTATION_INTERVAL == 0:
            # lose and gain energy to the environment
            population_manager.transfer_energy()

            # lose and gain genes to the environment
            population_manager.transfer_genes()

            # mutate organisms
            population_manager.mutate_organism_genomes()

            # disposes of dead organisms
            population_manager.clean_carcasses()

            # recalculate genome quality and cellularity of mutated organisms
            population_manager.recalculate_mutated_organisms()

        # reduce to population cap size
        population_manager.cull_organisms()

        # YUTA: reduce loose gene pool size to cap
        global_variables.GENOME_MANAGER.next_step()

        # perform the next step for the food in/out
        global_variables.FOOD_IO.next_step()

        # analyze and log
        analytics.analyze()

        # perform the next step for each organism
        population_manager.organisms_next_step()

        # stops the model if there are no organisms left alive
        end_conditions.check_ecosystem_alive()

    # end the model
    # ends analytics
    analytics.close_analytics()


main()
