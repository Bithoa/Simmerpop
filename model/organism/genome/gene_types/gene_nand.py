# gene_nand.py
import random
from . import cd_gene

__author__ = 'Yuta A. Takagi'


# this gene is designed for Yuta's model
#
# it is a gene that looks at two previous genes given by relative position in 'pre_index_a' and 'pre_index_b' and
# evaluates to their boolean NAND


class GeneNAND(cd_gene.Gene):
	def __init__(self, organism, pre_index_a, pre_index_b):
		super().__init__(organism)
		self.pre_index_a = pre_index_a
		self.pre_index_b = pre_index_b
		self.can_be_first_gene = False

	def __repr__(self):
		return 'n_' + str(self.pre_index_a) + '_' + str(self.pre_index_b) + '_' + str(self.value)

	def execute(self):
		temp_a = self.organism.genome[self.organism.genome_read_head - self.pre_index_a].value
		temp_b = self.organism.genome[self.organism.genome_read_head - self.pre_index_b].value
		if temp_a is None or temp_b is None:
			self.value = None
		else:
			self.value = not (temp_a and temp_b)

	def test_execute(self, food, read_head):
		temp_a = self.organism.genome[read_head - self.pre_index_a].test_value
		temp_b = self.organism.genome[read_head - self.pre_index_b].test_value
		if temp_a is None or temp_b is None:
			self.value = None
		else:
			self.test_value = not (temp_a and temp_b)

	def cost(self):
		return 1

	def mutate_pointer_a(self):
		self.pre_index_a = None

	def mutate_pointer_b(self):
		self.pre_index_b = None

	def fix_pointers(self, index):
		if (self.pre_index_a is None) or (self.pre_index_a > index):
			self.pre_index_a = random.randint(1, index)
		if (self.pre_index_b is None) or (self.pre_index_b > index):
			self.pre_index_b = random.randint(1, index)
