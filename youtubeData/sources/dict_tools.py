# some tools about Python dictionaries


def dict_get_existent(dict, key, default=None):
    value = default
    if key in dict:
        value = dict[key]
    return value


def dict_get_nonnull(dict, key, default=None):
    value = default
    if key in dict:
        if dict[key] is not None:
            value = dict[key]
    return value


def dict_get_excluding(dict, key, excluded_values_list, default=None):
    value = default

    if key in dict:
        possible_value = dict[key]
        count = len(excluded_values_list)
        is_excluded = False
        i = 0
        while (i < count) and (is_excluded is False):
            if possible_value == excluded_values_list[i]:
                is_excluded = True
            i = i + 1

        if is_excluded is False:
            value = possible_value

    return value


def dict_add_nonnull(dict, key, value):
    if value is not None:
        dict.append(key, value)


def dict_has_nonnull(dict, key):
    isHave = False
    if key in dict:
        if dict[key] is not None:
            isHave = True
    return isHave


def dict_has_items_nonnull(dict, keys):
    isHaveAll = True
    count = len(keys)
    i = 0
    while (i < count) and (isHaveAll is True):
        isHaveAll = dict_has_nonnull(dict, keys[i])
        i = i + 1
    return isHaveAll
