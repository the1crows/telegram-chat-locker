# telegram-chat-locker Bot
telegram chatlocker for community engagement on tweets

Twitter ChatLock Telegram Bot

This script implements a Telegram Bot that monitors a specific Twitter post for changes in the number of likes, replies, and retweets. When certain targets are met, the bot performs specific actions like locking or unlocking a Telegram chat.

Features

  •	Monitor Twitter posts for likes, replies, and retweets.
  •	Lock and unlock a Telegram chat based on Twitter post metrics.
  •	Send periodic updates in the Telegram chat about the Twitter post’s status.

Setup and Installation

Getting Twitter API Credentials

 1.	Create a Twitter Developer Account:
  •	Go to the Twitter Developer Portal.
  •	Sign in with your Twitter account and apply for a developer account.
  •	Fill out the application form with the necessary details about how you plan to use the API.
 2.	Create a Project and an App:
  •	Once approved, create a new project and app within the developer portal.
  •	From the app details page, generate your API keys and tokens: API Key, API Key Secret, Access Token, and Access Token Secret.
 3.	Add API Keys to Your Script:
  •	Replace the placeholders in your script with your Twitter API credentials.

Setting up Telegram Bot with BotFather

 1.	Create a New Bot:
  •	Open Telegram and search for the ‘BotFather’ account, or you can directly go to t.me/botfather.
  •	Start a chat with BotFather and use the /newbot command.
  •	Follow the prompts to set a name and a username for your bot.
  •	Upon successful creation, BotFather will provide you with a bot token.
 2.	Retrieve Your Bot Token:
  •	Copy the token provided by BotFather.
  •	Replace the placeholder in your script with your Telegram bot token.

Local Setup

  1. Install Python: Make sure Python 3.x is installed on your system. You can download it from python.org.
  2. Clone the Repository: Clone this repository to your local machine or download the source code.
   • git clone [URL to your repository]
     cd [repository name]
 
  3. Install Dependencies: Install the necessary Python packages using pip.
   • pip install -r requirements.txt


Configuration

  1. Twitter API Keys:
   • Insert your Twitter API keys into the script as shown in the “Getting Twitter API Credentials” section.
  2. Telegram Bot Token:
   • Insert your Telegram Bot token into the script as detailed in the “Setting up Telegram Bot with BotFather” section.
  3. Environmental Variables (Optional but Recommended):
   • Use environmental variables for your API keys and bot token for added security.

Run the script Locally using Python:

   • python bot_script.py

Your bot should now be up and running on your local machine.

Deploying to a Web Host

	1. Choose a Hosting Provider: Select a provider that supports Python applications. Some popular choices are Heroku, AWS, and Google Cloud.
	2. Prepare for Deployment: Depending on the provider, you may need to create a Procfile, set up environment variables, etc.
	3. Deploy: Upload your code to the hosting provider and follow their instructions to start the application. Make sure that your host has continuous uptime.
	4. Set Webhooks (if applicable): If using webhooks instead of polling, configure the webhook URL as per the Telegram API documentation.

Usage

	• Start the bot in your Telegram group chat.
	• Use the /shield command to begin monitoring a Twitter post.
	• Follow the prompts to set likes, replies, and retweets targets.
	• The bot will lock the chat and periodically send updates about the Twitter post’s status. Once the targets are met, the chat will be unlocked.

This bot is designed to integrate the Twitter API with a Telegram bot, allowing users to monitor and analyze Twitter posts directly from Telegram. The bot enables fetching the number of likes and retweets for a specific Twitter post and offers interactivity for users to update these figures.

Prerequisites

Before using the bot, ensure you have the following:

	• Python installed on your machine.
	• An active Telegram bot created through BotFather, with an available bot token.
	• Valid Twitter API keys, including Consumer Key, Consumer Secret, Access Token, and Access Token Secret.

Installation

   1. Clone this repository or download the source code.
   2. Open a terminal and navigate to the project folder.
   3. Create a virtual environment: python -m venv venv.
   4. Activate the virtual environment:
	 •	Windows: .\venv\Scripts\activate
	 •	macOS/Linux: source venv/bin/activate
   5. Install required packages: pip install -r requirements.txt.

Configuration

Replace the following placeholder values in bot.py with your actual values:

	• YOUR_TELEGRAM_BOT_TOKEN: The Telegram bot token you obtained from BotFather.
	• YOUR_CONSUMER_KEY, YOUR_CONSUMER_SECRET, YOUR_ACCESS_TOKEN, YOUR_ACCESS_TOKEN_SECRET: Your Twitter API keys.
	• URL_TO_YOUR_MEDIA: link to media file for the bot messages in telegram

Usage

To run the bot, use the command python chatlock.py in your activated terminal. Once the bot is active, you can use it in Telegram by sending commands like /start and /shield.

Features

	• /start: Initiates a conversation with the bot.
	• /shield: Request a Twitter link to fetch and update the number of likes and retweets.

License

This project is licensed under [MIT] - see the LICENSE file for details.

Feel free to customize this Bot based on your specific project, especially sections about the license and any additional configuration instructions if needed.
