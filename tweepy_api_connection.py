import tweepy as tw
import re
import json

consumer_key = 'rl9c2ppWCxAT6gvqQxsqM73Xx'
consumer_secret = '9sCRnX6CKofbdD8Gkt8Z6ocz2hqIO72SfekqWuMBsxjpaqzGec'

access_token = "1440682685496578058-sYNRIWt9Yj8r3kKAXtChHJwX84XUzw"
access_token_secret = "QOdHp3z7Gqix19dtYXJtiuJv0nwyy2YAMGz5qf7GBU6ar"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True)
print(api.me().name)

# If the application settings are set for "Read and Write" then
# this line should tweet out the message to your account's
# timeline. The "Read and Write" setting is on https://dev.twitter.com/apps
# api.update_status(status='Updating using OAuth authentication via Tweepy!')

# Scraping a specific Twitter user’s Tweets
# Uses REST API to pull data from twitter
screen_name_coinbase = 'Coinbase'
screen_name_pro = 'CoinbasePro'
count = 5
regex_search = 'agld-usd'

cursor = tw.Cursor(api.user_timeline, screen_name=screen_name_pro).items(count)
for tweet in cursor:
    tweets = [str.lower(tweet.text)][0]
    # print(tweets)
    filtered_tweet = re.search(regex_search, tweets)
    if filtered_tweet is not None:
        print(str(tweet.id) + ": " + tweets)


# Scraping tweets from a text search query
# query = 'dogecoin'
#
# cursor = tw.Cursor(api.search, q=query, lang='en', result_type='recent').items(count)
# for tweet in cursor:
#     # print(tweet)
#     tweets_list = [tweet.user.screen_name, tweet.id, tweet.text]
#     print(tweets_list)

# StreamListener used to filter real-time stream of public Tweets
# Streaming API pushes messages to a persistent session

# 1. Create a class inheriting from StreamListener
class MyStreamListener(tw.StreamListener):

    def on_connect(self):
        # Function called to connect to the Twitter Streaming API
        print("You are now connected to the Twitter streaming API.")

    def on_error(self, status_code):
        # Function displays the error or status code
        print('An Error has occurred: ' + repr(status_code))
        return False

    # def on_status(self, status):
    #     print('STATUS: ' + status.text)
    #
    #     # if retweeted_status attribute exists, flag this tweet as a retweet
    #     is_retweet = hasattr(status, "retweeted_status")
    #
    #     # check if text has been truncated
    #     if hasattr(status, "extended_tweet"):
    #         text = status.extended_tweet["full_text"]
    #     else:
    #         text = status.text
    #
    #         # check if this is a quote tweet.
    #         is_quote = hasattr(status, "quoted_status")
    #         quoted_text = ""
    #         if is_quote:
    #             # check if quoted tweet's text has been truncated before recording it
    #             if hasattr(status.quoted_status, "extended_tweet"):
    #                 quoted_text = status.quoted_status.extended_tweet["full_text"]
    #             else:
    #                 quoted_text = status.quoted_status.text

    def on_data(self, data):
        try:
            # Decode the JSON data from Twitter
            json_data = json.loads(data)

            # Pick the 'text' data from the Tweet
            tweet_message = json_data['text']

            # Show the text from the tweet we have collected
            print(tweet_message)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    # 2. Using that class create a Stream object
    myStreamListener = MyStreamListener()
    myStream = tw.Stream(auth=api.auth, listener=myStreamListener, tweet_mode='extended')

    # 3. Connect to the Twitter API using the Stream.
    words = ['gabby petito', 'bitcoin']
    print("Keywords: " + str(words))
    # print("is_retweet: " + is_retweet)
    myStream.filter(track=words)
