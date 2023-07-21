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
    return " ".join([simplemma.lemmatize(token, lang=lang) for token in text.split(" ")])
