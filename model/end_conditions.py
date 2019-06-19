# end_conditions.py
from . import global_variables
from . import population_manager
from . import analytics
import time

__author__ = 'Yuta A. Takagi (2016) & Diep H. Nguyen (2018)'


# defines a number of functions to end the model when specific conditions are met


# user defined static variables
# ====================================================================================================
# ****************************************************************************************************

NUM_STEPS = 100000  # the maximum number of steps

RUN_TIME = 6000  # the maximum runtime in minutes

# ****************************************************************************************************
# ====================================================================================================


# end condition static variables
START_TIME = None
END_TIME = None

# end condition variables
continue_run = None


# initialize the end conditions
def init_end_conditions():
  	# populate the dictionary named 'parameters' from the command line arguments
    global NUM_STEPS
    global RUN_TIME
    if 'MAX_NUM_STEPS' in global_variables.parameters.keys():
        NUM_STEPS = int(global_variables.parameters.get('MAX_NUM_STEPS'))
    if 'MAX_RUN_TIME' in global_variables.parameters.keys():
        RUN_TIME = int(global_variables.parameters.get('MAX_RUN_TIME'))

    global continue_run
    continue_run = True
    start_timer()


# stops the model if it exceeds a maximum step count
def check_max_step():
    if global_variables.step_num >= NUM_STEPS:
        global continue_run
        continue_run = False
        analytics.exit_line = 'step_count_executed\nstep_num: ' + str(global_variables.step_num)


# begins the timer for the 'check_timeout()' method
def start_timer():
    global START_TIME
    global END_TIME
    global RUN_TIME
    START_TIME = time.time()
    END_TIME = START_TIME + 60 * RUN_TIME


# stops the model if it exceeds a maximum runtime
def check_timeout():
    global END_TIME
    global continue_run
    if time.time() > END_TIME:  # end program if time limit is exceeded
        continue_run = False
        analytics.exit_line = 'time_limit_reached\nstep_num: ' + str(global_variables.step_num)


# stops the model if there are no organisms left alive
def check_ecosystem_alive():
    global continue_run
    if len(population_manager.organisms) == 0:
        continue_run = False
        analytics.exit_line = 'ecosystem_has_died\nstep_num: ' + str(global_variables.step_num)
