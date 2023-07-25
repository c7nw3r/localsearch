def remove_punctuation(text: str):
    text = text.replace("?", "")
    text = text.replace("!", "")
    text = text.replace(".", "")
    text = text.replace(",", "")

    return text


def remove_stopwords(text: str, lang: str):
    from stop_words import get_stop_words

    stop_words = get_stop_words(lang)
    return " ".join([e for e in text.split(" ") if e.lower() not in stop_words])


def lemmatize(text: str, lang: str):
    import simplemma

    tokens = text.split(" ")
    tokens = [token for token in tokens if len(token) > 0]

    return " ".join([simplemma.lemmatize(token, lang=lang) for token in tokens])


def md5(text: str):
    from hashlib import md5
    return str(md5(text.encode("utf-8")).hexdigest())
