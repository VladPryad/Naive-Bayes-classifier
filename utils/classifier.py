from utils.db import Sample, Word

class NaiveBayes:
    @staticmethod
    def classify(text):
        hamProb = 1
        spamProb = 1
        for word in text.split():
            words = Word.objects.filter(word = word.lower())

            if(len(words) != 0):
                wordObj = words[0]
                hamProb *= wordObj.hamProbNormalized
                spamProb *= wordObj.spamProbNormalized
            else:
                pass
        return ( spamProb*0.5, hamProb*0.5 )