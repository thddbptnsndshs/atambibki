import os
import re
import json
from pybtex.database.input import bibtex
import logging
import yaml

with open('/Users/shikunova/atambibki/config.yaml') as cnf:
    config = yaml.safe_load(cnf)

logging.basicConfig(filename=config['log_path'],
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def walk_rootdir(rootdir, out_path):
    """
     Walks the root directory to save the list of .bib files.
     :param rootdir: str, root directory that will be walked to collect .bib filenames
     :param out_path: str, path to save the file
     :return: None
     """
    bib_fns = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith('.bib'):
                bib_fns.append(os.path.join(subdir, file))
    # print(bib_fns)
    with open(out_path, 'w') as f:
        json.dump(bib_fns, f)


def read_bib_file(path):
    parser = bibtex.Parser()
    try:
        bib_data = parser.parse_file(path)
    except:
        logging.info(f'error in file {path}')
        return []
    return [{
        '_id': key,
        'type': val.type,
        'properties': dict(val.fields),
        'string': val.to_string('bibtex'),
    } for key, val in bib_data.entries.items()]


def parse_biber_errors(biber_output):
    error_rgx = r"WARN - I didn't find a database entry for '(.+?)'"
    keys_not_found = re.findall(error_rgx, biber_output)
    return keys_not_found
