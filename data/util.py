

def make_get_url(url,param):
    url += "?"
    first = True
    for it in param:
        if not first:
            url += "&"
        url += it + "=" + str(param[it]);
        first = False
    
    return url;