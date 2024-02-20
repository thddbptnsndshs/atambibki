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


# class BibEntry:
#     def __init__(self, entry_string):
#         self.entry_string = entry_string
#         self.entry_dict = self.bib2dict(entry_string)
#
#     # TODO: check the values in properties for capitalization and parenthesize capitalized words automatically
#     @staticmethod
#     def bib2dict(entry_string):
#         """
#           Processes the bib entry into dict format
#           :param entry_string: str, entry string
#           :return: entry_dict, dict -- dictionary of entry properties of structure {'key': key, 'properties': [...]}
#           """
#         entry_dict = dict()
#         type_key_rgx = r'@(?P<type>.+)\{(?P<key>.+),'
#         properties_rgx = r'\s*(?P<prp>.+)\s?=\s?\{?(?P<val>.+?)\}[,$\n]'
#         try:
#             entry_dict['type'] = re.search(type_key_rgx, entry_string).group('type')
#             entry_dict['_id'] = re.search(type_key_rgx, entry_string).group('key')
#             entry_dict['properties'] = dict(re.findall(properties_rgx, entry_string))
#         except:
#             return None
#         return entry_dict
#
#     @staticmethod
def dict2bib(entry_dict):
    """
      Formats a dict into a bib entry to write on a bob file
      :param entry_dict: dict, entry dictionary
      :return: entry_string: str, entry string
      """
    properties_string = ',\n\t'.join([f"{prp}={{{val}}}" for prp, val in entry_dict['properties'].items()])
    entry_string = f"""@{entry_dict['type']}{{{entry_dict['_id']},
{properties_string}
}}"""
    return entry_string


#
#
# def read_bib_file(path):
#     with open(path, 'r') as f:
#         content = f.read()
#     entry_strings = [
#         BibEntry(ent.strip()).entry_dict for ent in content.split('\n\n') if BibEntry(ent.strip()).entry_dict
#     ]
#     return entry_strings

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
