import sys
from question_detector import QuestionDetector

import sqlite3
from sqlalchemy import create_engine

import pandas as pd
import numpy as np
import re
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

from sklearn.datasets import make_multilabel_classification
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.base import BaseEstimator, TransformerMixin

import pickle

random_state = 10

def load_data(database_filepath):
    """Input database filepath and return X, y, and category names"""
    
#     engine = create_engine(database_filepath)
    engine = create_engine('sqlite:///{}'.format(database_filepath))

#     conn = sqlite3.connect('DisasterResponse.db')
#     cur = conn.cursor()

#     df = pd.read_sql('SELECT * FROM DisasterResponse', con=conn)
    df = pd.read_sql_table("DisasterResponse",engine)

#     conn.commit()
#     conn.close()
    
    X = df['message'] #.values`
    y = df.iloc[:, 4:].fillna(0) #.values
    y.related.replace(2, 1, inplace=True)
    category_names = y.columns.values
    
    return X, y, category_names

def tokenize(text):
    """Input text column and return clean text"""
    
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    stop_words = stopwords.words("english")
    
    # remove URLs
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, " ")
        
    lemmatizer = WordNetLemmatizer()
    
    # normalize case and remove punctuation and extra spaces
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower().strip())
    
    # tokenize text
    tokens = word_tokenize(text)
    
    # lemmatize andremove stop words
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return tokens  

# class QuestionDetector(BaseEstimator, TransformerMixin):

#     def id_question(self, text):
#         """Input text and identify if it contains a question word (who, what, where, when, why) and return boolean flag"""
#         sentence_list = sent_tokenize(text)
        
#         for sentence in sentence_list:            
            
#             try:
                
#                 pos_tags = pos_tag(tokenize(sentence))
                
#                 first_word, first_tag = pos_tags[0]
#                 # return true if the first word is which, who, what, where, or when
#                 if first_tag in ['WDT', 'WP', 'WRB']:
#                     return 1
#             except:
#                 return 0
            
#             return 0

#     def fit(self, x, y=None):
#         return self

#     def transform(self, X):
#         X_tagged = pd.Series(X).apply(self.id_question)

#         return pd.DataFrame(X_tagged).fillna(0)
    
def build_model():
    """Use Pipeline to build MultiOutputClassifer with parameters selected based on GridSearch"""
    pipeline = Pipeline([
        ('features', FeatureUnion([
            
            ('text_pipeline', Pipeline([
                ('vect', CountVectorizer(tokenizer=tokenize)),
                ('tfidf', TfidfTransformer())
            ])),
            
            ('id_question', QuestionDetector())
        ])),
        
        ('clf', MultiOutputClassifier(RandomForestClassifier(random_state=random_state)))
    ])
    
    best_parameters = {
        # GridSearchCV chose 0.75 over 1 for vect__max_df
        'features__text_pipeline__vect__max_df': [0.75],
        # GridSearchCV chose 200 over 100 for n_estimators, but using 100 now for efficiency
        'clf__estimator__n_estimators': [100],
        # GridSearchCV chose 4 over 2 min_samples_split
        'clf__estimator__min_samples_split': [4]
    }
    
    cv = GridSearchCV(pipeline, param_grid = best_parameters, verbose=3)
    
    return cv

def evaluate_model(model, X_test, y_test, category_names):
    """Input model, X_test, y_test, and category names to return classification report for each category"""
    y_pred = model.predict(X_test)
    
    classif_report = classification_report(y_test, y_pred, target_names=category_names)
    
    return classif_report

def save_model(model, model_filepath):
    """Input model and model filepath to save model"""
    with open(model_filepath, 'wb') as f:
        pickle.dump(model, f)

def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, y, category_names = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()