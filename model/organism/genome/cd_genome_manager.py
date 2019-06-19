# cd_genome_manager.py
from ... import global_variables
import itertools

__author__ = 'Yuta A. Takagi'


# holds the class definition for the 'GenomeManager' parent class. see the 'custom_genome_manager_template' module for
# details. change this module at your own risk
# variables for the 'make_gene_id()' method

ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
make_g_hash_depth = 1
make_g_hash_iterator = iter(ALPHA)


# makes a unique id for gene fragments
def make_gene_id():
    global ALPHA
    global make_g_hash_depth
    global make_g_hash_iterator
    try:
        return 'g*' + ''.join(next(make_g_hash_iterator))
    except StopIteration:
        make_g_hash_depth += 1
        make_g_hash_iterator = itertools.product(ALPHA, repeat=make_g_hash_depth)
        return 'g*' + ''.join(next(make_g_hash_iterator))


# the 'GenomeManager' parent class
class GenomeManager:
    def __init__(self):
        pass

    def make_genome(self, organism):
        raise NotImplementedError

    def calculate_cellularity(self, organism):
        raise NotImplementedError

    def lose_genes(self, organism):
        raise NotImplementedError

    def gain_genes(self, organism):
        raise NotImplementedError

    def mutate(self, organism):
        raise NotImplementedError

    def init_gene_from_string_repr(self, organism, string_repr):
        raise NotImplementedError
