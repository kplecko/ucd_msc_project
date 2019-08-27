# Analytics AI Parameters Needed:
```metadata json
{
    "query": string,
    "results_max_count": integer,
    "source": string ('live' or 'cached')
}
```

# Feedback Parameters Needed
```metadata json
{
    "feedback": integer
}
```

# Analytics AI Return JSON Format:
```metadata json
{
	"video_statistic_data": [
	{
		"video_id": string,
		"data":{ (dict)
			"title": string,
			"likeCount": integer,
			"dislikeCount": integer,
			"viewCount": integer,
			"en_transcript":{
				"relevant_book": string,
				"trans_similarity": float,
				"freq_trans": [ list()
					{
						"word": string,
						"weight": integer
					}
				],
				"trans_similarity_nor": integer [0, 10],
				"table_of_contents": absent or [(list)
				    {
				        "start": number,
				        "end": number,
				        "content": string
				    }
				],
				"entities": [(list)
				    {
				        'entity': string,
				        'type': string,
				        'salience': float,
				        "wikipedia_url": string
				    }
				]
			}
			"comments":{ dict()
				"sentiment": {
				    "best_comments": list(),
				    "worst_comments": list(),
				    "comment_positive_ratio": float,
				    "textblob_sentiment": float
				}
			}
		}
	}
	],
	"video_count": integer
}
```