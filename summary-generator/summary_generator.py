from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def getExtractiveSummarization(text, ratio = 1.2):
    stopwordList = set (stopwords.words("english"))
    words = word_tokenize(text)
    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopwordList:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    
    
    sentences = sent_tokenize(text)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]
    
    average = int(sumValues / len(sentenceValue))
    
    summarySentenceList = []
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (ratio * average)):
            summarySentenceList.append(sentence)
    
    summary = " ".join(summarySentenceList)
    return summary

summary = getExtractiveSummarization("""@Tesmanian_com Excited for future of solar at Tesla!""", ratio=1.2)

# print(summary)