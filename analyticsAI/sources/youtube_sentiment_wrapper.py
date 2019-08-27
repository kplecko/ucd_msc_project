# from youtube_sentiment import Youtube_Google_Sentiment
from sources.youtube_sentiment import Sentiment


def sentiment_wrapper(comments, likecount, params={"getBest": True, "getWorst": True, "getSentiment": True, "getPosRatio": True}):
    sentiment_obj = Sentiment()
    results = {}
    lc = []
    for val in likecount:
        lc.append(val["likeCount"])
    if params["getBest"]:
        best_comments = sentiment_obj.textblobsentiment_best(comments, lc)
        if best_comments:
            results["best_comments"] = best_comments
    if params["getWorst"]:
        worst_comments = sentiment_obj.textblobsentiment_worst(comments, lc)
        if worst_comments:
            results["worst_comments"] = worst_comments
    if params["getSentiment"]:
        results["textblob_sentiment"] = sentiment_obj.textblobsentiment(comments, lc)
    if params["getPosRatio"]:
        results["comment_positive_ratio"] = sentiment_obj.textblobsentiment_ratio(comments)
    return results
