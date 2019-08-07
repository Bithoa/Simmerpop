
#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

import os
import sys
import time
import operator

from . import global_variables
from . import population_manager
from . import end_conditions

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'

# defines a number of functions to perform analytic activities as well as saving functionality

# user defined static variables
# ====================================================================================================
# ****************************************************************************************************

# the folder to write results
OUTPUT_FOLDER_NAME = 'default_folder_name'
OUTPUT_DIRECTORY = None

# ****************************************************************************************************
# ====================================================================================================


# output files
output_debug = None
output_results = None
output_results_organism_metabolic_efficiency_bins = None
output_results_organism_cellularity_bins = None
output_results_current_best_solutions = None
output_results_cellularity_vs_metabolic_efficiency = None

# analytics variables
header_line = None
exit_line = None


# initialize the analytics
def init_analytics():
	global OUTPUT_DIRECTORY
	global OUTPUT_FOLDER_NAME
	if 'OUTPUT_FOLDER_NAME' in global_variables.parameters.keys():
		OUTPUT_FOLDER_NAME = global_variables.parameters.get('OUTPUT_FOLDER_NAME')

	try:
		OUTPUT_DIRECTORY = os.path.join(os.path.dirname(__file__), OUTPUT_FOLDER_NAME)
		os.makedirs(OUTPUT_DIRECTORY)
	except FileExistsError:
		print(
			'WARNING! Folder \"' + OUTPUT_FOLDER_NAME + '\" already exists. Program terminated to avoid overwriting contents.')
		sys.exit()
		pass

	initialization_message()  # logs info at start of run
	prep_files()  # initialize results files


# ends analytics
def close_analytics():
	exit_message()	# logs exit conditions
	close_files()  # closes files


# initialize results files
def prep_files():
	global OUTPUT_DIRECTORY
	global output_debug
	global output_results
	global output_results_organism_metabolic_efficiency_bins
	global output_results_organism_cellularity_bins
	global output_results_current_best_solutions
	global output_results_cellularity_vs_metabolic_efficiency

	# create output files
	output_debug = open(os.path.join(OUTPUT_DIRECTORY, 'debug.txt'), 'w')
	output_results = open(os.path.join(OUTPUT_DIRECTORY, 'results.txt'), 'w')
	output_results_organism_metabolic_efficiency_bins \
		= open(os.path.join(OUTPUT_DIRECTORY, 'results_organism_metabolic_efficiency_bins.txt'), 'w')
	output_results_organism_cellularity_bins \
		= open(os.path.join(OUTPUT_DIRECTORY, 'results_organism_cellularity_bins.txt'), 'w')
	output_results_current_best_solutions = \
		open(os.path.join(OUTPUT_DIRECTORY, 'results_organism_current_best_solutions.txt'), 'w')
	output_results_cellularity_vs_metabolic_efficiency = \
		open(os.path.join(OUTPUT_DIRECTORY, 'results_cellularity_vs_metabolic_efficiency.txt'), 'w')

	# prep output files
	print('step_num\tnum_organisms\tmean_org_cellularity\tmean_org_metabolism\tnum_energy_parcels\ttotal_energy\t'
		  'num_genes')
	output_results.write('step_num\tnum_organisms\tmean_org_cellularity\tmean_org_metabolism\tnum_energy_parcels\t'
						 'total_energy\n')
	output_debug.write(header_line)
	output_results_cellularity_vs_metabolic_efficiency.write('step_num\torg_cellularity\torg_metabolic_efficiency\n')


# close output files
def close_files():
	output_debug.close()
	output_results.close()
	output_results_organism_metabolic_efficiency_bins.close()
	output_results_organism_cellularity_bins.close()
	output_results_cellularity_vs_metabolic_efficiency.close()

# logs info at start of run
def initialization_message():
	global OUTPUT_FOLDER_NAME
	# for file metadata
	temp = str(OUTPUT_FOLDER_NAME)
	temp += '\tnum_steps: ' + str(end_conditions.NUM_STEPS)
	temp += '\tpop_cap: ' + str(global_variables.POPULATION_CAP)
	temp += '\tstart_pop_size: ' + str(global_variables.START_POPULATION)
	temp += '\tmutation_interval: ' + str(global_variables.MUTATION_INTERVAL)
	struct_time = time.localtime(end_conditions.START_TIME)
	temp += '\tdate/time: ' + time.strftime('%Y', struct_time)
	temp += '-' + time.strftime('%m', struct_time)
	temp += '-' + time.strftime('%d', struct_time)
	temp += ' ' + time.strftime('%H', struct_time)
	temp += ':' + time.strftime('%M', struct_time)
	temp += ':' + time.strftime('%S', struct_time)
	temp += '\n'
	global header_line
	header_line = temp


# logs exit conditions
def exit_message():
	global exit_line
	output_results.write(exit_line)
	output_debug.write(exit_line)
	print(exit_line)


# perform analytics
def analyze():
	temp_to_write = str(global_variables.step_num) + ':\t' + str(len(population_manager.organisms)) + '\t'
	if len(population_manager.organisms) > 0:
		temp_to_write += '%.4f' % (
		sum([org.cellularity for org in population_manager.organisms]) / len(population_manager.organisms)) + '\t'
		temp_to_write += '%.4f' % (
		sum([org.metabolic_efficiency for org in population_manager.organisms]) / len(population_manager.organisms)) + '\t'
	else:
		temp_to_write += 'None\tNone\t'
	temp_to_write += str(len(global_variables.ENERGY_IO.loose_energy_parcels)) + '\t'
	temp_to_write += '%.2f' % (sum([energy for energy in global_variables.ENERGY_IO.loose_energy_parcels])) + '\t'

	output_results.write(temp_to_write + '\n')


	if (global_variables.step_num) % 100 == 0:
		best_organism = max(population_manager.organisms, key=operator.attrgetter('metabolic_efficiency'))
		output_results_current_best_solutions.write(
			str(global_variables.step_num) + ':\t' + str(best_organism.metabolic_efficiency) + '\t' + str(
				best_organism.cellularity) +
			'\t' + str(best_organism.genome) + '\n')

	if (global_variables.step_num) % global_variables.MUTATION_INTERVAL == 0:

		metabolic_efficiency_bin_tallies = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
									  0]  # 0-0.5, 0.5-1, 1-1.5, 1.5-2, 2-2.5, 2.5-3, 3-3.5, 3.5-4, 4-4.5, 4.5-5, 5-5.5, 5.5-6, 6-6.5, 6.5-7, 7-7.5, 7.5-8
		for org in population_manager.organisms:
			if org.metabolic_efficiency < 0.5:
				metabolic_efficiency_bin_tallies[0] += 1
			elif org.metabolic_efficiency < 1:
				metabolic_efficiency_bin_tallies[1] += 1
			elif org.metabolic_efficiency < 1.5:
				metabolic_efficiency_bin_tallies[2] += 1
			elif org.metabolic_efficiency < 2:
				metabolic_efficiency_bin_tallies[3] += 1
			elif org.metabolic_efficiency < 2.5:
				metabolic_efficiency_bin_tallies[4] += 1
			elif org.metabolic_efficiency < 3:
				metabolic_efficiency_bin_tallies[5] += 1
			elif org.metabolic_efficiency < 3.5:
				metabolic_efficiency_bin_tallies[6] += 1
			elif org.metabolic_efficiency < 4:
				metabolic_efficiency_bin_tallies[7] += 1
			elif org.metabolic_efficiency < 4.5:
				metabolic_efficiency_bin_tallies[8] += 1
			elif org.metabolic_efficiency < 5:
				metabolic_efficiency_bin_tallies[9] += 1
			elif org.metabolic_efficiency < 5.5:
				metabolic_efficiency_bin_tallies[10] += 1
			elif org.metabolic_efficiency < 6:
				metabolic_efficiency_bin_tallies[11] += 1
			elif org.metabolic_efficiency < 6.5:
				metabolic_efficiency_bin_tallies[12] += 1
			elif org.metabolic_efficiency < 7:
				metabolic_efficiency_bin_tallies[13] += 1
			elif org.metabolic_efficiency < 7.5:
				metabolic_efficiency_bin_tallies[14] += 1
			else:
				metabolic_efficiency_bin_tallies[15] += 1
		output_results_organism_metabolic_efficiency_bins.write(
			str(global_variables.step_num) + ':\t' + '\t'.join([str(i) for i in metabolic_efficiency_bin_tallies]) + '\n')

		cellularity_bin_tallies = [0, 0, 0, 0, 0, 0, 0, 0, 0,
								   0]  # 0-0.1, 0.1-0.2, 0.2-0.3, 0.3-0.4, 0.4-0.5, 0.5-0.6, 0.6-0.7, 0.7-0.8, 0.8-0.9, 0.9-1
		for org in population_manager.organisms:
			if org.cellularity < 0.1:
				cellularity_bin_tallies[0] += 1
			elif org.cellularity < 0.2:
				cellularity_bin_tallies[1] += 1
			elif org.cellularity < 0.3:
				cellularity_bin_tallies[2] += 1
			elif org.cellularity < 0.4:
				cellularity_bin_tallies[3] += 1
			elif org.cellularity < 0.5:
				cellularity_bin_tallies[4] += 1
			elif org.cellularity < 0.6:
				cellularity_bin_tallies[5] += 1
			elif org.cellularity < 0.7:
				cellularity_bin_tallies[6] += 1
			elif org.cellularity < 0.8:
				cellularity_bin_tallies[7] += 1
			elif org.cellularity < 0.9:
				cellularity_bin_tallies[8] += 1
			else:
				cellularity_bin_tallies[9] += 1
		output_results_organism_cellularity_bins.write(
			str(global_variables.step_num) + ':\t' + '\t'.join([str(i) for i in cellularity_bin_tallies]) + '\n')

	if (global_variables.step_num) % 100 == 0:
		if len(population_manager.organisms) > 0:
			for org in population_manager.organisms:
				output_results_cellularity_vs_metabolic_efficiency.write(
					str(global_variables.step_num) + '\t' + str(org.cellularity) + '\t' + str(org.metabolic_efficiency) +'\n')
		else:
			output_results_cellularity_vs_metabolic_efficiency.write(str(global_variables.step_num) + ':\t' + 'None\tNone\n')
