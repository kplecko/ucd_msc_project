from sources import youtube_text_keywords
from sources import youtube_text_processing


# Given a separate transcript text (input_text), generate the corresponding text in the table of contents
def generate_table_of_contents_text(input_text):
    list_clean_text = youtube_text_processing.lemmatize_verbs(youtube_text_processing.normalization(input_text))
    output_ordered_dict = youtube_text_keywords.get_keywords(list_clean_text, 4)
    output_list = list(output_ordered_dict.keys())
    output_text = ", ".join(output_list)
    return output_text
