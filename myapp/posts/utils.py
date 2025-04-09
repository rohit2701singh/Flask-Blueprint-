# bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
# If you do not provide tags and attributes to bleach.clean(), then it uses safe default values internally
# tags not in this dict will be escaped or stripped from the text

allowed_tags = {
    'a', 'abbr', 'b', 'blockquote', 'code', 'em', 'i', 'li',
    'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'
}    

custom_attrs = {
    'a': ['href', 'title'],
    'code': ['class']
}