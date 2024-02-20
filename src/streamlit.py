import streamlit as st
import logging
import yaml
from bson.son import SON
import pymongo


with open('/Users/shikunova/atambibki/config.yaml') as cnf:
    config = yaml.safe_load(cnf)


logging.basicConfig(filename=config['log_path'],
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


st.markdown('<h1 style=\'text-align: center;\'>Who needs</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image('images/citavi.png', width=200)

with col2:
    st.image('images/zotero.png', width=200)

with col3:
    st.image('images/jabref.png', width=200)

st.markdown('<h1 style=\'text-align: center;\'>When you can have</h1>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.image('images/python.png', width=200)

with col2:
    st.markdown('')
    st.markdown('')
    st.markdown('<h2 style=\'text-align: center;\'>and</h2>', unsafe_allow_html=True)

with col3:
    st.image('images/mongodb.png', width=200)

# def query_db(filter):
client = pymongo.MongoClient('localhost', 27017)
try:
    client.admin.command('ping')
    logging.info("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    logging.info(e)
db = client["atambibki"]
refs = db["refs"]

pipeline = [
    {"$unwind": "$properties.year"},
    {"$group": {"_id": "$properties.year", "count": {"$sum": 1}}},
    {"$sort": SON([("_id", -1)])},
]

st.markdown('**Entries by year**')

year_data = [dict(zip(['year', 'count'], list(ele.values()))) for ele in refs.aggregate(pipeline) if ele['_id'].isdigit()]
st.area_chart(year_data, x='year', y='count', color='#4B5320')

pipeline = [
    {"$unwind": "$type"},
    {"$group": {"_id": "$type", "count": {"$sum": 1}}},
    {"$sort": SON([("count", -1)])},
]

st.markdown('**Entries by type**')

type_data = [dict(zip(['type', 'count'], list(ele.values()))) for ele in refs.aggregate(pipeline)]
st.bar_chart(type_data, x='type', y='count', color='#E52B50')

try:
    while search := st.text_input(
        'Want to find an entry?',
        key='entry_search'
    ):
        result = list(refs.find({'_id': search}))
        print(result)

        st.code(list(result)[0]['string'])
except:
    pass