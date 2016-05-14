import sys
import requests
from bs4 import BeautifulSoup as BS
import json


class Speech:
    """Gets speech from www.presidency.ucsb.edu/ based on speech_id"""

    def __init__(self, speech_id):
        self.response = requests.get(
            "http://www.presidency.ucsb.edu/ws/index.php?pid={}".format(speech_id))

    def get_content(self):
        if self.response.status_code != 200:
            print "Bad response: " + str(self.response.status_code)
            sys.exit()

        return self.response.content


class Sentiment:
    """Gets sentiment of speech"""

    def __init__(self, speech_content):
        self.soup = BS(speech_content, "html.parser")
        self.speech_text_raw = self.soup.find("span", "displaytext").text
        self.speech_text = self.speech_text_raw.replace("[applause]", "")

    def get_sentiment(self):
        print
        print self.speech_text

        # API info: http://text-processing.com/docs/sentiment.html
        sentiment_resp = requests.post(
            "http://text-processing.com/api/sentiment/", {"text": self.speech_text})

        if sentiment_resp.status_code == 200:
            # Convert content string to dictionary
            sentiment = json.loads(sentiment_resp.content)
            print
            print "Sentiment label: " + str(sentiment['label'])
            print "Sentiment probability: " + str(sentiment['probability'])
        else:
            print "Bad response: " + str(resp.status_code)

if __name__ == "__main__":
    speech_id = raw_input("Enter speech ID: ")
    speech = Speech(speech_id)
    speech_content = speech.get_content()
    sentiment = Sentiment(speech_content)
    sentiment.get_sentiment()
