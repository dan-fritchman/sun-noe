

## Is This Secure?

I think so.
It's not really my area of expertise.
My area of expertise is really limited to eating pizza.

Any links to the underlying spreadsheets are secured in Heroku's secret variables.
Are your cell number and email safe in that spreadsheet?
Or are you going to start getting spam, get your identity stolen, or have some other major problem?

Probably not as safe as if you, say, kept them hidden under your bed.
But yeah, safe.

Either way - don't put your credit card, social security number, or any other high-risk stuff in here.

## Google APIs

The trick part of all this, is probably setting up the Google API access. 
This generally has to be done through the web. 
An indication that its *wrong*, would include errors like so:

```
E           gspread.exceptions.APIError: {
E             "error": {
E               "code": 403,
E               "message": "Google Sheets API has not been used in project 591353589021 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/sheets.googleapis.com/overview?project=591353589021 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.",

E           gspread.exceptions.APIError: {
E            "error": {
E             "errors": [
E              {
E               "domain": "usageLimits",
E               "reason": "accessNotConfigured",
E               "message": "Access Not Configured. Drive API has not been used in project 591353589021 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=591353589021 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.",
E               "extendedHelp": "https://console.developers.google.com/apis/api/drive.googleapis.com/overview?project=591353589021"

```

Those URLs are the best help available, including the Google-API-project ID. 


