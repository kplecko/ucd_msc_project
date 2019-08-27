from scipy.stats import pearsonr
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial import distance


class Similarity:
    def __init__(self):
        pass

    def get_tfidf(self, text_list):
        """
        TF-IDF Matrix Format
        :param text_list: List of normalized documents
        :return: List()
        """
        text_str_list = [" ".join(text) for text in text_list]
        tfidf_vectorizer = TfidfVectorizer()
        tfidf = tfidf_vectorizer.fit_transform(text_str_list)

        return tfidf.toarray().tolist()

    def jaccard_similarity(self, doc1, doc2):
        """
        Jaccard Similarity
        :param doc1: List of words
        :param doc2: List of words
        :return: List()
        """
        intersection = len(list(set(doc1).intersection(set(doc2))))
        union = (len(doc1) + len(doc2)) - intersection

        return float(intersection / union)

    def pearson_similarity(self, doc1, doc2):
        """
        Pearson Similarity, based on TF-IDF
        :param doc1: List of words
        :param doc2: List of words
        :return: List()
        """
        str1 = " ".join(doc1)
        str2 = " ".join(doc2)
        corpus = [str1, str2]
        tfidf = self.get_tfidf(corpus)
        print(tfidf[0])
        print(tfidf[1])

        return pearsonr(tfidf[0], tfidf[1])[0]

    # Cosine similarity
    def cos_similarity(self, text_list):
        """
        Cosine Similarity, based on TF-IDF
        :param text_list: List of normalized documents
        :return: List()
        """
        similarity_list = list()
        tfidf_list = self.get_tfidf(text_list)
        for each in range(1, len(tfidf_list)):
            similarity_list.append(1 - distance.cosine(tfidf_list[0], tfidf_list[each]))

        return similarity_list

    def manhattan_distance(self, doc1, doc2):
        """
        Manhattan Distance, based on TF-IDF
        :param doc1: List of words
        :param doc2: List of words
        :return:
        """
        str1 = " ".join(doc1)
        str2 = " ".join(doc2)
        tfidf = self.get_tfidf(str1, str2)
        return sum([abs(tfidf[0][i] - tfidf[1][i]) for i in range(len(tfidf[0]))])

    def hamming_distance(self, doc1, doc2):
        """
        Hamming Distance, based on TF-IDF
        :param doc1: List of words
        :param doc2: List of words
        :return: List()
        """
        str1 = " ".join(doc1)
        str2 = " ".join(doc2)
        tfidf = self.get_tfidf(str1, str2)
        return sum(el1 != el2 for el1, el2 in zip(tfidf[0], tfidf[1]))

    def euclidean_distance(self, doc1, doc2):
        """
        Euclidean Distance, based on TF-IDF
        :param doc1: List of words
        :param doc2: List of words
        :return: List()
        """
        str1 = " ".join(doc1)
        str2 = " ".join(doc2)
        tfidf = self.get_tfidf(str1, str2)
        e_distance = distance.euclidean(tfidf[0], tfidf[1])
        return 1 / e_distance if (e_distance != 0) else 0
