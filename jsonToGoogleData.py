# -*-coding: utf-8 -*

import sys
import json
import importlib


def buildDataRow(name, birthDate, deathDate, childName, toolTip):
    # Beginning of line
    dataRow = '['

    # First attribute: name, composed of attributes v (ID) and f (displayed)
    # v: ID (name without ' and /). Two / delimit the surname
    dataRow = dataRow + '{ \'v\': \''
    dataRow = dataRow + name.replace('/', '').replace('\'', '\\\'')
    # f: Displayed (name without ' and / then dates styled with HTML)
    dataRow = dataRow + '\', \'f\': \''
    dataRow = dataRow + name.replace('/', '').replace('\'', '\\\'')
    dataRow = dataRow + '<div style="color:green; font-style:italic">'
    dataRow = dataRow + birthDate + '</div>'
    dataRow = dataRow + ' — '
    dataRow = dataRow + '<div style="color:red; font-style:italic">'
    dataRow = dataRow + deathDate
    dataRow = dataRow + '</div>\' }, \''

    # Second attribute: child name (without ' and /). Two / delimit the surname
    dataRow = dataRow + childName.replace('/', '').replace('\'', '\\\'')

    # Third attribute: tool tip
    dataRow = dataRow + '\', \'' + toolTip + '\''

    # End of line
    dataRow = dataRow + '],\n'
    return dataRow

# Build toolTip with the separator if needed


def buildToolTip(occupation, birthPlace, deathPlace, sex):
    SEPARATOR = ' - '
    if sex == 'F':
        endLetter = 'e'
    else:
        endLetter = ''

    toolTip = ''

    if occupation != '':
        toolTip = toolTip + occupation.replace('\'', '\\\'')
    if birthPlace != '':
        if occupation != '':
            toolTip = toolTip + SEPARATOR
        toolTip = toolTip + 'Né' + endLetter + \
            ' à '+birthPlace.replace('\'', '\\\'')
    if deathPlace != '':
        if birthPlace != '':
            toolTip = toolTip + SEPARATOR
        else:
            if occupation != '':
                toolTip = toolTip + SEPARATOR
        toolTip = toolTip + 'Mort' + endLetter + \
            ' à ' + deathPlace.replace('\'', '\\\'')

    # Not return an empty toolTip
    if toolTip == '':
        toolTip = ' - '
    return toolTip


# Safe: return empty string if the attribute is not present
def extractDictAttribute(data, attribute):
    if attribute in data:
        return data[attribute]
    else:
        return ''


# [
# [{ 'v': 'Mike', 'f': 'Mike<div style="color:red; font-style:italic">President</div>' }, '', 'The President'],
# [{ 'v': 'Jim', 'f': 'Jim<div style="color:red; font-style:italic">Vice President</div>' }, 'Mike', 'VP'],
# ['Alice', 'Mike', '']]
# ]
if __name__ == '__main__':
    print('- jsonToGoogleData - \n')

    # Debug mode
    DEBUG_MODE = False
    DEBUG_ORPHAN_NODE__NAME = 'DEBUG-ORPHAN'
    DEBUG_ORPHAN_NODE__TOOLTIP = 'Its parents are people which has not found their place in my tree yet'

    # Paths
    jsonPath = './RESULT.json'
    outPath = './googleRowsData.txt'

    # JSON file reading
    with open(jsonPath, 'r', encoding='utf-8') as jsonFile:
        jsonFileContent = jsonFile.read()
        jsonDict = json.loads(jsonFileContent)

    # Counters
    personCounter = 0
    solvedWarningCounter = 0
    warningCounter = 0
    infoCounter = 0

    # Constants
    # - Root
    treeConstantsModule = importlib.import_module('treeConstants')

    trueRootTreeName = treeConstantsModule.trueRootTreeName
    trueRootTreeBirthDate = treeConstantsModule.trueRootTreeBirthDate
    toolTip = buildToolTip(treeConstantsModule.trueRootTreeOccupation,
                           treeConstantsModule.trueRootTreeBirthDate, '', treeConstantsModule.trueRootTreeSex)
    falseRootTreeName = treeConstantsModule.falseRootTreeName
    parentsOfRootTreeName = treeConstantsModule.parentsOfRootTreeName

    # - Manual fixes, not covered by the algo
    # If one person have one of this person as child, it will not be added to prevent other trees to be displayed
    # Cause: I added children to the sibling of one of my ancestors
    forbiddenChildNames = treeConstantsModule.forbiddenChildNames

    # Begininning of the rows list
    dataRows = '[\n'

    # First row
    # I am the root, then I have no child, and I am not yet dead
    dataRow = buildDataRow(
        trueRootTreeName, trueRootTreeBirthDate, '', '', toolTip)
    dataRows = dataRows + dataRow

    if DEBUG_MODE:
        orphanDataRow = buildDataRow(
            DEBUG_ORPHAN_NODE__NAME, '', '', '', DEBUG_ORPHAN_NODE__TOOLTIP)
        dataRows = dataRows + orphanDataRow

    for person in jsonDict['children']:
        if person['type'] == 'INDI':
            dataRow = ''
            childName = ''
            toolTip = buildToolTip(
                extractDictAttribute(person['data'], 'OCCUPATION'),
                extractDictAttribute(person['data'], 'BIRTH/PLACE'),
                extractDictAttribute(person['data'], 'DEATH/PLACE'),
                extractDictAttribute(person['data'], 'SEX'))
            personName = person['data']['NAME']

            # Birth date with robustness
            if 'BIRTH/DATE' in person['data']:
                personBirthDate = person['data']['BIRTH/DATE']
            else:
                personBirthDate = ''

            # Death date with robustness
            if 'DEATH/DATE' in person['data']:
                personDeathDate = person['data']['DEATH/DATE']
            else:
                personDeathDate = ''

            # Avoid error for the tree root - childName will remain empty, and my sibling will not be added - i am the only root
            if personName != trueRootTreeName and personName != falseRootTreeName and '@FAMILY_SPOUSE' in person['data']:
                personFamilySpouse = person['data']['@FAMILY_SPOUSE']

                # Manually add me as my parent's son
                if personName in parentsOfRootTreeName:
                    childName = trueRootTreeName
                else:
                    # Look for the person which family child ID is the same as the person's family spouse ID in the JSON file: it will be one of my son
                    possibleSons = []
                    for possibleSonIter in jsonDict['children']:
                        if possibleSonIter['type'] == 'INDI':
                            possibleSonIterName = possibleSonIter['data']['NAME']
                            if possibleSonIterName != trueRootTreeName and '@FAMILY_CHILD' in possibleSonIter['data']:
                                personFamilyChild = possibleSonIter['data']['@FAMILY_CHILD']
                                if personFamilySpouse == personFamilyChild:
                                    # Store the different found son
                                    possibleSons.append(
                                        possibleSonIter['data'])
                    if len(possibleSons) == 0:
                        # No son found - does not have to be in the tree (unless there is an error)
                        print('INFO: ' + personName + ' has no son\n')
                        infoCounter = infoCounter + 1
                    elif len(possibleSons) == 1:
                        childName = possibleSons[0]['NAME']
                    else:
                        # Choose the correct son
                        print('WARNING: ' + personName +
                              ' has several sons:')
                        warningCounter = warningCounter + 1
                        # First loop: get the family ID built (as a spouse) by each candidate son
                        possibleSonsWhichHaveChildren = []
                        for eachSon in possibleSons:
                            print('  -' + eachSon['NAME'])
                            for possibleGrandSonIter in jsonDict['children']:
                                if possibleGrandSonIter['type'] == 'INDI':
                                    if possibleGrandSonIter['data']['NAME'] != trueRootTreeName:
                                        if '@FAMILY_CHILD' in possibleGrandSonIter['data'] and '@FAMILY_SPOUSE' in eachSon:
                                            if possibleGrandSonIter['data']['@FAMILY_CHILD'] == eachSon['@FAMILY_SPOUSE']:
                                                # The current item is a child of this candidate son: it is likely in my direct tree
                                                # (most siblings in my tree are dead branches without spouses and childs)
                                                if eachSon not in possibleSonsWhichHaveChildren:
                                                    # Avoid adding duplicate values
                                                    possibleSonsWhichHaveChildren.append(
                                                        eachSon)

                        if len(possibleSonsWhichHaveChildren) == 1:
                            # Only one candidate son have children: it is one of my ancestor
                            childName = possibleSonsWhichHaveChildren[0]['NAME']
                            print('SOLVED: '+childName)
                            warningCounter = warningCounter - 1
                            solvedWarningCounter = solvedWarningCounter + 1
                        else:
                            # Cannot find which son is the correct one
                            if DEBUG_MODE:
                                childName = DEBUG_ORPHAN_NODE__NAME

                        print('')

                # If a child have been found, add the person in the list
                # Else, it will be add as a parent to the DEBUG-ORPHAN node
                if childName != '':
                    # MANUAL CHANGE
                    if childName not in forbiddenChildNames:
                        dataRow = buildDataRow(
                            personName, personBirthDate, personDeathDate, childName, toolTip)
                        personCounter = personCounter+1

                dataRows = dataRows + dataRow

    # End of the rows list
    dataRows = dataRows + ']'

    # Writing the result in a file
    with open(outPath, 'w', encoding='utf-8') as outFile:
        outFile.write(dataRows)

    # Report
    print('Finished. '+str(warningCounter) +
          ' warning(s), '+str(solvedWarningCounter)+' solved problem(s), '+str(infoCounter)+' info(s).')
