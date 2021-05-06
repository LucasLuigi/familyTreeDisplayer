# familyTreeDisplayer

## Description

A set of scripts to transform a GEDCOM file into an HTML page
Python 3.9+

## Installation steps

1. Clone [tmcw/gedcom](https://github.com/tmcw/gedcom)
2. `npm init`
3. Add dependencies to gedcom `("gedcom": "^3.0.0")` to use its functions

## Execution step

1. Export a GEDCOM file in UTF-8 format
2. In app.js, paste it in the variable ged_me, delimited with \`
3. Run `gedToJson.bat` to make a RESULT.json
4. In `treeConstants.py`, replace the field by yours. Be careful, the surname is delimited by /
5. Run `python jsonToGoogleData.py`. Set DEBUG_MODE to True to export the orphan nodes
6. Paste the content of `googleRowsData.txt` in `familyTreeDisplayer.html` as the argument of data.addRows()
7. Run `familyTreeDisplayer.html` in a browser
