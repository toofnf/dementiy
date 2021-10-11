import string


class Cleaner(object):

    def transform(self, sentence):
        raise NotImplementedError


class NaiveCleaner(Cleaner):

    def transform(self, X):
        def clean(s):
            translator = str.maketrans("", "", string.punctuation)
            return s.translate(translator)

        return [clean(x).lower() for x in X]
