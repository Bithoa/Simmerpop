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
# it is a gene that reads from an food input and evaluates to that value


class GeneGet(cd_gene.Gene):
	def __init__(self, organism, get_from):
		super().__init__(organism)
		self.get_from = get_from
		self.can_be_first_gene = True

	def __repr__(self):
		return 'g_' + str(self.get_from) + '_' + str(self.value)

	def execute(self):
		self.value = self.organism.food.inputs[self.get_from]

	def test_execute(self, food, read_head):
		self.test_value = food.inputs[self.get_from]

	def cost(self):
		return 1

	def mutate_pointer(self):
		self.get_from = random.randint(0, 7)
