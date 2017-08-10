# *--coding:utf-8--*
from datetime import datetime
import traceback;
import nltk
from nltk.stem.lancaster import LancasterStemmer  
from nltk.corpus import stopwords, brown

class TextProcessor():
    '''
    process text inputed by user
    '''
    def __init__(self, text=""):
        # text inputed by user
        self.text = text

    def __get_corrected_pos__(self, words_tagged=[]):
        '''
        correcte words pos based on brown
        '''
        def get_word_pos(word_set=None, word=""):
            '''
            get word's pos and its frequent according to brown
            '''
            tags = [_tag for (_word, _tag) in word_set if _word == word.lower()]
            # word exissts in brown
            if tags:
                # calculate frequent of word's tags
                frequent = nltk.FreqDist(tags)
                # get the most probable pos
                return frequent.max()
            else:
                return ""
        # corrected word and its pos
        words_corrected_tag = []
        # get brown tagged words
        brown_tagged = brown.tagged_words(categories=['reviews', 'editorial'])
        # get stopwords in English
        stopwords_list = stopwords.words('english')
        # correct word's pos one-by-one
        for word, word_pos in words_tagged:
            # if word_pos[:2] in ['JJ', 'NN', 'VB']:
            if word not in stopwords_list and word_pos[0:2] not in ['VB', 'JJ', 'CD']:
                # get tagged word's pos
                temp_word_pos = get_word_pos(word_set=brown_tagged, word=word)
                if temp_word_pos:
                    # use tagged word's pos
                    words_corrected_tag.append((word, temp_word_pos))
                else:
                    # self-defined pos for words
                    patterns = [
                        (r'.*[ts]ion$', 'NNP'),
                        (r'.*om[ae]$', 'NNP'),
                        (r'.*[tsl]is$', 'NNP'),
                        (r'.*[cd]er$', 'NNP'),
                        (r'.*[mnpsxd]ia$', 'NNP'),
                        (r'.*[pt]hy$', 'NNP'),
                        (r'.*asm$', 'NNP'),
                        (r'.*mor$', 'NNP'),
                        (r'.*ncy$', 'NNP'),
                        (r'.*', 'NN') # nouns (default)
                    ]
                    # create a regexp tagger
                    regexp_tagger = nltk.RegexpTagger(patterns)
                    # tag word by regexp tagger
                    temp_word, temp_word_pos = regexp_tagger.tag([word, ])[0]
                    words_corrected_tag.append((temp_word, temp_word_pos))
            else:
                words_corrected_tag.append((word, word_pos))
        return words_corrected_tag

    def __get_chunck__(self, words_tagged=[]):
        '''
        get NP-chunck of tagged words
        '''
        chunck = []
        if words_tagged:
            try:
                # create grammer
                basic_grammar = r'''NP: {<JJ|VBD|VBG|NN.*>*<NN.*>+<CD>?}'''
                # create parser
                regexp_parser = nltk.RegexpParser(basic_grammar)
                # generate grammer tree
                result_tree = regexp_parser.parse(words_tagged)
                # extract 'NP' subtree
                for subtree in result_tree.subtrees():
                    if subtree.label() == 'NP':
                        # create a chunck by joining words
                        chunck.append(" ".join([word for (word, pos) in subtree.leaves()]))
            except:
                traceback.print_exc()
        return chunck

    def get_keywords(self):
        '''
        get keyword list from text
        '''
        keywords = []
        # word tokenize
        words = nltk.word_tokenize(self.text)
        # tag words
        words_tagged = nltk.pos_tag(words)
        #print words_tagged
        # corrected word's pos
        words_corrected_tag = self.__get_corrected_pos__(words_tagged=words_tagged)
        #print words_corrected_tag
        # get NP-chunck
        keywords.extend(self.__get_chunck__(words_corrected_tag))
        # remove duplicates
        return list(set(keywords))

if __name__ == "__main__":
    text = "What made you want to look up Waardenburg syndrome type 2D? Please tell us where you read or heard it (including the quote, if possible)."
    text2 = "Waardenburg syndrome is usually inherited in an autosomal dominant pattern, which means one copy of the altered gene is sufficient to cause the disorder. "
    start = datetime.now()
    text_processor = TextProcessor(text = text2)
    print text_processor.get_keywords()
    print "Total:", datetime.now()-start
