import sys
sys.path.append("../models")
from question_detector import QuestionDetector

import json
import plotly
import pandas as pd

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from flask import Flask
from flask import render_template, request, jsonify
import plotly
from plotly.graph_objs import Bar
import joblib
from sqlalchemy import create_engine


app = Flask(__name__)

def tokenize(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()

    clean_tokens = []
    for tok in tokens:
        clean_tok = lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)

    return clean_tokens

# load data
engine = create_engine('sqlite:///../data/DisasterResponse.db')
df = pd.read_sql_table('DisasterResponse', engine)

# load model
model = joblib.load("../models/classifier.pkl")


# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():
    
    # extract data needed for visuals
    # create a flag to identify cases that require urgent action
    df_urgent = df.copy()
    df_urgent['urgent'] = df['child_alone']+df['search_and_rescue']+df['fire']+df['earthquake']+df['floods']
    urgent_cases = df_urgent[['id', 'child_alone','search_and_rescue','fire','earthquake','floods','urgent']].query('urgent > 0')
    urgent_cases = urgent_cases.melt(id_vars=['id'], var_name='category', value_vars=['child_alone','search_and_rescue','fire','earthquake','floods'])

    # summarize number of urgent cases to get an idea of human resources needed in immediate future
    urgent_cases = urgent_cases.groupby('category').sum()['value']
    case_cat = list(urgent_cases.index)
    
    # create visuals
    graphs = [
        {
            'data': [
                Bar(
                    x=case_cat,
                    y=urgent_cases, 
                    marker_color='#ffa15a'
                )
            ],

            'layout': {
                'title': 'Cases needing immediate intervention',
                'yaxis': {
                    'title': "# cases"
                },
                'xaxis': {
                    'title': "Category"
                }
            }
        }
    ]
    
    # encode plotly graphs in JSON
    ids = ["graph-{}".format(i) for i, _ in enumerate(graphs)]
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    
    # render web page with plotly graphs
    return render_template('master.html', ids=ids, graphJSON=graphJSON)


# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '') 

    # use model to predict classification for query
    classification_labels = model.predict([query])[0]
    classification_results = dict(zip(df.columns[4:], classification_labels))

    # This will render the go.html Please see that file. 
    return render_template(
        'go.html',
        query=query,
        classification_result=classification_results
    )


def main():
    app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()