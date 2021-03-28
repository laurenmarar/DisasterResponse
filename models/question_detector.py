from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize

class QuestionDetector(BaseEstimator, TransformerMixin):

    def id_question(self, text):
        """Input text and identify if it contains a question word (who, what, where, when, why) and return boolean flag"""
        sentence_list = sent_tokenize(text)
        
        for sentence in sentence_list:            
            
            try:
                
                pos_tags = pos_tag(tokenize(sentence))
                
                first_word, first_tag = pos_tags[0]
                # return true if the first word is which, who, what, where, or when
                if first_tag in ['WDT', 'WP', 'WRB']:
                    return 1
            except:
                return 0
            
            return 0

    def fit(self, x, y=None):
        return self

    def transform(self, X):
        X_tagged = pd.Series(X).apply(self.id_question)

        return pd.DataFrame(X_tagged).fillna(0)