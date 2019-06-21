
#!/usr/bin/env python

"""
This file is part of Simmerpop which is released under the GNU General Purpose License version 3. 
See COPYING or go to <https://www.gnu.org/licenses/> for full license details.
"""

import random

from . import cd_gene

__authors__ = ['Yuta A. Takagi', 'Diep H. Nguyen']
__copyright__ = 'Copyright 2019, Goldman Lab'
__license__ = 'GPLv3'


# this gene is designed for Yuta's model
#
# it is a gene that evaluates to the same value as the previous gene and writes that value to a food output


class GenePut(cd_gene.Gene):
	def __init__(self, organism, put_to):
		super().__init__(organism)
		self.put_to = put_to
		self.can_be_first_gene = False

	def __repr__(self):
		return 'p_' + str(self.put_to) + '_' + str(self.value)

	def execute(self):
		temp = self.organism.genome[self.organism.genome_read_head - 1].value
		self.organism.food.solution[self.put_to] = temp
		self.value = temp

	def test_execute(self, food, read_head):
		temp = self.organism.genome[read_head - 1].test_value
		food.solution[self.put_to] = temp
		self.test_value = temp

	def cost(self):
		return 1

	def mutate_pointer(self):
		self.put_to = random.randint(0, 7)
