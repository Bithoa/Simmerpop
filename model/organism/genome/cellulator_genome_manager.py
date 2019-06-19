# .py
from ... import global_variables
from . import cd_genome_manager
from .gene_types import gene_get, gene_put, gene_nand, gene_cellularity
import random
import itertools
import os
import re

__author__ = 'Yuta A. Takagi (2016) & Diep H. Nguyen (2018)'


# this genome manager is designed for the Cellulator study (!!insert publication reference here) and utilizes the following gene types:
# GeneCellularity
# GeneGet
# GeneNAND
# GenePut
#
# it maintains a pool of loose genome fragments outside of organisms. genome fragments can passively move in and out of
# organisms from this pool if the organism has a low cellularity value


# ====================================================================================================
# ****************************************************************************************************

LOOSE_GENE_POOL_CAP = 1000  # max number of loose genome fragments

MUTATION_PROB = 0.005 # the probability of mutation

POINTER_MUT_PROB = MUTATION_PROB  # probability of a gene pointer mutating

DELETION_PROB = MUTATION_PROB  # probability of a gene being deleted

INSERTION_PROB = MUTATION_PROB # probability of a gene being inserted between each gene
INS_GET_WT = 10  # the relative proportion of 'GeneGet' genes being inserted
INS_PUT_WT = 10  # the relative proportion of 'GenePut' genes being inserted
INS_NAND_WT = 30  # the relative proportion of 'GeneNAND' genes being inserted
INS_CELL_WT = 5  # the relative proportion of 'GeneCellularity' genes being inserted

GENOME_BREAK_PROB = 0.1  # probability of a genome fragmenting after each gene
NUM_CELLGENES = 0 # initial number of cellularity genes in the starting genome
HGT_PROB = 0.5 # probability of horizontal gene transfer
# ****************************************************************************************************
# ====================================================================================================


# initialize the global variables
def init_script():
    if 'LOOSE_GENE_POOL_CAP' in global_variables.parameters.keys():
        LOOSE_GENE_POOL_CAP = int(global_variables.parameters.get('LOOSE_GENE_POOL_CAP'))
    if 'MUTATION_PROB' in global_variables.parameters.keys():
        MUTATION_PROB = float(global_variables.parameters.get('MUTATION_PROB'))

    POINTER_MUT_PROB = MUTATION_PROB
    DELETION_PROB = MUTATION_PROB
    INSERTION_PROB = MUTATION_PROB
    if 'POINTER_MUT_PROB' in global_variables.parameters.keys():
        POINTER_MUT_PROB = float(global_variables.parameters.get('POINTER_MUT_PROB'))
    if 'DELETION_PROB' in global_variables.parameters.keys():
        DELETION_PROB = float(global_variables.parameters.get('DELETION_PROB'))
    if 'INSERTION_PROB' in global_variables.parameters.keys():
        INSERTION_PROB = float(global_variables.parameters.get('INSERTION_PROB'))
    if 'INS_GET_WT' in global_variables.parameters.keys():
        INS_GET_WT = int(global_variables.parameters.get('INS_GET_WT'))
    if 'INS_PUT_WT' in global_variables.parameters.keys():
        INS_PUT_WT = int(global_variables.parameters.get('INS_PUT_WT'))
    if 'INS_NAND_WT' in global_variables.parameters.keys():
        INS_NAND_WT = int(global_variables.parameters.get('INS_NAND_WT'))
    if 'INS_CELL_WT' in global_variables.parameters.keys():
        INS_CELL_WT = int(global_variables.parameters.get('INS_CELL_WT'))
    if 'GENOME_BREAK_PROB' in global_variables.parameters.keys():
        GENOME_BREAK_PROB = float(global_variables.parameters.get('GENOME_BREAK_PROB'))
    if 'NUM_CELLGENES' in global_variables.parameters.keys():
        NUM_CELLGENES = int(global_variables.parameters.get('NUM_CELLGENES'))
    if 'HGT_PROB' in global_variables.parameters.keys():
        HGT_PROB = float(global_variables.parameters.get('HGT_PROB'))


# the cellulator genome manager class
class GenomeManager(cd_genome_manager.GenomeManager):
    # initializes the instance
    def __init__(self):
        self.loose_genome_fragments = []

    # creates a genome of:
    # 8 GeneGet genes, one mapped to each input
    # 16 randomized GeneNAND genes
    # 8 GenePut genes, one mapped to each output
    # and a number of GeneCellularity genes defined by NUM_CELLGENES
    def make_genome(self, organism):
        # make random genes
        temp_genes = []
        for i in range(8):
            temp_genes.append(gene_get.GeneGet(organism, i))
            temp_genes.append(gene_nand.GeneNAND(organism, random.randint(1, len(temp_genes)), random.randint(1, len(temp_genes))))
            temp_genes.append(gene_nand.GeneNAND(organism, random.randint(1, len(temp_genes)), random.randint(1, len(temp_genes))))
            temp_genes.append(gene_put.GenePut(organism, i))
        for i in range(NUM_CELLGENES):
            temp_genes.append(gene_cellularity.GeneCellularity(organism))
        return temp_genes

    # calculates the cellularity as 1 - 0.5^(# of cellularity genes)
    def calculate_cellularity(self, organism):
        if len(organism.genome) > 0:
            cellularity_gene_tally = 0
            for gene in organism.genome:
                if type(gene) is gene_cellularity.GeneCellularity:
                    cellularity_gene_tally += 1
            return 1 - 0.5 ** cellularity_gene_tally
        else:
            return 0  # if there is no genome, hard code to 0 probability?

    # returns a list of the genome broken up randomly according to the GENOME_BREAK_PROB
    def break_genome(self, organism):
        to_return = []
        temp_fragment = []
        for gene in organism.genome:
            if random.random() < GENOME_BREAK_PROB:  # if it breaks
                temp_fragment.append(gene)
                to_return.append(temp_fragment)
                temp_fragment = []
            else:
                temp_fragment.append(gene)
        if len(temp_fragment) > 0:
            to_return.append(temp_fragment)
        return to_return

    # causes the organism to lose a random gene segment according to the HGT_PROB
    def lose_genes(self, organism):
        if random.random() < HGT_PROB:
            my_fragments = self.break_genome(organism)
            if len(my_fragments) == 1:  # if there is only one fragment, remove it
                remove_at = 0
            elif my_fragments[1][0].can_be_first_gene:  # if there are more than one fragment and the second fragment
                # begins with a Gene that can_be_first_gene, remove any random fragment
                remove_at = random.randint(0, len(my_fragments) - 1)
            else:  # otherwise remove any random fragment except the first
                remove_at = random.randint(1, len(my_fragments) - 1)
            deletion_index_left = len(list(itertools.chain.from_iterable(my_fragments[:remove_at])))
            deletion_index_right = len(list(itertools.chain.from_iterable(my_fragments[:remove_at + 1])))
            removed_section = my_fragments.pop(remove_at)
            for gene in removed_section:
                gene.organism = None
            self.loose_genome_fragments.append(removed_section)
            organism.genome = list(itertools.chain.from_iterable(my_fragments))
            # if genome_read_head is right of deleted section
            if organism.genome_read_head >= deletion_index_right:
                organism.genome_read_head -= len(removed_section)
            # if genome_read_head is in the middle of the deleted section
            elif organism.genome_read_head >= deletion_index_left:
                organism.genome_read_head = deletion_index_left
                if organism.genome_read_head == len(organism.genome):
                    organism.genome_read_head = 0
            if len(organism.genome) == 0:
                organism.alive = False
            organism.mutated = True

    # causes the organism to gain a random gene segment according to the HGT_PROB
    def gain_genes(self, organism):
        if random.random() < HGT_PROB:
            if len(self.loose_genome_fragments) > 0:  # if gene is gained
                my_fragments = self.break_genome(organism)
                get_from = random.randint(0, len(self.loose_genome_fragments) - 1)
                section_to_insert = self.loose_genome_fragments.pop(get_from)
                for gene in section_to_insert:
                    gene.organism = organism
                if section_to_insert[0].can_be_first_gene:  # insert at beginning only if the section begins with a Gene
                    # that can_be_first_gene
                    insert_at = random.randint(0, len(my_fragments))
                else:  # otherwise insert anywhere but the beginning
                    insert_at = random.randint(1, len(my_fragments))
                insertion_index = len(list(itertools.chain.from_iterable(my_fragments[:insert_at])))
                my_fragments.insert(insert_at, section_to_insert)
                organism.genome = list(itertools.chain.from_iterable(my_fragments))
                if organism.genome_read_head >= insertion_index:
                    organism.genome_read_head += len(section_to_insert)
                organism.mutated = True

    # randomly removes gene fragments from the environmental gene pool if their number exceeds the LOOSE_GENE_POOL_CAP
    def cull_genome_fragments_pool(self):
    	# remove random gene fragments if over gene pool cap
    	while len(self.loose_genome_fragments) > LOOSE_GENE_POOL_CAP:
            remove_me = random.randint(0, len(self.loose_genome_fragments) - 1)
            self.loose_genome_fragments.pop(remove_me)

    # causes point mutations in the genome according to the various mutation probabilities
    def mutate(self, organism):
        # Mutating pointers in genes
        for gene in organism.genome:
            if type(gene) is gene_get.GeneGet and random.random() < POINTER_MUT_PROB:
                gene.mutate_pointer()
                organism.mutated = True
            elif type(gene) is gene_put.GenePut and random.random() < POINTER_MUT_PROB:
                gene.mutate_pointer()
                organism.mutated = True
            elif type(gene) is gene_nand.GeneNAND:
                if random.random() < POINTER_MUT_PROB:
                    gene.mutate_pointer_a()
                    organism.mutated = True
                if random.random() < POINTER_MUT_PROB:
                    gene.mutate_pointer_b()
                    organism.mutated = True

        # Deleting genes
        i = 0
        while i < len(organism.genome):
            if random.random() < DELETION_PROB:
                # don't delete first Gene if second Gene isn't can_be_first_gene
                if len(organism.genome) == 1:
                    organism.alive = False
                    organism.mutated = True
                elif not (i == 0 and not organism.genome[1].can_be_first_gene):
                    organism.genome.pop(i)
                    # if gene is deleted before genome_read_head, adjust genome_read_head to shift with the genes
                    if organism.genome_read_head > i:
                        organism.genome_read_head -= 1
                    # if last gene in genome is deleted, and genome_read_head exceeds the new genome size, reset
                    # genome_read_head
                    elif organism.genome_read_head >= len(organism.genome):
                        organism.genome_read_head = 0
                    i -= 1
                organism.mutated = True
            i += 1
        if len(organism.genome) == 0:
            organism.alive = False

        # Inserting genes
        ins_total_wt = INS_GET_WT + INS_PUT_WT + INS_NAND_WT + INS_CELL_WT
        i = 0
        while i < len(organism.genome):
            # insert GeneGet
            if random.random() < INSERTION_PROB:
                if random.random() < INS_GET_WT / ins_total_wt:
                    organism.genome.insert(i, gene_get.GeneGet(organism, random.randint(0, 7)))
                    # if gene is inserted before genome_read_head, adjust genome_read_head to shift with the genes
                    if organism.genome_read_head > i:
                        organism.genome_read_head += 1
                    i += 1
                elif i != 0 and random.random() < INS_PUT_WT / (ins_total_wt - INS_GET_WT):
                    organism.genome.insert(i, gene_put.GenePut(organism, random.randint(0, 7)))
                    if organism.genome_read_head > i:
                        organism.genome_read_head += 1
                    i += 1
                elif i != 0 and random.random() < INS_NAND_WT / (ins_total_wt - INS_GET_WT - INS_PUT_WT):
                    organism.genome.insert(i, gene_nand.GeneNAND(organism, None, None))
                    if organism.genome_read_head > i:
                        organism.genome_read_head += 1
                    i += 1
                elif i != 0 and random.random() < INS_CELL_WT / (ins_total_wt - INS_GET_WT - INS_PUT_WT - INS_NAND_WT):
                    organism.genome.insert(i, gene_cellularity.GeneCellularity(organism))
                    if organism.genome_read_head > i:
                        organism.genome_read_head += 1
                    i += 1
                organism.mutated = True
            i += 1

        if len(organism.genome) == 0:
            organism.alive = False
	
	fix_pointers(organism)

    # repairs pointers in a genome that have been broken due to mutations
    def fix_pointers(self, organism):
        for i, gene in enumerate(organism.genome):
            if type(gene) is gene_nand.GeneNAND:
                gene.fix_pointers(i)

    # returns a Gene initialized from a string representation
    def init_gene_from_string_repr(self, organism, string_repr):
        repr_params = string_repr.split('_')
        to_return = None
        if repr_params[0] == 'g':
            to_return = gene_get.GeneGet(organism, int(repr_params[1]))
            if repr_params[2] == 'True':
                to_return.val = True
            elif repr_params[2] == 'False':
                to_return.val = False
            else:
                to_return.val = None
        elif repr_params[0] == 'p':
            to_return = gene_put.GenePut(organism, int(repr_params[1]))
            if repr_params[2] == 'True':
                to_return.val = True
            elif repr_params[2] == 'False':
                to_return.val = False
            else:
                to_return.val = None
        elif repr_params[0] == 'n':
            to_return = gene_nand.GeneNAND(organism, int(repr_params[1]), int(repr_params[2]))
            if repr_params[3] == 'True':
                to_return.val = True
            elif repr_params[3] == 'False':
                to_return.val = False
            else:
                to_return.val = None
        elif repr_params[0] == 'c':
            to_return = gene_cellularity.GeneCellularity(organism)
            if repr_params[1] == 'True':
                to_return.val = True
            elif repr_params[1] == 'False':
                to_return.val = False
            else:
                to_return.val = None
        return to_return
