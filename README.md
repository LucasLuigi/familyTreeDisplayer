# familyTreeDisplayer

## Description

A set of scripts to transform a GEDCOM file into an HTML page
Python 3.9+

## Installation steps

1. Clone [tmcw/gedcom](https://github.com/tmcw/gedcom)
2. Install it globally `npm install -g`
3. Add it as ths project's dependency: `npm install gedcom`
4. `npm install xmlhttprequest`
5. In familyTreeDisplayer/ run `npm init`
6. Add dependencies to tmcw/gedcom `("gedcom": "^3.0.0")` to use its functions

## Execution step

1. Export a GEDCOM file in UTF-8 format
2. In app.js, paste it in the variable ged_me, delimited with \`
3. Run `1_gedToJson.bat` to make a RESULT.json
4. In `treeConstants.py`, replace the fields by yours. Be careful, the surname is delimited by /
5. Run `2_jsonToHtml.bat`. Set DEBUG_MODE in jsonToGoogleData.py to True to include the orphan nodes and export every formatted dates
6. Paste the content of `googleRowsData.txt` in `familyTreeDisplayer.html` as the argument of data.addRows()
7. Run `familyTreeDisplayer.html` in a browser
