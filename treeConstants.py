# -*-coding: utf-8 -*

# Used to be imported with importlib
__name__ = 'treeConstants'

# - Root
# Root of the tree
trueRootTreeName = 'Lucas /Luigi/'

# Parents of the root
parentsOfRootTreeName = {
    'Papa', 'Maman'}

# Sibling of the root, not displayed in the website
falseRootTreeName = 'Paul /Luigi/'

# - Manual fixes, not covered by the algo
# If one person have one of this person as child, it will not be added to prevent other trees to be displayed
# Cause: I added children to the sibling of one of my ancestors, or one of my ancestor has had several wives
forbiddenChildNames = ['Tatie /Lucy/']
