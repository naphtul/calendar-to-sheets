# calendar-to-sheets
An example project on how to integrate with Google APIs (with OAuth2) and transform data from one service to another.
## Input
A Google Calendar event name (or better yet, events).
## Output
A Google Sheet with the Dates of the events and the descriptions (or just the URL from the description, if one exists within an HTML `<a>` tag).
## Setup
1. Install requirements: `pip install -r requirements.txt`
1. Login to [Google Cloud Console](https://console.cloud.google.com/welcome)
1. From the Projects dropdown create a project
1. Wait for the project creation to complete and Select the newly created project
1. Click the API Library and Enable the two APIs:
   - Google Calendar API
   - Google Sheets API
1. Create an OAuth Consent Screen by following [this](https://developers.google.com/workspace/guides/configure-oauth-consent) procedure. The scopes you need to add are:
   - `https://www.googleapis.com/auth/calendar.readonly`
   - `https://www.googleapis.com/auth/spreadsheets`
1. Add your Google email address to the list of approved testers
1. Create Credentials by following [this](https://developers.google.com/workspace/guides/create-credentials#desktop-app) procedure
1. Save the downloaded JSON file as `credentials.json`, and move the file to your working directory
## Running
Simply run the [cal2sheets.py](cal2sheets.py) script `python cal2sheets.py`

If this is the first time running this code, A Browser window should open with request to approve the access of the app to your Calendar and Sheets. Rest assured, by reviewing the code you can see that no one but yourself has access to your calendar and sheets, but feel free to remove the access later from [your account](https://myaccount.google.com/permissions).