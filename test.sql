CREATE DATABASE IF NOT EXISTS owl DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

use owl;

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

SELECT count(*) FROM owl.disease_ontology;

select right(do_name,3) as strend, count(right(do_name,3)) as num
from disease_ontology
group by right(do_name,3)
order by count(right(do_name,3)) desc;

select count(*) from disease_ontology where do_name like '% with %' or do_name like '% of %';
select count(*) from disease_ontology where do_name like '% and %';