# Hosting the Newsweec Bot for yourself


### Clone the repo and cd to the directory.
```commandline
git clone https://github.com/Adwaith-Rajesh/newsweec.git
cd newsweec
```
### Install the required dependencies
```commandline
pip install -r requirements.txt
```

### Add the required credentials

Create a file `.env` in the root directory and add the following data.
```bash
BOT_API_TOKEN="your-telegram-bot-api-token"
ADMIN_ID="telegram-user-id-of-the-admin"
```

### Start the bot
```commandline
python newsweec.py --start
```

## To test whether the internal functions work or not.

### Install the dev dependencies
```commandline
pip install -r requirements-dev.txt
```

### Run pytest
```commandline
pytest -v
```
