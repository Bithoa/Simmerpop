from ... import global_variables
from ... import population_manager
from ... import analytics
from . import cd_food_io
from ..food_types import custom_food_template

__author__ = 'Yuta A. Takagi'


# a food In/Out manages the global aspects of food and interfaces between the population portion of the model.
# having a separate set of modules for food allows for the mechanics of this part of the model to be independently
# changed without a need to alter the rest of the model.


# ====================================================================================================
# ****************************************************************************************************


# ****************************************************************************************************
# ====================================================================================================


# all food In/Outs should be child classes to the 'FoodIO' class defined in the 'cd_food_io' module
class FoodIO(cd_food_io.FoodIO):  # this class name cannot be altered. Leave as 'FoodIO'
    def __init__(self):
        # only one 'FoodIO' instance is created. any custom variables can be defined here.
        # make sure to initialize from saved settings here if you'd like to add custom save functionality

        # the following example line creates a list to store the discarded food
        self.trash = []

    def get_food(self):
        # this method is called when an organism requires a 'Food' and should return an instance of a child of the
        # 'Food' object defined in the 'cd_food_type' module

        # this example line returns a food of the type 'FoodCustom'
        return custom_food_template.FoodCustom()

    def get_test_food(self):
        # this method is called to calculate the 'genome_quality' and should behave identically to the 'get_food()'
        # method without affecting any aspects of the global food.

        return custom_food_template.FoodCustom()

    def discard_food(self, food_to_discard):
        # this method is called when an organism is discarding a 'Food'

        # following example line adds the discarded food to the cample variable 'self.trash'
        self.trash.append(food_to_discard)

    def init_food_from_string_repr(self, string_repr):
        # this method is used to create an instance of a 'Food' based on its string representation. this method really
        # only needs to be defined if you would like your custom 'Food' types to have the save functionality enabled.

        # the following example lines creates 'FoodCustom' instances based on their string representation. compare with
        # the 'FoodCustom' classes '__repr__()' method.
        repr_params = string_repr.split('_')
        to_return = None
        if repr_params[0] == 'FoodCustom':
            to_return = custom_food_template.FoodCustom()
            to_return.inputs = [input_as_string == 'True' for input_as_string in repr_params[1].strip('[]').split(', ')]
            to_return.solution = \
                [None if solution_as_string == 'None' else solution_as_string == 'True'
                 for solution_as_string in repr_params[2].strip('[]').split(', ')]
            to_return.example = str(repr_params[3])
        return to_return
