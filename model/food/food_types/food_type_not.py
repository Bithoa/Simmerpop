from ..food_types import cd_food_type
from ..food_io import food_io_basic
from ... import population_manager
import random

__author__ = 'Yuta A. Takagi'


# this food type is designed for Yuta's model
#
# the solution is the simple inverse (boolean not) of each input position
# the reward is the number of correct solutions raised to a power (3 by default), minus a dynamically adapting quantity who's
# value increases if the population is healthy, but decreases if organisms are dying


FOODNOT_BASE_PAYOFF_EXPONENT = 3
FOODNOT_PAYOFF_ADJUSTMENT_FACTOR = 0.1
FOODNOT_REDUCE_PAYOFF_WHEN_OVER = 1.0
FOODNOT_INCREASE_PAYOFF_WHEN_UNDER = 0.5

adjustment = 0

class FoodNot(cd_food_type.Food):  # the not of the input #NO REDUCTION FACTOR
    def __init__(self):
        super().__init__()
        for i in range(8):
            self.inputs[i] = random.choice([True, False])
        self.position_solved = [False, False, False, False, False, False, False, False]
        self.quality = 8
        self.spent = False

    def __repr__(self):
        return 'FoodNot_' + str(self.inputs) + '_' + str(self.solution)

    def check_solution(self):
        if self.spent:
            raise Exception('bad!!!!!!')
        correct_solution = []
        for val in self.inputs:
            correct_solution.append(not val)
        num_correct = 0
        for i in range(8):
            if (not self.position_solved[i]) and (self.solution[i] is not None):
                if self.solution[i] == correct_solution[i]:
                    num_correct += 1
                    self.position_solved[i] = True
                    
        reward = calc_food_payoff(num_correct)
        
        if self.position_solved == [True, True, True, True, True, True, True, True]:
            self.spent = True
        to_return = [num_correct, reward]
        self.quality -= num_correct
        return to_return
    
    def calc_food_payoff(self.num_correct)
        global FOODNOT_BASE_PAYOFF_EXPONENT
        global FOODNOT_PAYOFF_ADJUSTMENT_FACTOR
        reward = (num_correct ** FOODNOT_BASE_PAYOFF_EXPONENT) - (adjustment * FOODNOT_PAYOFF_ADJUSTMENT_FACTOR)
        if reward < 0:
            reward = 0
            
    def calc_food_payoff_reduction_factor():
        global adjustment
        if len(population_manager.organisms) > (population_manager.POPULATION_CAP):
            adjustment += 1
        if len(population_manager.organisms) <= (population_manager.POPULATION_CAP * 0.5):
            adjustment -= 1

