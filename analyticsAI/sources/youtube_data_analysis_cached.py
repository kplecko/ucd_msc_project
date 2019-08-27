from sources.youtube_data_analysis_db_search import db_search


def analyticsai_cached(params):
    '''
    Analytics AI cached search
    :param params: parameter from front end
}
    :return: Database search result
    '''
    return db_search(params)
