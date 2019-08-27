from textblob import TextBlob as tb


# the single function for computing sentiment of a text
def compute_sentiment(input):
    output = float(tb(input).sentiment.polarity)
    return output


def sentiment_fast(comments, like_counts, params={"getBest": True, "getWorst": True, "getSentiment": True, "getPosRatio": True}):
    # internal parameters
    best_comments_max_count = 10
    worst_comments_max_count = 10

    comments_sentiments = []
    comments_count = len(comments)

    # compute sentiment of each comment
    i = 0
    while i < comments_count:
        this_sentiment = compute_sentiment(comments[i])
        comments_sentiments.append(this_sentiment)
        i = i + 1

    results = {}

    # build comment dictionaries
    comment_dicts = []
    i = 0
    while i < comments_count:
        this_comment_dict = {"comment": comments[i], "sentiment": comments_sentiments[i], "likeCount": like_counts[i]["likeCount"]}
        comment_dicts.append(this_comment_dict)
        i = i + 1

    # determine whether we need the sorted comment dictionaries (on the sentiment from the largest to the smallest)
    is_sorted_comment_dicts_needed = False
    if params["getBest"]:
        is_sorted_comment_dicts_needed = True
    else:
        if params["getWorst"]:
            is_sorted_comment_dicts_needed = True

    # build the sorted comment dictionaries (on the sentiment from the largest to the smallest) if it is needed
    if is_sorted_comment_dicts_needed is True:
        sorted_comment_dicts = []
        i = 0
        while i < comments_count:
            this_comment_dict = comment_dicts[i]
            sorted_comment_dicts.append(this_comment_dict)
            i = i + 1

        i = 0
        while i < comments_count:
            target_item_index = i
            target_compared = sorted_comment_dicts[target_item_index]["sentiment"]

            j = i + 1
            while j < comments_count:
                test_compared = sorted_comment_dicts[j]["sentiment"]
                if test_compared > target_compared:
                    target_item_index = j
                    target_compared = sorted_comment_dicts[target_item_index]["sentiment"]
                j = j + 1

            if target_item_index > i:
                swap_item = sorted_comment_dicts[i]
                sorted_comment_dicts[i] = sorted_comment_dicts[target_item_index]
                sorted_comment_dicts[target_item_index] = swap_item

            i = i + 1

    # generate "best_comments"
    if params["getBest"]:
        best_comments = []
        i = 0
        while (i < best_comments_max_count) and (i < comments_count):
            this_comment_dict = sorted_comment_dicts[i]
            if this_comment_dict["sentiment"] > 0:
                best_comments.append(this_comment_dict["comment"])
            i = i + 1
        results["best_comments"] = best_comments

    # generate "worst_comments"
    if params["getWorst"]:
        worst_comments = []
        i = 0
        while (i < worst_comments_max_count) and (i < comments_count):
            this_item_index = comments_count - i - 1
            this_comment_dict = sorted_comment_dicts[this_item_index]
            if this_comment_dict["sentiment"] < 0:
                worst_comments.append(this_comment_dict["comment"])
            i = i + 1
        results["worst_comments"] = worst_comments

    # generate "textblob_sentiment"
    if params["getSentiment"]:
        if comments_count == 0:
            result = 0
        else:
            result = 0
            divider = 0
            i = 0
            while i < comments_count:
                this_comment_dict = comment_dicts[i]
                result = result + (this_comment_dict["sentiment"] * (this_comment_dict["likeCount"] + 1))
                divider = divider + this_comment_dict["likeCount"]
                i = i + 1
            divider = comments_count + divider
            result = result / divider
        results["textblob_sentiment"] = result

    # generate "comment_positive_ratio"
    if params["getPosRatio"]:
        if comments_count == 0:
            result = 0
        else:
            result = 0
            i = 0
            while i < comments_count:
                this_comment_dict = comment_dicts[i]
                if this_comment_dict["sentiment"] > 0:
                    result = result + 1
                i = i + 1
            result = result / comments_count
        results["comment_positive_ratio"] = result

    return results
