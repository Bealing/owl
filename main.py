from text_processor import TextProcessor
from keyword_retrieval import KeywordRetrieval

if __name__ == "__main__":
    text = raw_input("Please input your text (It's better not to input more than 15 words)\n>> ")
    # create text processor to get keywords
    text_processor = TextProcessor(text = text)
    keywords = text_processor.get_keywords()
    if keywords:
        print "Extracted keywords:", keywords
        for word in keywords:
            print "="*100
            print ("{0:^100}".format("<< Keyword: %s >>" % word))
            # create KeywordRetrieval instance to get keyword's retrieval
            kr = KeywordRetrieval(keyword=word)
            dos = kr.get_result()
            if dos:
                # sorted by name's length(similarity)
                for do in sorted(dos, key=lambda do: len(do.name)):
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
                print "\n\tTotal:%d records" % len(dos)
            else:
                print "There was nothing about keyword<%s>." % word
        print "="*100
    else:
        print "The model does not extract any keywords"