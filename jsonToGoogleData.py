# -*-coding: utf-8 -*

import sys
import json
import importlib

from enum import Enum

# Debug mode
# Choosed in __main__
DEBUG_MODE = False
birthDatesList = ''
deathDatesList = ''


# Display mode
class displayMode(Enum):
    COMPLETE = 0
    BIRTHPLACE = 1


appliedDisplayMode = displayMode.COMPLETE

# Variabled for the checker
idNameDict = {}
childrenDict = {}


def buildDataRow(id, name, nickname, birthDate, birthPlace, deathDate, childId, toolTip):
    global childrenDict
    # Debug
    global DEBUG_MODE
    global birthDatesList
    global deathDatesList
    if DEBUG_MODE:
        if birthDate != '':
            birthDatesList = birthDatesList + formatDate(birthDate) + '\n'
        if deathDate != '':
            deathDatesList = deathDatesList + formatDate(deathDate) + '\n'

     # Beginning of line
    dataRow = '['

    # First attribute: name, composed of attributes v (ID) and f (displayed)
    # v: ID (name without ' and /). Two / delimit the surname
    dataRow = dataRow + '{ \'v\': \''
    dataRow = dataRow + id
    # f: Displayed (name without ' and /. Dates are stylized with HTML)
    dataRow = dataRow + '\', \'f\': \''
    if appliedDisplayMode == displayMode.COMPLETE:
        dataRow = dataRow + name.replace('\'', '\\\'').replace('/', '')
        if nickname != "":
            dataRow = dataRow + ", dit " + nickname
        dataRow = dataRow + '<br><br><div style="color:green; font-style:italic">'
        dataRow = dataRow + formatDate(birthDate) + '</div>'
        dataRow = dataRow + ' — '
        dataRow = dataRow + '<div style="color:red; font-style:italic">'
        dataRow = dataRow + formatDate(deathDate)
        dataRow = dataRow + '</div>'
    elif appliedDisplayMode == displayMode.BIRTHPLACE:
        if birthPlace == '':
            birthPlace = '?'
        # FIXME Does not work very well - split not used
        birthCity = birthPlace.split(', ')[0]
        dataRow = dataRow + birthPlace.replace('\'', '\\\'')
    dataRow = dataRow + '\' }, \''

    # Second attribute: child name (without ' and /). Two / delimit the surname
    dataRow = dataRow + childId.replace('\'', '\\\'').replace('/', '')

    # Third attribute: tool tip
    dataRow = dataRow + '\', \'' + toolTip + '\''

    # End of line
    dataRow = dataRow + '],\n'

    # Checker variables assignation
    if childId not in childrenDict:
        childrenDict[childId] = 1
    else:
        childrenDict[childId] = childrenDict[childId] + 1
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
def extractSecureDictAttribute(data, attribute):
    if attribute in data:
        return data[attribute]
    else:
        return ''


def formatDate(date):
    # Lowering case
    formattedDate = str.lower(date)

    # Translating months when it is necessary
    formattedDate = formattedDate.replace('feb', 'fev')
    formattedDate = formattedDate.replace('apr', 'avr')
    formattedDate = formattedDate.replace('may', 'mai')
    formattedDate = formattedDate.replace('jun', 'jui')
    formattedDate = formattedDate.replace('aug', 'aou')

    # Replacing about, after, before and between
    formattedDate = formattedDate.replace('abt ', '~')
    formattedDate = formattedDate.replace('aft', '>')
    formattedDate = formattedDate.replace('bef', '<')
    if formattedDate.find('bet') != -1:
        formattedDate = formattedDate.replace('bet ', '[')
        formattedDate = formattedDate.replace('and', '-')
        formattedDate = formattedDate + ']'

    return formattedDate


def checker(jsonDict):
    global childrenDict
    global idNameDict
    output = True

    for childId in childrenDict:
        if childrenDict[childId] > 2:
            # One person is the child of more than two people ; biologically impossible
            print('CHECKER ERROR: '+idNameDict[childId].replace('/', '')+' has ' +
                  str(childrenDict[childId])+' parents.')
    print('')
    return output


# [
# [{ 'v': 'Mike', 'f': 'Mike<div style="color:red; font-style:italic">President</div>' }, '', 'The President'],
# [{ 'v': 'Jim', 'f': 'Jim<div style="color:red; font-style:italic">Vice President</div>' }, 'Mike', 'VP'],
# ['Alice', 'Mike', '']]
# ]
if __name__ == '__main__':
    print('- jsonToGoogleData - \n')

    # Debug mode
    DEBUG_ORPHAN_NODE__NAME = 'DEBUG-ORPHAN'
    DEBUG_ORPHAN_NODE__ID = '@IDEBUG@'
    DEBUG_ORPHAN_NODE__TOOLTIP = 'Its parents are people which has not found their place in my tree yet'

    # Paths
    jsonPath = './RESULT.json'
    outPath = './googleRowsData.txt'

    # JSON file reading
    with open(jsonPath, 'r', encoding='utf-8') as jsonFile:
        jsonFileContent = jsonFile.read()
        jsonDict = json.loads(jsonFileContent)

    # Counters
    personInTheHtmlTreeCounter = 0
    personInTheJsonTreeCounter = 0
    solvedWarningCounter = 0
    warningCounter = 0
    infoCounter = 0

    # Constants
    # - Log
    WARNING_LOG_PREFIX = 'WARNING: '
    SOLVED_LOG_PREFIX = 'SOLVED: '

    # - Root
    treeConstantsModule = importlib.import_module('treeConstants')

    trueRootTreeName = treeConstantsModule.trueRootTreeName
    falseRootTreeName = treeConstantsModule.falseRootTreeName
    parentsOfRootTreeName = treeConstantsModule.parentsOfRootTreeName

    # - Manual fixes, not covered by the algo
    # If one person have one of this person as child, it will not be added to prevent other trees to be displayed
    # Cause: I added children to the sibling of one of my ancestors
    forbiddenChildNames = treeConstantsModule.forbiddenChildNames

    forbiddenChildNumber = len(forbiddenChildNames)
    forbiddenChildIds = [''] * forbiddenChildNumber

    # Begininning of the rows list
    dataRows = '[\n'

    flagRootFound = False
    flagCounterforbiddenChildFound = forbiddenChildNumber

    # Extracting misc. informations
    for person in jsonDict['children']:
        # Building a (id, name) dict
        if person['type'] == 'INDI':
            idNameDict[person['data']['xref_id']] = person['data']['NAME']
            personInTheJsonTreeCounter = personInTheJsonTreeCounter + 1
            # Extracting the root's other informations than the name
        if person['type'] == 'INDI' and person['data']['NAME'] == trueRootTreeName and not flagRootFound:
            flagRootFound = True
            trueRootDataDict = person['data']
        # Extracting the forbidden children's ID
        if person['type'] == 'INDI' and person['data']['NAME'] in forbiddenChildNames and flagCounterforbiddenChildFound > 0:
            # Storing the ID matching person['data']['NAME'] in the correct index
            forbiddenChildIds[forbiddenChildNames.index(
                person['data']['NAME'])] = person['data']['xref_id']
            flagCounterforbiddenChildFound = flagCounterforbiddenChildFound - 1

    if not flagRootFound:
        print('ERROR: '+trueRootTreeName+' not found in '+jsonPath)
        sys.exit(-1)

    # First row
    trueRootTreeBirthDate = extractSecureDictAttribute(
        trueRootDataDict, 'BIRTH/DATE')
    trueRootTreeBirthPlace = extractSecureDictAttribute(
        trueRootDataDict, 'BIRTH/PLACE')
    trueRootTreeId = extractSecureDictAttribute(
        trueRootDataDict, 'xref_id')
    trueRootTreeOccupation = extractSecureDictAttribute(
        trueRootDataDict, 'OCCUPATION')
    trueRootTreeSex = extractSecureDictAttribute(
        trueRootDataDict, 'SEX')
    trueRootTreeNickname = extractSecureDictAttribute(
        trueRootDataDict, 'NAME/NICKNAME')

    toolTip = buildToolTip(trueRootTreeOccupation,
                           trueRootTreeBirthPlace, '', trueRootTreeSex)
    dataRow = buildDataRow(trueRootTreeId, trueRootTreeName, trueRootTreeNickname,
                           trueRootTreeBirthDate, trueRootTreeBirthPlace, '', '', toolTip)
    dataRows = dataRows + dataRow
    personInTheHtmlTreeCounter = personInTheHtmlTreeCounter + 1

    if DEBUG_MODE:
        orphanDataRow = buildDataRow(
            DEBUG_ORPHAN_NODE__ID, DEBUG_ORPHAN_NODE__NAME, '', '', '', '', '', DEBUG_ORPHAN_NODE__TOOLTIP)
        dataRows = dataRows + orphanDataRow

    for person in jsonDict['children']:
        warningLog = ''

        if person['type'] == 'INDI':
            dataRow = ''
            childName = ''
            childIdList = []
            personBirthPlace = extractSecureDictAttribute(
                person['data'], 'BIRTH/PLACE')
            personDeathPlace = extractSecureDictAttribute(
                person['data'], 'DEATH/PLACE')
            personId = extractSecureDictAttribute(
                person['data'], 'xref_id')
            toolTip = buildToolTip(
                extractSecureDictAttribute(person['data'], 'OCCUPATION'),
                personBirthPlace,
                personDeathPlace,
                extractSecureDictAttribute(person['data'], 'SEX'))
            personName = person['data']['NAME']
            personNickname = extractSecureDictAttribute(
                person['data'], 'NAME/NICKNAME')

            # Birth date with robustness
            personBirthDate = extractSecureDictAttribute(
                person['data'], 'BIRTH/DATE')

            # Death date with robustness
            personDeathDate = extractSecureDictAttribute(
                person['data'], 'DEATH/DATE')

            # Avoid error for the tree root - childName will remain empty, and my sibling will not be added - i am the only root
            if personName != trueRootTreeName and personName != falseRootTreeName and '@FAMILY_SPOUSE' in person['data']:
                personFamilySpouse = person['data']['@FAMILY_SPOUSE']

                # Manually add me as my parent's son
                if personName in parentsOfRootTreeName:
                    childIdList.append(trueRootTreeId)
                else:
                    # Look for the person which family child ID is the same as the person's family spouse ID in the JSON file: it will be one of my son
                    possibleSons = []
                    for possibleSonIter in jsonDict['children']:
                        if possibleSonIter['type'] == 'INDI':
                            possibleSonIterName = possibleSonIter['data']['NAME']
                            if possibleSonIterName != trueRootTreeName and '@FAMILY_CHILD' in possibleSonIter['data']:
                                personFamilyChild = possibleSonIter['data']['@FAMILY_CHILD']
                                if personFamilySpouse == personFamilyChild:
                                    # Do not keep in the candidate child list the forbidden ones
                                    if possibleSonIter['data']['xref_id'] not in forbiddenChildIds:
                                        # Store the different found son
                                        possibleSons.append(
                                            possibleSonIter['data'])
                    if len(possibleSons) == 0:
                        # No son found - does not have to be in the tree (unless there is an error)
                        print('INFO: ' + personName + ' has no son\n')
                        infoCounter = infoCounter + 1
                    elif len(possibleSons) == 1:
                        childIdList.append(possibleSons[0]['xref_id'])
                    else:
                        # Choose the correct son
                        warningLog = personName + ' has several sons:\n'
                        warningCounter = warningCounter + 1
                        # First loop: get the family ID built (as a spouse) by each candidate son
                        possibleSonsWhichHaveChildren = []
                        for eachSon in possibleSons:
                            warningLog = warningLog + \
                                '  -' + eachSon['NAME']+'\n'
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
                            childIdList.append(
                                possibleSonsWhichHaveChildren[0]['xref_id'])
                            print(SOLVED_LOG_PREFIX + warningLog + ' --> ' +
                                  possibleSonsWhichHaveChildren[0]['NAME'] + ' <--')
                            warningCounter = warningCounter - 1
                            solvedWarningCounter = solvedWarningCounter + 1
                        else:
                            print(SOLVED_LOG_PREFIX + warningLog + ' !!! ' +
                                  'Adding each one of them' + ' !!!')
                            # Cannot find which son is the correct one: I guess each one is correct (wedding between cousins)
                            for eachPossibleSon in possibleSonsWhichHaveChildren:
                                childIdList.append(
                                    eachPossibleSon['xref_id'])
                            warningCounter = warningCounter - 1
                            solvedWarningCounter = solvedWarningCounter + 1

                        print('')

                # If a child have been found, add the person in the list
                # Else, it will be add as a parent to the DEBUG-ORPHAN node
                if len(childIdList) != 0:
                    # Used in case one person has two sons in my tree (wedding between cousins)
                    duplicaterIndex = 1
                    for childIdItem in childIdList:
                        # FIXME marche pas. Le lien dans les graphes se fait entre personId et childIdItem.
                        # Ici, j'ai une person qui a 2 enfants. Je dois la rajouter mais avec 2 index différents (+ faire les liens)
                        dataRow = buildDataRow(
                            f"{personId}+{duplicaterIndex}", personName, personNickname, personBirthDate, personBirthPlace, personDeathDate, f"{childIdItem}+{duplicaterIndex}", toolTip)
                        personInTheHtmlTreeCounter = personInTheHtmlTreeCounter+1
                        dataRows = dataRows + dataRow
                        duplicaterIndex += 1

    # End of the rows list
    dataRows = dataRows + ']'

    # Checker
    checkerOutput = checker(jsonDict)

    # Writing the result in a file
    with open(outPath, 'w', encoding='utf-8') as outFile:
        outFile.write(dataRows)

    # Report
    print('Finished, '+str(personInTheHtmlTreeCounter)+' people added out of '+str(personInTheJsonTreeCounter)+' in the original tree.\n'+str(warningCounter) +
          ' not solved warning(s), '+str(solvedWarningCounter)+' solved one(s), '+str(infoCounter)+' info(s).')
    if checkerOutput:
        print('\nThe checker returned no error.\n')
    else:
        print('\nThe checker returned error(s).\n')
    # Writing the formatted dates in a file
    with open('./formatted_dates.txt', 'w', encoding='utf-8') as outFile:
        if DEBUG_MODE:
            outFile.write(birthDatesList+deathDatesList)
        else:
            # Flush the file
            outFile.write("")
