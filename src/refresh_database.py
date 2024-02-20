from utils import *
import json
import pymongo
from pymongo.errors import DuplicateKeyError
import yaml
import logging
from tqdm import tqdm

with open('/Users/shikunova/atambibki/config.yaml') as cnf:
    config = yaml.safe_load(cnf)


logging.basicConfig(filename=config['log_path'],
                    filemode='w',
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
    if config['database']['refresh']:  # flush database if necessary
        refs.delete_many({})

    walk_rootdir(**config['filenames'])
    with open(config['filenames']['out_path'], 'r') as f:
        content = json.load(f)
        logging.info(f'found {len(content)} bib documents')
        logging.info(f'starting processing...')
        # print(content)
        # assert False
    for bib_fn in tqdm(content):
        print(bib_fn)
        entry_dicts = read_bib_file(bib_fn)
        for entry in entry_dicts:
            try:
                refs.insert_one(entry)
            except DuplicateKeyError:  # skip duplicates
                pass
        print(f'inserted {len(entry_dicts)} entries from {bib_fn}')

    logging.info('finished refreshing the base! yay!')
