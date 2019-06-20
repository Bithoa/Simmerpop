# cd_gene.py

__author__ = 'Yuta A. Takagi'


# holds the class definition for the 'Gene' parent class. see the 'custom_gene_template' module for details.
# change this module at your own risk


# the 'Gene' parent class
class Gene:
	def __init__(self, organism):
		self.organism = organism
		self.value = None
		self.test_value = None
		self.can_be_first_gene = None

	def __repr__(self):
		raise NotImplementedError

	def execute(self):	# does the action of the gene
		raise NotImplementedError

	def test_execute(self, food, read_head):
		raise NotImplementedError

	def cost(self):
		raise NotImplementedError
