import os


def stopwords():
    application_path = os.path.abspath(os.path.join(os.getcwd(), ""))
    stopword_path = application_path + "/data/Stopwords/stopwords.csv"
    file = open(stopword_path, "r")
    lines = []
    for line in file:
        formatted = line.replace("\n", "")
        lines.append(formatted)
    return lines
