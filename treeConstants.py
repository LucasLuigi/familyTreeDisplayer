# -*-coding: utf-8 -*

__name__ = 'treeConstants'

# - Root
# Root of the tree
trueRootTreeName = 'Lucas /Luigi/'
trueRootTreeBirthDate = '01 JAN 2000'
trueRootTreeOccupation = 'Développeur'
trueRootTreeBirthDate = 'Ville, 75000, Paris, IDF, France'
trueRootTreeSex = 'M'

# Parents of the root
parentsOfRootTreeName = {
    'Papa', 'Maman'}

# Sibling of the root, not displayed in the website
falseRootTreeName = 'Paul /Luigi/'

# - Manual fixes, not covered by the algo
# If one person have one of this person as child, it will not be added to prevent other trees to be displayed
# Cause: I added children to the sibling of one of my ancestors
forbiddenChildNames = {'Tatie /Lucy/'}
