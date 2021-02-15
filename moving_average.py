def moving_average(data,window):
    """The partitions begin with window-1 None. Then follow partial lists, containing
       window-sized elements. We do this only up to len(data)-window+1 as the following
       partitions would have less then window elements."""

    parts = [None]*(window-1) + [ data[i:i+window] for i in range(len(data)-window+1)]
    #       The None's           The sliding window of window elements

    # we return None if the value is None else we calc the avg
    return [ sum(x)/window if x else None for x in parts] 
