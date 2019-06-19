from ... import global_variables
from ... import population_manager
from ... import analytics
import itertools

__author__ = 'Yuta A. Takagi'


# holds the class definition for the 'FoodIO' parent class. see the 'custom_food_io_template' module for details
# change this module at your own risk


# variables for the 'make_food_id()' method
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
make_f_hash_depth = 1
make_f_hash_iterator = iter(ALPHA)


# makes a unique id for food
def make_food_id():
    global make_f_hash_depth
    global make_f_hash_iterator
    try:
        return 'f*' + ''.join(next(make_f_hash_iterator))
    except StopIteration:
        make_f_hash_depth += 1
        make_f_hash_iterator = itertools.product(ALPHA, repeat=make_f_hash_depth)
        return 'f*' + ''.join(next(make_f_hash_iterator))


# the 'FoodIO' parent class
class FoodIO:
    def __init__(self):
        pass
    def make_food_pool(self):
        raise NotImplementedError
    def add_food(self) :
        raise NotImplementedError
    def get_food(self):
        raise NotImplementedError

    def get_test_food(self):
        raise NotImplementedError

    def discard_food(self, food_to_discard):
        raise NotImplementedError

    def init_food_from_string_repr(self, string_repr):
        raise NotImplementedError
