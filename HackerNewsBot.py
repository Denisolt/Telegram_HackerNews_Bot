import logging
import telegram
from telegram.error import NetworkError, Unauthorized
import requests
import hn





def main():
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot('377514645:AAFMnrVmoE-GmAmVahB7GVIrN22Ii2rOrQM')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            HackerNews(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1

def HackerNews(bot):
    global update_id
    # Request updates after the last update_id
    for update in bot.getUpdates(offset=update_id, timeout=10):
        # chat_id is required to reply to any message
        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        top_posts = hn.get_post()
        Info = 'These are the top posts right now from https://news.ycombinator.com\n'
        number = 1
        for post in top_posts:
			Info = Info + str(number) + ': ' + post.title+'\nLink: '+post.url+'\n\n'
			number = number+1
        update.message.reply_text(Info)

if __name__ == '__main__':
    main()