import tweepy
import threading
import time
import re
from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import logging

# Twitter API credentials
CONSUMER_KEY = 'YOUR_CONSUMER_KEY'
CONSUMER_SECRET = 'YOUR_CONSUMER_SECRET'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

# Initialize Twitter API
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token from BotFather
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

# States for conversation handler
LINK, LIKES, REPLIES, REPOSTS = range(4)

# Command handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome to the Twitter Monitoring Bot!")

def shield(update: Update, context: CallbackContext):
    if is_user_admin(update, context):
        update.message.reply_text("Please send the Twitter post link.")
        return LINK
    else:
        update.message.reply_text("Sorry, you must be an admin to use this command.")
        return ConversationHandler.END

def link_handler(update: Update, context: CallbackContext):
    context.user_data['link'] = update.message.text
    update.message.reply_text("How many likes should it be?")
    return LIKES

def likes_handler(update: Update, context: CallbackContext):
    context.user_data['likes'] = int(update.message.text)
    update.message.reply_text("How many replies should it be?")
    return REPLIES

def replies_handler(update: Update, context: CallbackContext):
    context.user_data['replies'] = int(update.message.text)
    update.message.reply_text("How many reposts should it be?")
    return REPOSTS

def reposts_handler(update: Update, context: CallbackContext):
    context.user_data['reposts'] = int(update.message.text)
    update.message.reply_text("Tracking started. I will lock the chat now.")
    lock_chat(update, context, True)

    # Start a background thread to monitor the Twitter post
    thread = threading.Thread(target=monitor_twitter_post, args=(context.user_data['link'], context.user_data['likes'], context.user_data['replies'], context.user_data['reposts'], update, context))
    thread.start()

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Operation cancelled. Chat is now open.')
    lock_chat(update, context, False)
    return ConversationHandler.END

def lock_chat(update: Update, context: CallbackContext, lock: bool):
    permissions = ChatPermissions(can_send_messages=not lock)
    context.bot.set_chat_permissions(chat_id=update.effective_chat.id, permissions=permissions)

last_update_message_id = None

def monitor_twitter_post(tweet_url, target_likes, target_replies, target_reposts, update, context):
    global last_update_message_id
    tweet_id = extract_tweet_id(tweet_url)
    image_url = 'URL_TO_YOUR_MEDIA'  # Replace with your media URL

    while True:
        retweets, likes = get_tweet_metrics(tweet_id)
        replies = get_replies_count(tweet_id, twitter_api)
        # Prepare status symbols based on goals
        likes_status = '✅' if likes >= target_likes else '❌'
        replies_status = '✅' if replies >= target_replies else '❌'
        reposts_status = '✅' if retweets >= target_reposts else '❌'

        # Send update to chat with media
        if likes >= target_likes and replies >= target_replies and retweets >= target_reposts:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, 
                                   caption="Goal reached! Unlocking the chat.")
            lock_chat(update, context, False)
            break
        else:
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, 
                                   caption=f"Locking chat until the tweet has {target_likes} likes, {target_replies} replies, and {target_reposts} reposts.\n\n"
                                           f"{likes_status} Current Likes: {likes} | 🎯 {target_likes}\n"
                                           f"{replies_status} Current Replies: {replies} | 🎯 {target_replies}\n"
                                           f"{reposts_status} Current Reposts: {retweets} | 🎯 {target_reposts}\n\n"
                                           f"Check the tweet here:\n{tweet_url}")
        # Delete last updated message
        if last_update_message_id:
            try:
                context.bot.delete_message(chat_id=update.effective_chat.id, message_id=last_update_message_id)
            except Exception as e:
                logger.error(f"Error deleting message: {e}")

        # Send new updated message
        new_message = context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url, 
                                             caption=f"Your caption here")
        last_update_message_id = new_message.message_id
    
    time.sleep(3600)  # 3600 = 1 Hour
            
def is_user_admin(update: Update, context: CallbackContext) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
            
    try:
        chat_administrators = context.bot.get_chat_administrators(chat_id)
        return any(admin.user.id == user_id for admin in chat_administrators)
    except Exception as e:
        logger.error(f"Error checking if user is admin: {e}")
        return False
            
def extract_tweet_id(tweet_url):
    match = re.search(r'/status/(\d+)', tweet_url)
    return match.group(1) if match else None
            
def get_tweet_metrics(tweet_id):
    try:
        tweet = twitter_api.get_status(tweet_id)
        retweets = tweet.retweet_count
        likes = tweet.favorite_count
        return retweets, likes
    except Exception as e:
        logger.error(f"Error fetching tweet metrics: {e}")
        return 0, 0
            
def get_replies_count(tweet_id, twitter_api):
    original_tweet = twitter_api.get_status(tweet_id)
    user_screen_name = original_tweet.user.screen_name
    query = f"to:{user_screen_name}"
    replies_count = 0
            
    try:
        for page in tweepy.Cursor(twitter_api.search, q=query, since_id=tweet_id, tweet_mode='extended').pages():
            for tweet in page:
                if hasattr(tweet, 'in_reply_to_status_id_str'):
                    if tweet.in_reply_to_status_id_str == tweet_id:
                        replies_count += 1
    except Exception as e:
        logger.error(f"Error fetching replies: {e}")
            
    return replies_count
            
# Main function to set up the bot           
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('shield', shield)],
        states={
            LINK: [MessageHandler(Filters.text & ~Filters.command, link_handler)],
            LIKES: [MessageHandler(Filters.text & ~Filters.command, likes_handler)],
            REPLIES: [MessageHandler(Filters.text & ~Filters.command, replies_handler)],
            REPOSTS: [MessageHandler(Filters.text & ~Filters.command, reposts_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
