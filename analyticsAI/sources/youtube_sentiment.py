import re
import math
from nltk.classify import NaiveBayesClassifier
from textblob import TextBlob as tb
import os


class Youtube_Google_Sentiment:
    def __init__(self):
        self.response_json = {}
        self.likecount = []
        self.best_commdb = []
        self.sentiment_sum = 0

    def best_comment(self):
        """
        :return returns index of 10 (max) best comments
        """
        if len(self.best_commdb) == 0:
            self.comment_db()
        best_comments = sorted(self.best_commdb, key=lambda t: t[2], reverse=True)[: (min(25, len(self.best_commdb)))]
        best_comments = sorted(best_comments, key=lambda t: t[1], reverse=True)[: (min(10, len(self.best_commdb)))]
        return [best_comment[0] for best_comment in best_comments if best_comment[1] > 0]

    def worst_comment(self):
        """
        :return returns index of 10 (max) worst comments
        """
        if len(self.best_commdb) == 0:
            self.comment_db()
        worst_comments = sorted(self.best_commdb, key=lambda t: t[1], reverse=False)[: (min(10, len(self.best_commdb)))]
        return [worst_comment[0] for worst_comment in worst_comments if worst_comment[1] < 0]

    def sentiment_ratio(self):
        """
        :return returns ratio of positive biased comments to all biased comments
        """
        pos_count = 0
        for senti_comment in self.best_commdb:
            if senti_comment[1] > 0:
                pos_count += 1
        return pos_count / len(self.best_commdb)


class Sentiment:
    def __init__(self):
        pass

    def textblobsentiment(self, comments, likecount):
        """
        :param comments: list of text
        :param likecount: list of likes in same order
        :return: Text blob average sentiment with likes considered
        """
        comment_sum = 0.0
        if len(comments) == 0:
            return 0
        sum_for_norm = 0  # consider each like as comment with same polarity and normalise accordingly
        for i, titem in enumerate(comments):
            comment_sum += float(tb(titem).sentiment.polarity) * (likecount[i] + 1)
            sum_for_norm += likecount[i]
        return comment_sum / (len(comments) + sum_for_norm)

    def textblobsentiment_best(self, comments, likecount):
        """
        :param comments: list of text
        :param likecount: list of likes in same order
        :return: best sentiment comments sorted by likes
        """
        if len(comments) == 0:
            return 0
        list_comments = []
        for i, val in enumerate(likecount):
            list_comments.append([float(tb(comments[i]).sentiment.polarity), comments[i], val])
        # list_comments = sorted(list_comments, key=lambda t: t[2], reverse=True)[:min(25, len(comments))]
        list_comments = sorted(list_comments, key=lambda t: t[0], reverse=True)[: min(10, len(comments))]
        return [l[1] for l in list_comments if l[0] > 0]

    def textblobsentiment_worst(self, comments, likecount):
        """
        :param comments: list of text
        :param likecount: list of likes in same order
        :return: worst sentiment comments
        """
        if len(comments) == 0:
            return 0
        list_comments = []
        for i, val in enumerate(likecount):
            list_comments.append([float(tb(comments[i]).sentiment.polarity), comments[i], val])
        list_comments = sorted(list_comments, key=lambda t: t[0])[: min(10, len(comments))]
        return [l[1] for l in list_comments if l[0] < 0]

    def textblobsentiment_ratio(self, comments):
        """
        :param comments: list of text
        :return: ratio of positive to negative comments
        """
        if len(comments) == 0:
            return 0
        p_count = 0
        for val in comments:
            if float(tb(val).sentiment.polarity) > 0:
                p_count += 1
        return p_count / len(comments)

    @staticmethod
    def make_full_dict(words):
        """
        :param words: list with text
        :return: List of text,True pair required for bloomberg method
        """
        return dict([(word, True) for word in words])

    def bloomberg(self, text):
        """
        :param text: list of text (tagged label files rt positive and rt negative
        :return: Bloomberg average sentiment
        """
        if len(text) == 0:
            return 0
        # Returns classified sentiment using bloomberg sentiment and two sentiment tagged files
        negative_sentences = open(os.path.join("rt-polarity-neg.txt"), "r", encoding="utf8")
        positive_sentences = open(os.path.join("rt-polarity-pos.txt"), "r", encoding="utf8")
        negative_sentences = re.split(r"\n", negative_sentences.read())
        positive_sentences = re.split(r"\n", positive_sentences.read())

        positive_features = []
        negative_features = []
        # breaks up the sentences into lists of individual words
        # creates instance structures for classifier
        for i in positive_sentences:
            positive_words = re.findall(r"[\w']+|[.,!?;]", i)
            positive_words = [Sentiment.make_full_dict(positive_words), "pos"]
            positive_features.append(positive_words)
        for i in negative_sentences:
            negative_words = re.findall(r"[\w']+|[.,!?;]", i)
            negative_words = [Sentiment.make_full_dict(negative_words), "neg"]
            negative_features.append(negative_words)
        # creates training test features
        positivecutoff = int(math.floor(len(positive_features) * 3 / 4))
        negativecutoff = int(math.floor(len(negative_features) * 3 / 4))
        trainfeatures = positive_features[:positivecutoff] + negative_features[:negativecutoff]

        # Runs the classifier on the testFeatures
        classifier = NaiveBayesClassifier.train(trainfeatures)
        comment_sum = 0.0
        for c in text:
            res = classifier.classify(Sentiment.make_full_dict(c.split()))
            if str(res) == "pos":
                comment_sum += 1
        return comment_sum / len(text)
