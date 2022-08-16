import pyjokes
from googletrans import Translator


def get_joke():
    joke_v = []
    translator = Translator()
    joke = pyjokes.get_joke(category='all')
    translated_joke = translator.translate(joke, dest="ru")
    joke_v.append(joke)
    joke_v.append(translated_joke.text)
    return joke_v
