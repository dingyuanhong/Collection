
def make_get(param):
    uri = "";
    first = True
    for it in param:
        if not first:
            uri += "&"
        uri += it + "=" + str(param[it]);
        first = False
    return uri;

def make_get_url(url,param):
    d = make_get(param)
    if len(d) > 0:
        url += "?" + d;
    return url;