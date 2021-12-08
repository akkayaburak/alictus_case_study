# Alictus Automation

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
pip install -r requirements.txt
```

Then you need to go to [Google Drive API](https://developers.google.com/drive) and create an app.

You must enable Google Drive API and Google Sheets API to run the app.

Also, after enabling you need a credentials file that Drive provides (also you need to create an `OAuth 2.0 Client`) and change its name to `google_drive_credentials.json`.

After putting that file to the same folder, you are ready.

Of course, you also need [Slack API](https://api.slack.com/), go and create a Slack App and get the required token.

If you want this to work, lastly you need to download [ngrok](https://ngrok.com/).

After that, follow the instructions on [here](https://dashboard.ngrok.com/get-started/your-authtoken).

## Usage

Now, go to `slack_api.py` and insert the required token inside `Web Client`.

This client inserts messages to `automation` channel. Don't forget to change that if you want it to insert messages to another channel.

Open ngrok and run `ngrok http 5000` because we will run Flask on port 5000.

Ngrok will show you https URL that it provides, copy and paste that to your slack bot URL.

Don't forget, you need to invite the slack bot to your channel and give the required permissions to it.

Now, run `slack_bot.py` and Flask will do the rest.

Run `alictus_automation.py` and you will see the results on your drive and slack channel.

Now `/{your_slack_bot_name} {campaing_name}` will work, I hope.
