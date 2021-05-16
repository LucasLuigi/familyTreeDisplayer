var gedcom = require('gedcom')

// Does not work because of returns: to debug
function readTextFile(file) {
    var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
    var rawFile = new XMLHttpRequest();
    var gedText;
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function () {
        if (rawFile.readyState === 4) {
            if (rawFile.status === 200 || rawFile.status == 0) {
                gedText = rawFile.responseText;
            }
        }
    }
    rawFile.send(null);
    return gedText;
}

var ged_me = `0 HEAD
1 SOUR GeneWeb
2 VERS 7.0.0
2 NAME gwb2ged
2 CORP INRIA
3 ADDR http://www.geneweb.org
2 DATA lucas
1 DATE 28 APR 2021
2 TIME 23:16:23
1 FILE base.ged.tmp
1 GEDC
2 VERS 5.5.1
2 FORM LINEAGE-LINKED
1 CHAR UTF-8
0 @I1@ INDI
1 NAME Papa
1 SEX M
1 BIRT
2 DATE 01 FEB 1960
2 PLAC Paris, France
1 FAMC @F1@
1 FAMS @F2@
0 @I2@ INDI
1 NAME Maman
1 SEX F
1 BIRT
2 DATE 01 FEB 1960
2 PLAC Paris, France
1 FAMC @F3@
1 FAMS @F2@
0 @I3@ INDI
1 NAME Lucas /Luigi/
1 SEX M
1 BIRT
2 DATE 01 JAN 2000
2 PLAC Paris, France, dont care anyway
1 FAMC @F2@
0 @I4@ INDI
1 NAME Papy
1 SEX M
1 BIRT
2 DATE 01 JAN 1900
2 PLAC Paris, France
1 DEAT
2 DATE 01 JAN 2000
1 OCCU Cultivateur
1 FAMC @F4@
1 FAMS @F3@
0 TRLR`

// Does not work yet
//var ged_me = readTextFile("file:///C:/Users/Admin/Workspace/familyTreeDisplayer/base.ged")

var parseOut = gedcom.parse(ged_me);

var compactOut = gedcom.compact(parseOut)

console.log(JSON.stringify(compactOut, null, 4))