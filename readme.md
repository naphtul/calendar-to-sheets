# calendar-to-sheets
## Input
A Google Calendar event name (or better yet, events).
## Output
A Google Sheet with the Date of the event and the description (or just the URL from the description, if one exists within an HTML a tag).
## Setup
1. `pip install -r requirements.txt`
2. You need to create `credentials.json` by following the [following procedure](https://developers.google.com/workspace/guides/configure-oauth-consent).

The scopes you need are listed here:
- `https://www.googleapis.com/auth/calendar.readonly`
- `https://www.googleapis.com/auth/spreadsheets`