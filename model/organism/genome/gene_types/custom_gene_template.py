from .... import global_variables
from . import cd_gene

__author__ = 'You!'


# ====================================================================================================
# ****************************************************************************************************


# ****************************************************************************************************
# ====================================================================================================


# change 'GeneCustom' to whatever you'd like to call your gene class
# all genes should be child classes to the 'Gene' class defined in the 'cd_gene' module
class GeneCustom(cd_gene.Gene):
    def __init__(self, organism):
        # this is the method called when creating instances of this class
        # all variables should be defined and initialized here
        #
        # this class inherits the following variables from its parent class 'Gene':
        # self.organism
        #   the 'Organism' (defined in the 'organism' module) who's genome this gene instance resides in.
        #   Should be set to 'None' if it is not within an organism.
        # self.value
        #   the value that this gene last evaluated to 'True', 'False', or if it has not been evaluated yet, 'None'.
        # self.test_value
        #   a temporary value analogous to 'self.value' used to calculate the 'genome_quality' of an 'Organism'.
        # self.can_be_first_gene
        #   a static boolean flag indicating whether this gene type is allowed to be the first gene in a genome.

        super().__init__(organism)  # this example line initializes variables using the 'Gene' class '__init__()' method

        self.can_be_first_gene = False  # this example line sets the 'can_be_first_gene' variable to 'False'

        self.example = 'Hello'  # this example line defines a variable 'example' unique to this gene type

    def __repr__(self):
        # this is the method called when a string representation of this gene is required (ex. if you print() this gene)
        # if you would like to enable saving functionality with your custom gene type you will need to create/modify
        # your 'GenomeManager' class to recreate this gene instance based the string representation returned here.

        # although you can handle this however you'd like, I would suggest you follow the format I have used in my gene
        # classes. a continuous string with each section separated by an underscore '_'. the first section is an
        # identifying string unique for this gene type. the last section is the current 'self.value'. all other
        # variables fall between.

        return 'example_' + str(self.example) + '_' + str(self.value)

    def execute(self):
        # this method is called to evaluate its value

        # for example, you could set the value to true if the 'example' variable equals the string 'Hello'
        self.value = (self.example == 'Hello')

        # or you could do an operation based on previous genes in the genome, the following example evaluates to the
        # inverse of the value of the previous gene. 'self.organism.genome' accesses the 'genome' of the 'organism' this
        # gene belongs to. 'self.organism.read_head' is the current 'read_head' position (the location of this gene when
        # executed. thus 'self.organism.genome[self.organism.read_head - 1].value' accesses the value of the previous
        # gene.
        self.value = not self.organism.genome[self.organism.read_head - 1].value

    def test_execute(self, food, read_head):
        # this method is called to evaluate the value when calculating the 'genome_quality' and should have identical
        # functionality to the 'execute()' method but write to the 'test_value' so as not to disrupt any ongoing
        # non-test operations. a test 'food' and 'read_head' are given and should be used in place of
        # 'self.organism.food' and 'self.organism.read_head' if necessary.

        self.test_value = (self.example == 'Hello')

        self.test_value = not self.organism.genome[read_head - 1].test_value

    def cost(self):
        # this method should return the cost of executing the gene
        return 1
