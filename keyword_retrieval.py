import MySQLdb
import traceback

from disease_ontology import  DiseaseOntology

# mysql's information
DB = "owl"
USER = "root"
PASSWD = "123456"

SELECT_TABLE_BY_NAME_SQL = r'''
select do_id, do_uri, do_name, do_definition, do_synonyms, do_parents_uri, do_ancestors_uri, do_deprecated from disease_ontology where do_name like '%%%s%%'
'''
SELECT_TABLE_BY_SYNONYM_SQL = r'''
select do_id, do_uri, do_name, do_definition, do_synonyms, do_parents_uri, do_ancestors_uri, do_deprecated from disease_ontology where do_synonyms like '%%%s%%'
'''
SELECT_CHILDREN_BY_URI = r'''
select do_id, do_name, do_definition, do_deprecated from disease_ontology where do_parents_uri = '%s'
'''
SELECT_PARENTS_BY_URI = r'''
select do_id, do_name, do_definition, do_deprecated from disease_ontology where do_uri = '%s'
'''

class KeywordRetrieval():
    '''
    retrieve information related with keywords 
    '''
    def __init__(self, keyword=None):
        self.keyword =keyword
        self.db_conn = None
        try:
            # connect to database 
            self.db_conn = MySQLdb.connect(host='localhost', port=3306,
                                           user=USER, passwd=PASSWD, db=DB)
        except:
            self.db_conn.close()
            traceback.print_exc()

    def __get_children__(self, uri=""):
        '''
        get children's information tuple by parents' uri
        '''
        children = []
        if uri:
            try:
                db_cur = self.db_conn.cursor()
                #count_children = db_cur.execute(SELECT_CHILDREN_BY_URI % uri)
                db_cur.execute(SELECT_CHILDREN_BY_URI % uri)
                results_children = db_cur.fetchall()
                # get children's ontology
                for record in results_children:
                    child = DiseaseOntology()
                    # save key information of children
                    (child.id, child.name, child.definition, child.deprecated) = record
                    children.append(child)
                db_cur.close()
            except:
                traceback.print_exc()
        # else:
        #     print "parameter <uri> is empty."
        return children

    def __get_parents__(self, parents_list=""):
        '''
        get children's information tuple by parents' uri
        '''
        parents = []
        # split parents uri
        parents_uri_list = parents_list.split("|")
        try:
            db_cur = self.db_conn.cursor()
            # get parent's ontology iteratively
            for parents_uri in parents_uri_list:
                # execute SQL operation
                count_parent =  db_cur.execute(SELECT_PARENTS_BY_URI % parents_uri)
                if count_parent:
                    parent = DiseaseOntology()
                    # save key information of parents
                    (parent.id, parent.name, parent.definition, parent.deprecated) = db_cur.fetchone()
                    parents.append(parent)
        except:
            traceback.print_exc()
        db_cur.close()
        return parents

    def __get_ancestors__(self, ancestors_list=''):
        '''
        get ontology's ancestors by URI
        '''
        ancestors = []
        # split ancestors URI
        ancestors_uri_list = ancestors_list.split("|")
        try:
            # get ancestor's ontology iteratively
            for ancestor_uri in ancestors_uri_list:
                # get parent's parents ...
                ancestor = self.__get_parents__(parents_list=ancestor_uri)
                ancestors.extend(ancestor)
        except:
            traceback.print_exc()
        return ancestors

    def get_result(self):
        '''
        get searching result
        '''
        dos = []
        try:
            db_cur = self.db_conn.cursor()
            # execute SQL Select by name
            db_cur.execute(SELECT_TABLE_BY_NAME_SQL % self.keyword)
            # fetch result set 
            results_name = db_cur.fetchall()
            for record in results_name:
                do = DiseaseOntology()
                # process each filed
                do.id = record[0] # do_id
                do.name = record[2] # do_name
                do.definition = record[3] # do_definition
                do.synonym.extend(record[4].split('|')) # do_synonyms
                do.parents.extend(self.__get_parents__(parents_list=record[5])) # do_parents
                do.ancestors.extend(self.__get_ancestors__(ancestors_list=record[6])) # do_ancestors
                do.children.extend(self.__get_children__(uri=record[1])) # do_uri
                do.deprecated = record[7] # do_deprecated
                dos.append(do)
            # execute SQL Select by synonym
            db_cur.execute(SELECT_TABLE_BY_SYNONYM_SQL % self.keyword)
            # fetch result set 
            results_synonym = db_cur.fetchall()
            for record in results_synonym:
                # remove duplicated record
                if record not in results_name:
                    do = DiseaseOntology()
                    # process ecah filed of records
                    do.id = record[0]
                    temp_synonym = record[4].split('|')
                    do.name = [item for item in temp_synonym if self.keyword.lower() in item.lower()][0]
                    do.definition = record[3]
                    do.synonym.extend(temp_synonym)
                    do.synonym.append(record[2])
                    do.parents.extend(self.__get_parents__(parents_list=record[5]))
                    do.ancestors.extend(self.__get_ancestors__(ancestors_list=record[6]))
                    do.children.extend(self.__get_children__(uri=record[1]))
                    do.deprecated = record[7]
                    dos.append(do)
        except:
            traceback.print_exc()
        #print dos[0]['ancestors']
        return dos

if __name__ == '__main__':
    keywords='hyperuricemia'
    kr = KeywordRetrieval(keyword=keywords)
    print kr.get_result()