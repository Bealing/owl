import nltk
from nltk.stem.lancaster import LancasterStemmer  
from nltk.corpus import stopwords
from nltk.corpus import brown

def preprocess_text(text=""):
    '''
    Preprocess:
    1) Sentence Tokenizing
    2) Word Tokenizing
    3) Stopwords Removing(including punctuations)
    4) Pos Tagging
    5) Keywords Extracting
    '''
    
    text = "What made you want to look up hyperuricemia? Please tell us where you read or heard it (including the quote, if possible)."
    # Sentence Tokenizing
    sents = nltk.sent_tokenize(text.lower())
    # Word Tokenizing
    words = []
    for sent in sents:
        #sent= sent[0].lower() +sent[1:]
        words.extend(nltk.word_tokenize(sent))
    #print words
    # remove punctuations
    #english_punctuations = ',.:?{}[]~!@#$%^&*()'
    #words_cleand = [word for word in words if word not in list(english_punctuations)]
    #print words_cleand
    # stemming
    #stemmer = LancasterStemmer()
    #words_stemmed = [stemmer.stem(word) for word in words_cleand]
    #print words_stemmed
    # remove stopwords
    #words_filtered = [word for word in words_cleand if word not in stopwords.words('english')]
    #print words_filtered
    # tag pos
    words_tagged = nltk.pos_tag(words)

    brown_tagged_sents = brown.tagged_sents(categories='news')
    #brown_sents = brown.sents(categories='news')

    patterns = [
        (r'.*mia','NNP'),
        (r'.*','NN')
    ]
    regexp_tagger = nltk.RegexpTagger(patterns)
    print regexp_tagger.tag(words)
    print regexp_tagger.evaluate(brown_tagged_sents)

    fd = nltk.FreqDist(brown.words())
    cfd = nltk.ConditionalFreqDist(brown.tagged_words())
    most_freq_words = fd.keys()[:100]
    likely_tags = dict((word, cfd[word].max()) for word in most_freq_words)
    print likely_tags
    baseline_tagger = nltk.UnigramTagger(model=likely_tags)
    print baseline_tagger.tag(words)
    baseline_tagger.evaluate(brown_tagged_sents)
    return words_tagged

if __name__ == "__main__":
    #text = raw_input()
    print preprocess_text("")