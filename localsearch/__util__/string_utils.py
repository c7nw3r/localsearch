from localsearch.__spi__ import Lang


def remove_punctuation(text: str):
    text = text.replace("?", "")
    text = text.replace("!", "")
    text = text.replace(".", "")
    text = text.replace(",", "")

    return text


def remove_stopwords(text: str, lang: Lang):
    from stop_words import get_stop_words

    stop_words = get_stop_words(lang)
    return " ".join([e for e in text.split(" ") if e.lower() not in stop_words])


def lemmatize(text: str, lang: Lang):
    import simplemma

    tokens = text.split(" ")
    tokens = [token for token in tokens if len(token) > 0]

    return " ".join([simplemma.lemmatize(token, lang=lang) for token in tokens])


def md5(text: str):
    from hashlib import md5
    return str(md5(text.encode("utf-8")).hexdigest())


# TODO: rename chunk_size, window_size to window_size, overlap
def split_sentences(
        text: str,
        language: Lang,
        chunk_size: int = 3,
        window_size: int = 1
) -> List[str]:
    import pysbd
    seg = pysbd.Segmenter(language=language, clean=False)
    sentences = seg.segment(text)

    return [" ".join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size-window_size)]


def split_characters(
        text: str,
        window_size: int = 500,
        overlap: int = 100
) -> List[str]:

    return [text[i: i+window_size] for i in range(0, len(text), window_size-overlap)]
