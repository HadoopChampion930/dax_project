import string
from google.cloud import translate
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.tag import StanfordNERTagger
import os
from nltk import TweetTokenizer
import time
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from . import TaggingUtils

def get_constituent_id_name(old_constituent_name):
    mapping = {}
    mapping["BMW"] = ("BMWDE8170003036" , "BAYERISCHE MOTOREN WERKE AG")
    mapping["Allianz"] = ("ALVDEFEI1007380" , "ALLIANZ SE")
    mapping["Commerzbank"] = ("CBKDEFEB13190" , "COMMERZBANK AKTIENGESELLSCHAFT")
    mapping["adidas"] = ("ADSDE8190216927", "ADIDAS AG")
    mapping["Deutsche Bank"] = ("DBKDEFEB13216" , "DEUTSCHE BANK AG")
    mapping["EON"] = ("EOANDE5050056484" , "E.ON SE")
    mapping["Lufthansa"] = ("LHADE5190000974" ,"DEUTSCHE LUFTHANSA AG")
    mapping["Continental"] = ("CONDE2190001578" , "CONTINENTAL AG")
    mapping["Daimler"] = ("DAIDE7330530056" , "DAIMLER AG")
    mapping["Siemens"] = ("SIEDE2010000581" , "SIEMENS AG")
    mapping["BASF"] = ("BASDE7150000030" , "BASF SE")
    mapping["Bayer"] = ("BAYNDE5330000056" , "BAYER AG")
    mapping["Beiersdorf"] = ("BEIDE2150000164" , "BEIERSDORF AG")
    mapping["Deutsche Börse"] = ("DB1DEFEB54555" , "DEUTSCHE BOERSE AG")
    mapping["Deutsche Post"] = ("DPWDE5030147191" , "DEUTSCHE POST AG")
    mapping["Deutsche Telekom"] = ("DTEDE5030147137" , "DEUTSCHE TELEKOM AG")
    mapping["Fresenius"] = ("FREDE6290014544" , "FRESENIUS SE & CO.KGAA")
    mapping["HeidelbergCement"] = ("HEIDE7050000100" , "HEIDELBERGCEMENT AG")
    mapping["Henkel vz"] = ("HEN3DE5050001329" , "HENKEL AG & CO.KGAA")
    mapping["Infineon"] = ("IFXDE8330359160" , "INFINEON TECHNOLOGIES AG")
    mapping["Linde"] = ("LINDE8170014684" , "LINDE AG")
    mapping["Merck"] = ("MRKDE6050108507" , "MERCK KGAA")
    mapping["ProSiebenSat1 Media"] = ("PSMDE8330261794" , "PROSIEBENSAT.1 MEDIA SE")
    mapping["RWE"] = ("RWEDE5110206610" , "RWE AG")
    mapping["SAP"] = ("SAPDE7050001788" , "SAP SE")
    mapping["thyssenkrupp"] = ("TKADE5110216866" , "THYSSENKRUPP AG")
    mapping["Vonovia"] = ("VNADE5050438829" , "VONOVIA SE")
    mapping["DAX"] = ("DAX", "DAX")
    mapping["Fresenius Medical Care"] = ("FMEDE8110066557" , "FRESENIUS MEDICAL CARE AG & CO.KGAA")
    mapping["Volkswagen"] = ("VOW3DE2070000543" , "VOLKSWAGEN AG")
    #("MUV2DEFEI1007130" , "MUNCHENER RUCKVERSICHERUNGS - GESELLSCHAFT AKTIENGESELLSCHAFT IN MUNCHEN")

    return mapping[old_constituent_name]

def analytics():
    sia = SIA()

    tokenizer = TweetTokenizer(preserve_case=True, reduce_len=True, strip_handles=False)

    list_of_tweets = []
    for tweet in tweets_to_check:
        doc = tweet._json

        if collection.find({"id_str": doc["id_str"]}, {"id_str": 1}).limit(1):
            continue

        list_of_tweets.append(doc)

    if language != "en":
        if not do_translation(list_of_tweets):
            if not do_translation(list_of_tweets):
                return None


    for document in list_of_tweets:
        if language == 'en':
            document.update(preprocess_tweet(document['text']))
        else:
            document.update(preprocess_tweet(document['text_en']))

        document['search_term'] = searchQuery
        document['constituent'] = constituent
        document['language'] = language

        date = datetime.strptime(document['created_at'], '%a %b %d %H:%M:%S %z %Y')
        document['date'] = date

        #Update sentiment
        sentiment_score,sentiment = get_nltk_sentiment(document["semi_processed_text"], sia)
        document["nltk_sentiment_score"] = sentiment
        document["nltk_sentiment_number"] = sentiment_score

        #Update tags
        document["tag_LOCATION"] = list()
        document["tag_PERSON"] = list()
        document["tag_ORGANIZATION"] = list()
        document["tag_MONEY"] = list()
        document["tag_PERCENT"] = list()
        document["tag_DATE"] = list()
        document["tag_TIME"] = list()

        if language == 'en':
            text = document['text']
        else:
            text = document['text_en']

        for word, tag in get_tags(text, st, tokenizer):
            if tag != "O":
                document["tag_" + tag].append(word)

        if 'retweeted_status' in document:
            document.pop('retweeted_status', None)

    return list_of_tweets

def get_nltk_sentiment(text):
    sia = SIA()
    return sia.polarity_scores(text)

def do_translation(to_translate):
    translate_client = None
    try:
        translate_client = translate.Client()
    except Exception as e:
        #print("Error translating. Skipping...")
        print(e)
        return False


    texts = []
    tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=False)

    for tweet in to_translate:
        tokens = tokenizer.tokenize(tweet._json['text'])
        # remove links
        no_url_tokens = [word for word in tokens if 'http' not in word]
        texts.append(" ".join(no_url_tokens))


    texts = [tweet._json['text'] for tweet in to_translate]

    try:
        translations = translate_client.translate(texts, target_language='en')
    except Exception as e:
        #print("Error translating. Skipping...")
        print(e)
        return False

    if len(translations) == len(to_translate):
        for i in range(0, len(translations)):
            to_translate[i]._json['text_en'] = translations[i]['translatedText']

        time.sleep(1)
        return True
    else:
        return False

def preprocess_tweet(text):
    # Tokenize the tweet text
    tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=False)
    tokens = tokenizer.tokenize(text)

    # remove links
    no_url_tokens = [word for word in tokens if 'http' not in word]

    no_url_joined = " ".join(no_url_tokens)

    # remove stop words and punctuation
    stop_words = set(stopwords.words('english'))
    punct = string.punctuation
    punct_1 = punct.replace('#', '')
    punct_2 = punct_1.replace('@', '')
    stop_words.update(punct_2)
    stop_words.add('...')

    filtered_tokens = [word for word in no_url_tokens if not word in stop_words]

    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(word) if (word[0] != '#' and word[0] != '@') else word for word in filtered_tokens]

    return {'semi_processed_text': no_url_joined, 'processed_text': stemmed_tokens}

def get_tags(text, st, tokenizer):
    new_text = text.replace('€','$')
    tokenized_text = tokenizer.tokenize(new_text)
    classified_text = st.tag(tokenized_text)
    return classified_text

def update_tags(dict_object, taggged_text):
    tags = {}
    tags["PERSON_TAGS"] = []
    tags["NORP_TAGS"] = []
    tags["FACILITY_TAGS"] = []
    tags["ORG_TAGS"] = []
    tags["GPE_TAGS"] = []
    tags["LOC_TAGS"] = []
    tags["PRODUCT_TAGS"] = []
    tags["EVENT_TAGS"] = []
    tags["WORK_OF_ART_TAGS"] = []
    tags["LANGUAGE_TAGS"] = []
    tags["DATE_TAGS"] = []
    tags["TIME_TAGS"] = []
    tags["PERCENT_TAGS"] = []
    tags["MONEY_TAGS"] = []
    tags["QUANTITY_TAGS"] = []
    tags["ORDINAL_TAGS"] = []
    tags["CARDINAL_TAGS"] = []

    for ent in doc.ents:
        print(ent.label_, ent.text)

    return None


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('google_key_path', help='The path of the Google key')
    parser.add_argument('param_connection_string', help='The connection string')
    parser.add_argument('tagger_dir_1', help='Tagging server directory')
    parser.add_argument('tagger_dir_2', help='Tagging server directory')
    args = parser.parse_args()