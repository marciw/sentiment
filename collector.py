# Tweet collector via tweepy and user-supplied search terms,
# to be used with CloudFormation template
# based on http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
# with modifications by http://github.com/marciw

from twaiter import TWaiter
import tweepy, sys, twitterparams

# authentication params (supplied via cfn)
consumer_key = twitterparams.OAuthConsKey
consumer_secret = twitterparams.OAuthConsSecret
access_token = twitterparams.OAuthToken
access_token_secret = twitterparams.OAuthTokenSecret

# OAuth via tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def main(terms):
    if len(terms) == 3:
        search = [terms[1], terms[2]]
    else:
        print "Please provide exactly two search terms. Multiple-word terms should be enclosed in quotation marks. \nExample: \"health care\" term2"
        sys.exit()
        # should exit more gracefully

    collection = 'tweets'
    waiter = TWaiter(api, collection)
    stream = tweepy.Stream(auth, waiter)

    print "Collecting tweets. Please wait."

    try:
        stream.filter(track=search)
    except Exception, e:
        print "An error occurred. No tweets collected.", e
        stream.disconnect()


if __name__ == '__main__':
    main(sys.argv)