def flatten(some_list, tuples=True):
    # only lists (and tuples, unless tuples=False) are expanded; a string
    # or any other item stays whole at every depth
    nested = (list, tuple) if tuples else list
    flat = []
    for item in some_list:
        if isinstance(item, nested):
            flat.extend(flatten(item, tuples))
        else:
            flat.append(item)
    return flat
