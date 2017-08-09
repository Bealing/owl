# parse OWL file and store entities and classes into MYSQL DB
import rdflib, ontospy
import MySQLdb
import traceback

from datetime import datetime

OWL_FILE = "hdo.owl"
# property's URI
#ROOT_URI = "http://purl.obolibrary.org/obo/DOID_4"
#ID_URI="http://www.geneontology.org/formats/oboInOwl#id"
DEFINITION_URI = "http://purl.obolibrary.org/obo/IAO_0000115"
SYNONYM_URI = "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym"
DEPRECATED_URI = "http://www.w3.org/2002/07/owl#deprecated"
# mysql's information
DB = "owl"
USER = "root"
PASSWD = "123456"
# mysql operation: create a new table
CREATE_TABLE_SQL = '''
DROP TABLE if exists disease_ontology;
CREATE TABLE IF NOT EXISTS disease_ontology (
    id INT NOT NULL auto_increment primary key,
    do_id INT NOT NULL UNIQUE,
    do_uri VARCHAR(100) NOT NULL,
    do_name VARCHAR(200) NOT NULL,
    do_definition LONGTEXT,
    do_links TEXT(1000),
    do_synonyms TEXT(1000),
    do_parents_uri VARCHAR(100),
    do_ancestors_uri LONGTEXT,
    do_deprecated tinyint(1) DEFAULT 0
);
'''
# mysql operation: insert a record
INSERT_TABLE_SQL = '''
INSERT INTO disease_ontology 
    (do_id, do_uri, do_name, do_definition,
     do_links, do_synonyms, do_parents_uri, 
     do_ancestors_uri, do_deprecated)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
'''

class Owlparser():
    def __init__(self, hdo=None):
        try:
            # record's number
            self.count = 0
            # create database's connection
            self.db_conn = MySQLdb.connect(host='localhost', port=3306,
                                           user=USER, passwd=PASSWD,
                                           db=DB)
            db_cur = self.db_conn.cursor()
            print "db connected!"
            # create a new table
            db_cur.execute(CREATE_TABLE_SQL)
            db_cur.close()
            self.db_conn.commit()    
            # intialize OWL graph in memory
            self.hdo = hdo
            print "parser created!"
        except:
            # print exception's message
            traceback.print_exc()
            # close database's connection if an exception occurs
            self.db_conn.close()
    def __del__(self):
        try:
            self.db_conn.close()
        except:
            traceback.print_exc()

    def insert_one_record(self, values=None):
        '''
        execute a sql to insert a record
        values: variables tuple
        '''
        try:
            # update curser
            db_cur = self.db_conn.cursor()
            # execute a insert-sql
            if values:
                db_cur.execute(INSERT_TABLE_SQL, values)
            # close cursor to release connection resource
            db_cur.close()
            # commit
            self.db_conn.commit()
        except:
            print '--------------------------------------'
            print values
            print '--------------------------------------'
            traceback.print_exc()
    def parse_records(self, uri=""):
        '''
        parse records and store every record to mysql db recursively
        '''
        try:
            print "Processed:%s" % uri
            # Initially, get top level ontology classes as starting points
            if uri == "":
                top_class_list = self.hdo.ontologyClassTree()[0]
                for tcl in top_class_list:
                    self.parse_records(uri=tcl.uri)
                return
            # get do class
            disease_ontology = self.hdo.getClass(uri=uri)
            # get do's URI
            do_uri = disease_ontology.uri
            # do_id = int(disease_ontology.getValuesForProperty(rdflib.URIRef(ID_URI))[0].value[5:])
            # get do's id
            do_id = int(do_uri.split('_')[-1])
            # get do's name
            do_name = disease_ontology.bestLabel().value
            # get do's definition
            temp_definition = disease_ontology.getValuesForProperty(rdflib.URIRef(DEFINITION_URI))
            do_definition = r'\n'.join([item.value for item in temp_definition])
            # get do's synonyms
            temp_synonym = disease_ontology.getValuesForProperty(rdflib.URIRef(SYNONYM_URI))
            do_synonyms = r'|'.join([item.value for item in temp_synonym])
            # get do's parents' uri
            do_parents_uri = r'|'.join([item.uri for item in disease_ontology.parents()])
            # get do's ancestors' uri
            do_ancestors_uri = r'|'.join([item.uri for item in disease_ontology.ancestors()])
            # do is deprecated?
            temp_deprecated = disease_ontology.getValuesForProperty(rdflib.URIRef(DEPRECATED_URI))
            if temp_deprecated and temp_deprecated[0].value:
                do_deprecated = 1
            else:
                do_deprecated = 0

            # insert a record into table
            sql_values = (do_id, do_uri, do_name, do_definition, "",
                          do_synonyms, do_parents_uri, do_ancestors_uri, do_deprecated)
            self.insert_one_record(values=sql_values)
            # get the URIs of do's children and then parse them
            children = disease_ontology.children()
            for child in children:
                self.parse_records(uri=child.uri)
        except:
            print '--------------------------------------'
            print uri
            print '--------------------------------------'
            traceback.print_exc()

if __name__ == "__main__":
    print "Loading OWL from file into memory(about 15 minutes)..."
    hdo = ontospy.Ontospy(OWL_FILE)
    print "Create parser..."
    parser =  Owlparser(hdo)
    parser.parse_records()
    print "OWL was parsed finsuccessfully.\n %d records were stored into mysql." % parser.count
