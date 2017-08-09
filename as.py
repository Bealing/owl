def parse_records(uri=ROOT_URI):
    '''
    parse records and store every record to mysql db recursively
    '''
    try:
        
        disease_ontology = hdo.getClass(uri)
        print disease_ontology

        children = disease_ontology.children()
        for child in children:
            print child.uri
            parse_records(uri=child.uri)
    except:
        traceback.print_exc()

[
    {'definition': 'An acquired metabolic disease that has_material_basis_in an abnormally high level of uric acid in the blood.',
    'ancestors': None, 
    'synonym': ['(Blood urate raized) or (hyperuricemia)', 'uricacidemia'], 
    'name': 'hyperuricemia', 
    'deprecated': 0, 
    'children': [], 
    'parents': [{
        'definition': 'A disease of metabolism that has _material_basis_in enzyme deficiency or accumulation of enzymes or toxins which interfere with normal function due toan endocrine organ disease, organ malfunction, inadequate intake, dietary deficiency, or malabsorption.', 
        'ancestors': None, 
        'synonym': [], 
        'name': 'acquired metabolic disease', 
        'deprecated': 0, 
        'children': [], 
        'parents': [], 
        'id': 60158L}],
    'id': 1920L}, 
    {'definition': '',
    'ancestors': None,
    'synonym': [
        'Hypoxanthine-guanine phosphoribosyltransferase deficiency (disorder) [Ambiguous]', 
        'Lesch - Nyhan syndrome', 'deficiency of IMP pyrophosphorylase', 
        'Hypoxanthine-guanine phosphoribosyltransferase deficiency (disorder)', 
        'HG-PRT deficiency', 
        'hypoxanthine guaninephosphoribosyltransferase deficiency', 
        'Hypoxanthine-guanine-phosphoribosyltransferase deficiency (& [Lesch - Nyhan syndrome])',
         'Complete hypoxanthine-guanine phosphoribosyltransferase deficiency', 
         'X-linked hyperuricemia (disorder) [Ambiguous]', 'Lesch-Nyhan syndrome (disorder)',
          'Lesch-Nyhan syndrome'
          ], 
    'name': 'X-linked hyperuricemia (disorder) [Ambiguous]', 
    'deprecated': 0, 
    'children': [], 
    'parents': [
        {'definition': 'An inherited metabolic disorder involving dysfunction of purine and pyrimidine metabolism.', 'ancestors': None, 'synonym': [], 'name': 'purine-pyrimidine metabolic disorder', 
        'deprecated': 0, 'children': [], 'parents': [], 'id': 653L}], 
        'id': 1919L}]
