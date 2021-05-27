@ECHO OFF

if exist RESULT.json (
	move RESULT.json RESULT.backup.json
)

node app.js > RESULT.json