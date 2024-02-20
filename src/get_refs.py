from utils import *
import json
import pymongo
from pymongo.errors import DuplicateKeyError
import yaml
import logging
import os

with open('/Users/shikunova/atambibki/config.yaml') as cnf:
    config = yaml.safe_load(cnf)

logging.basicConfig(filename=config['log_path'],
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

if __name__ == "__main__":
    logging.info('started connecting to the DB...')
    client = pymongo.MongoClient('localhost', 27017)
    try:
        client.admin.command('ping')
        logging.info("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        logging.info(e)
    db = client["atambibki"]
    refs = db["refs"]

    with open(config['biber_output_path'], 'r') as f:
        refs_to_find = parse_biber_errors(f.read())
    logging.info('looking for ' + ', '.join(refs_to_find))
    found = []
    for key in refs_to_find:
        result = list(refs.find({'_id': key}))
        if result:
            found.append(result)

    logging.info(f'incredible. found {len(found)} entries out of {len(refs_to_find)}')
    logging.info(f'writing to {os.environ["PROJECT_PATH"]}')
    with open(os.environ["PROJECT_PATH"] + '/ref.bib', 'a') as f:
        for entry_dict in found:
            f.write(dict2bib(entry_dict[0]) + '\n\n')
    logging.info('finished building the ref file! yay!')
