from ..food_types import cd_food_type
from ..food_io import food_io_basic
from ... import population_manager
import random

__author__ = 'Yuta A. Takagi'


# this food type is designed for Yuta's model
#
# the solution is the simple inverse (boolean not) of each input position
# the reward is the number of correct solutions raised to the power of 3, minus a dynamically adapting quantity who's
# value increases if the population is healthy, but decreases if organisms are dying


# ====================================================================================================
# ****************************************************************************************************


# ****************************************************************************************************
# ====================================================================================================


reduction_factor = 0


def calc_food_payoff_reduction_factor():
    global reduction_factor
    if len(population_manager.organisms) > (population_manager.POPULATION_CAP):
        reduction_factor += 1
    if len(population_manager.organisms) <= (population_manager.POPULATION_CAP * 0.5):
        reduction_factor -= 1


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
        # reward = 25 * (math.sin(math.pi / 8 * num_correct - math.pi / 2) + 1)
        # if master.step_num < 24000:
        #     reward = (num_correct**3) - (master.step_num*0.01)
        # else:
        #     reward = (num_correct**3) - (24000 * 0.01)
        
        reward = (num_correct ** 3) - (reduction_factor * 0.1)
        #reward = (num_correct ** 2.5) #no reduction_factor
        if reward < 0:
            reward = 0
        # reward = (num_correct**2.25)
        # reward = (num_correct**3)/4
        # reward = (num_correct**4)/20
        if self.position_solved == [True, True, True, True, True, True, True, True]:
            self.spent = True
        to_return = [num_correct, reward]
        self.quality -= num_correct
        return to_return
