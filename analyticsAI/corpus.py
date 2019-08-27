from __init__ import application_path


def get_keywords_corpus(topic_name):
    topic_name = topic_name.lower()

    if topic_name == "python":
        keywords_index_corpus = keywords_from_index(application_path, topic_name)
        keywords_book_corpus = keywords_from_book(application_path, topic_name)

        keywords_corpus = list(set(keywords_index_corpus).intersection(set(keywords_book_corpus)))
        return keywords_corpus

    if topic_name == "java":
        return keywords_from_index(application_path, topic_name)

    if topic_name == "hadoop":
        return keywords_from_index(application_path, topic_name)

    if topic_name == "f#":
        return keywords_from_index(application_path, topic_name)

    if topic_name == "cassandra":
        return keywords_from_index(application_path, topic_name)

    if topic_name == "r programming":
        return keywords_from_index(application_path, "r")

    return False


def keywords_from_index(application_path, topic_name):
    keywords_view_path = "/data/Book_Keywords/" + topic_name + "_keywords_index.txt"
    keywords_index_path = application_path + keywords_view_path
    with open(keywords_index_path, "r") as v:
        keywords_index_corpus = v.read().splitlines()

    return keywords_index_corpus


def keywords_from_book(application_path, topic_name):
    keywords_book_path = "/data/Book_Keywords/" + topic_name + "_keywords_book.txt"
    keywords_book_path = application_path + keywords_book_path
    with open(keywords_book_path, "r") as b:
        keywords_book_corpus = b.read().splitlines()

    return keywords_book_corpus
