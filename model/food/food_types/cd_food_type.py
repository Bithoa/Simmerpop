from ... import global_variables
from ... import population_manager
from ... import analytics

__author__ = 'Yuta A. Takagi'


# holds the class definition for the 'Food' parent class. see the 'custom_food_template' module for details
# change this module at your own risk


# the 'Food' parent class
class Food:
    def __init__(self):
        self.inputs = [None, None, None, None, None, None, None, None]
        self.solution = [None, None, None, None, None, None, None, None]
        self.id = None

    def __repr__(self):
        raise NotImplementedError

    def check_solution(self):
        raise NotImplementedError
