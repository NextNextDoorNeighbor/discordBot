import goslate

def trans():
    gs = goslate.Goslate()
    translatedText = gs.translate('Hello World','de')

    print(translatedText)