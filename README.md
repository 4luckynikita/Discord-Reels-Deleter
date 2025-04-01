# Discord Reels Deleter

Attach this Python script to your Discord bot to prevent the sending of Instagram Reels from a specific user in your server. This was built half as a joke, half out of curiosity. This bot has spiraled into more than just a surface level joke so it has more random features going for it now. Enjoy!

*Note: Ensure you have Python and Pipenv installed!*
### Prerequisite - Set up a bot on [Discord's Developer Portal](https://discord.com/developers) and add it to a server of your choice.
Ensure bot has permissions to send and manage messages in the OAuth page.

## SETUP AND RUN FOR LOCAL USE
### 1. Clone the repo
```sh
git clone https://github.com/4luckynikita/Discord-Reels-Deleter.git
```

### 2. Set up .env file
- Reaname `.env.example` to `.env`
- Set variables in the file. For example:
```
BOT_TOKEN=12345682732819
```


### 3. Install necessary packages
```sh
pipenv install -r requirements.txt
```

##
There are two options for running the actual script. Choose one of the two options. Option 4b is best is pipenv shell is having issues.
## 

### 4a. Turn on the enviornment and run the script!
Activate your shell by running
```sh
pipenv shell
```
and run the bot script with
```sh
python bot.py
```
### 4b. Run script and environment in one command
This creates an environment for the runtime of the bot.py file
```sh
pipenv run python bot.py
```
