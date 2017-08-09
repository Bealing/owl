import nltk
from nltk.stem.lancaster import LancasterStemmer  
from nltk.corpus import stopwords, brown

from datetime import datetime


class TextProcessor():
    '''
    '''
    def __init__(self, text="", frequent_threshold=0.1):
        # text inputed by user
        self.text = text
        # calculate based on Empirical knowledge. frequent_threshold: 0.0~1.0
        self.frequent_threshold = int(frequent_threshold * 100) 

    def __get_corrected_pos__(self, words_tagged=[]):
        #print words_tagged
        def get_word_pos(word_set=None, word=""):
            '''
            get word's pos and its frequent according to brown
            '''
            tags = [_tag for (_word, _tag) in word_set if _word == word.lower()]
            if tags:
                frequent = nltk.FreqDist(tags)
                #print frequent
                max_value = frequent.max()
                return (max_value, frequent[max_value])
            else:
                return ("", 0)
        words_corrected_tag = []
        brown_tagged = brown.tagged_words(categories='news')
        for word, word_pos in words_tagged:
            # if word_pos[:2] in ['JJ', 'NN', 'VB']:
            if word_pos[:2] == 'NN':
                (temp_word_pos, temp_word_frequent) = get_word_pos(word_set=brown_tagged, word=word)
                if word_pos == temp_word_pos:
                    words_corrected_tag.append((word, word_pos))
                elif temp_word_frequent >= self.frequent_threshold:
                    words_corrected_tag.append((word, temp_word_pos))
                else:
                    patterns = [
                        (r'.*[ts]ion$', 'NN'),
                        (r'.*om[ae]$', 'NNP'),
                        (r'.*[ts]is$', 'NNP'),
                        (r'.*[cd]er$', 'NNP'),
                        (r'.*[mns]ia$', 'NNP'),
                        (r'.*[pt]hy$', 'NNP'),
                        (r'.*asm$', 'NNP'),
                        (r'.*mor$', 'NNP'),
                        (r'.*ncy$', 'NNP'),
                        (r'.*', 'NN') # nouns (default)
                    ]
                    regexp_tagger = nltk.RegexpTagger(patterns)
                    temp_word, temp_word_pos = regexp_tagger.tag([word, ])[0]
                    words_corrected_tag.append((temp_word, temp_word_pos))
                
            else:
                words_corrected_tag.append((word, word_pos))
        print words_corrected_tag
        return words_corrected_tag

    def get_keywords(self):
        '''
        get keyword list from text
        '''
        keywords = []
        words = nltk.word_tokenize(self.text)
        words_tagged = nltk.pos_tag(words)
        #print words_tagged
        words_tagged_corrected = self.__get_corrected_pos__(words_tagged=words_tagged)
        #print words_tagged_corrected

        basic_grammar = r'''NP: {<DT|JJ|NN.*|IN>*<NN.*>+<CD>?}'''
        regexp_parser = nltk.RegexpParser(basic_grammar)
        result_tree = regexp_parser.parse(words_tagged_corrected)
        for subtree in result_tree.subtrees():
            if subtree.label() == 'NP':
                keywords.append(" ".join([word for (word, pos) in subtree.leaves()]))

        expanded_grammar = r'''NP: {<DT|JJ|NN.*|IN|CC>*<NN.*>+<CD>?}'''
        regexp_parser = nltk.RegexpParser(expanded_grammar)
        result_tree = regexp_parser.parse(words_tagged_corrected)
        for subtree in result_tree.subtrees():
            if subtree.label() == 'NP':
                keywords.append(" ".join([word for (word, pos) in subtree.leaves()]))
        return list(set(keywords))


if __name__ == "__main__":
    text = "What made you want to look up hyperuricemia? Please tell us where you read or heard it (including the quote, if possible)."
    start = datetime.now()
    text_processor = TextProcessor(text = text)
    print text_processor.get_keywords()
    print "Total:", datetime.now()-start
