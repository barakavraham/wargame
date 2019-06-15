from re import sub

def format_response(res):
    return sub(r'\n\s+', ' ', res.data.decode('utf-8'))
