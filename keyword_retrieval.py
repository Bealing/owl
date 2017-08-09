import MySQLdb
import json
import traceback

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

class DiseaseOntology():
    def __init__(self):
        self.id = None
        self.name = ""
        self.definition = ""
        self.synonym = []
        self.parents = []
        self.ancestors = []
        self.children = []
        self.deprecated = 0 # False
    def to_json(self):
        '''
        to json
        '''
        '''
        json_object = {}
        json_object['name'] = self.name
        json_object['definition'] = self.definition
        json_object['synonym'] = []
        json_object['synonym'].append(self.synonym)
        return str(json_object)
        '''
        return json.dumps(self.__dict__)
    def __repr__(self):
        return str(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]
    
class KeywordRetrieval():
    def __init__(self, keywords=None):
        self.keywords =keywords
        self.db_conn = None
        try:
            self.db_conn = MySQLdb.connect(host='localhost', port=3306,
                                           user='root', passwd='123456', db='owl')
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
                    (child.id, child.name, child.definition, child.deprecated) = record
                    children.append(child)
                db_cur.close()
            except:
                traceback.print_exc()
        else:
            print "parameter <uri> is empty."
        return children

    def __get_parents__(self, parents_list=""):
        '''
        get children's information tuple by parents' uri
        '''
        parents = []
        parents_uri_list = parents_list.split("|")
        try:
            db_cur = self.db_conn.cursor()
            for parents_uri in parents_uri_list:
                couut_parent =  db_cur.execute(SELECT_PARENTS_BY_URI % parents_uri)
                if couut_parent:
                    parent = DiseaseOntology()
                    (parent.id, parent.name, parent.definition, parent.deprecated) = db_cur.fetchone()
                    parents.append(parent)
        except:
            traceback.print_exc()
        db_cur.close()
        return parents

    def __get_ancestors__(self, ancestors_list=''):
        ancestors = []
        ancestors_uri_list = ancestors_list.split("|")
        print "----------",ancestors_uri_list
        try:
            for ancestor_uri in ancestors_uri_list:
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
            db_cur.execute(SELECT_TABLE_BY_NAME_SQL % self.keywords)
            results_name = db_cur.fetchall()
            for record in results_name:
                do = DiseaseOntology()
                do.id = record[0]
                do.name = record[2]
                do.definition = record[3]
                do.synonym.extend(record[4].split('|'))
                do.parents.extend(self.__get_parents__(parents_list=record[5]))
                do.ancestors.extend(self.__get_ancestors__(ancestors_list=record[6]))
                do.children.extend(self.__get_children__(uri=record[1]))
                do.deprecated = record[7]
                dos.append(do)

            db_cur.execute(SELECT_TABLE_BY_SYNONYM_SQL % self.keywords)
            results_synonym = db_cur.fetchall()
            for record in results_synonym:
                if record not in results_name:
                    # print "===:",record
                    do = DiseaseOntology()
                    do.id = record[0]
                    temp_synonym = record[4].split('|')
                    do.name = [item for item in temp_synonym if self.keywords in item.lower()][0]
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
        print dos[0]['ancestors']
if __name__ == '__main__':
    keywords='hyperuricemia'
    kr = KeywordRetrieval(keywords=keywords)
    kr.get_result()