import nltk
from nltk.stem.lancaster import LancasterStemmer  
from nltk.corpus import stopwords, brown
from text_processor import TextProcessor
from keyword_retrieval import KeywordRetrieval
from datetime import datetime

if __name__ == "__main__":
    text = raw_input("Please input your text (It's better not to input more than 15 words)\n>> ")
    # case based ontology
    print "Case: [[ Ontology-based method]]\nText :%s" % text
    # create text processor to get keywords
    start = datetime.now()
    text_processor = TextProcessor(text = text)
    keywords = text_processor.get_keywords()
    if keywords:
        dos = {}
        print "Extracted ontology keywords:", keywords
        for word in keywords:
            kr = KeywordRetrieval(keyword=word)
            dos[word] = kr.get_result()
    else:
        print "The model does not extract any keywords"
    end = datetime.now()
    time_1 = end - start
    for word in keywords:
        if dos[word]:
            # sorted by name's length(similarity)
            for do in sorted(dos[word], key=lambda do: len(do.name)):
                # print do's information 
                print "_"*100
                print ("{0:>11}:  {1:<85}".format("Name", do.name))
                # definition
                if do.definition:
                    definition_str = do.definition
                else:
                    definition_str = 'none'
                print ("{0:>11}:  {1:<85}".format("Definition", definition_str))
                # synonym
                print ("{0:>11}:  {1:<85}".format("Synonym", ", ".join(do.synonym)))
                # parents
                if do.parents:
                    parents_str = ", ".join([parent.name for parent in do.parents])
                else:
                    parents_str = 'none'
                print ("{0:>11}:  {1:<85}".format("Parents", parents_str))
                # chidlren
                if do.children:
                    children_str = ", ".join([child.name for child in do.children])
                else:
                    children_str = 'none'
                print ("{0:>11}:  {1:<85}".format("Children",children_str))
                # ancestors
                if do.ancestors:
                    ancestors_str = " > ".join([ancestor.name for ancestor in do.ancestors[::-1]])
                else:
                    ancestors_str = 'none'
                print ("{0:>11}:  {1:<85}".format("Ancestors", ancestors_str))
                # deprecated
                if do.deprecated:
                    deprecated_str = "yes"
                else:
                    deprecated_str = "no"
                print ("{0:>11}:  {1:<85}".format("Deprecated", deprecated_str))
            # total records
            print "\n\tTotal:%d records" % len(dos[word])
        print "="*100

    # case based traditional method
    print "Case: [[ traditional method]]\nText :%s" % text
    # create text processor to get keywords
    words = nltk.word_tokenize(text)
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%'] 
    words_cleand = [word for word in words if word.lower() not in stopwords.words('english') and word.lower() not in english_punctuations]
    if words_cleand:
        dos = []
        print "Extracted keywords:", words_cleand
        for word in words_cleand:
            kr = KeywordRetrieval(keyword=word)
            dos.extend(kr.get_result())
    else:
        print "The model does not extract any keywords"
    dos = list(set(dos))
    end = datetime.now()
    time_2 = end - start
    for do in sorted(dos, key=lambda do: len(do.name)):
        # print do's information 
        print "_"*100
        print ("{0:>11}:  {1:<85}".format("Name", do.name))
    # total records
    print "\n\tTotal:%d records" % len(dos)
    print "="*100
    
    print ("\n{0:^100}\n".format("<<Performance Comparisons >>"))
    print 'Ontology-based method:', time_1
    print 'traditional method:', time_2
