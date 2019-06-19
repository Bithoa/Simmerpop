# custom_genome_manager_template.py
from ... import global_variables
from . import cd_genome_manager
from .gene_types import custom_gene_template
import random

__author__ = 'Yuta A. Takagi'


# global variables may be shared between all instances of the GenomeManager class
EXAMPLE_MUTATE_PROB = 0.001

# implement a method called init_script() if you would like to dynamically initialize global variables
def init_script():
    # you can define and pass key value pairs from the command line arguments.
    # Define the key in the form 'KEY' and access its value by calling
    # global_variables.parameters.get('KEY')
    global EXAMPLE_MUTATE_PROB
	EXAMPLE_MUTATE_PROB = float(global_variables.parameters.get('KEY_FOR_EXAMPLE_MUTATION_PROB'))
    # in the above example, you could override the default mutate prob of 0.001 from the command line by typing:
    # python3 run_simmerpop.py KEY_FOR_EXAMPLE_MUTATION_PROB 0.025

# a genome manager manages the global aspects of energy and interfaces between the population portion of the model. in
# addition to acting as an In/Out it also has methods involved in handling an organism's genome
# having a separate set of modules for gene functions allows for the mechanics of this part of the model to be
# independently changed without a need to alter the rest of the model.
# all genome managers should be child classes to the 'GenomeManager' class defined in the 'cd_genome_manager' module
class GenomeManager(cd_genome_manager.GenomeManager):  # this class name cannot be altered. Leave as 'GenomeManager'
    def __init__(self):
        # only one 'GenomeManager' instance is created. any custom variables can be defined here.
        # make sure to initialize from saved settings here if you'd like to add custom save functionality

        # the following example line creates a list to store discarded gene fragments
        self.trash = []

    def make_genome(self, organism):
        # this method is called when creating an instance of the 'Organism' (defined in the 'organism' module) de novo.
        # it should return a list of genes which represent that organism's initial 'genome'.

        # the following example lines returns a genome of ten 'GeneCustom' genes (a completely useless genome).
        temp_genes = []
        for i in range(10):
            temp_genes.append(custom_gene_template.GeneCustom(organism))
        return temp_genes

    def calculate_cellularity(self, organism):
        # this method is called to calculate the organism's 'cellularity' and should return a float between 0 and 1
        # representing the organism's cellularity.

        # the following example line returns a random cellularity value. note, usually you would want the cellularity to
        # be a function of the organism's genome.
        return random.random()

    def lose_genes(self, organism):
        # this function is called when the organism needs to lose genes from its genome. the genome must be edited
        # directly and can be accessed at 'organism.genome'.

        # the following example lines removes the last gene in the genome. the lost gene is added to the custom variable
        # 'self.trash'. if there are no genes remaining in the genome the 'organism.alive' flag is set to 'False'. the
        # 'organism.mutated' flag is set to 'True'. if the 'genome_read_head' was on the last gene, set it to 0.
        self.trash.append(organism.genome.pop(len(organism.genome) - 1))
        if len(organism.genome) == 0:
            organism.alive = False
        organism.mutated = True
        if organism.genome_read_head == len(organism.genome):
            organism.genome_read_head = 0

    def gain_genes(self, organism):
        # this function is called when the organism needs to gain genes to its genome. the genome must be edited
        # directly and can be accessed at 'organism.genome'.

        # the following example lines adds an 'GeneCustom' gene to the end of the genome. the 'organism.mutated' flag is
        # set to 'True'.
        organism.genome.append(custom_gene_template.GeneCustom(organism))
        organism.mutated = True

    def mutate(self, organism):
        # this function is called when the organism's genes need to be mutated. the genome must be edited directly and
        # can be accessed at 'organism.genome'.

        # the following example lines looks through the genome and checks if each gene is a 'GeneCustom' gene. if it is,
        # it is mutated with a probability of 1/1000. the mutation is a change of the 'gene.example' value to the string
        # 'Good bye'. if this occurs the 'organism.mutated' flag is set to 'True'
        for gene in organism.genome:
            if type(gene) is custom_gene_template.GeneCustom and random.random() < EXAMPLE_MUTATE_PROB:
                gene.example = 'Good bye'
                organism.mutated = True

    def init_gene_from_string_repr(self, organism, string_repr):
        # this method is used to create an instance of a 'gene' based on its string representation. this method really
        # only needs to be defined if you would like your custom 'Food' types to have the save functionality enabled.

        # the following example lines creates 'GeneCustom' instances based on their string representation. compare with
        # the 'GeneCustom' classes '__repr__()' method.
        repr_params = string_repr.split('_')
        to_return = None
        if repr_params[0] == 'example':
            to_return = custom_gene_template.GeneCustom(organism)
            if repr_params[2] == 'True':
                to_return.val = True
            elif repr_params[2] == 'False':
                to_return.val = False
            else:
                to_return.val = None
            to_return.example = repr_params[1]
        return to_return







    
