import sys
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """Input filepaths for messages and category labels and return merged dataframe"""
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = messages.merge(categories, left_on='id', right_on='id')
  
    return df

def clean_data(df):
    """Input dataframe and return cleaned dataframe"""
    categories = df['categories'].str.split(';', expand=True)
    category_colnames = list(categories.iloc[0].str.split('-').str[0])
    categories.columns = category_colnames
    
    for column in categories:
        try:
            categories[column] = categories[column].str.split('-',expand=True)[1]
        except:
            continue
        categories[column] = pd.to_numeric(categories[column])
    
    df = df.drop(columns=['categories'])
    
    df = pd.concat([df, categories], axis=1)
    
    df = df.drop_duplicates()
    
    # Impute nulls
    df.iloc[:, 4:] = df.iloc[:, 4:].fillna(0)
    # Set outcome columns to binary
    df.related.replace(2, 1, inplace=True)
    return df

def save_data(df, database_filepath):
    """Input dataframe and SQL database name to save"""
    engine = create_engine('sqlite:///'+database_filepath)

    df.to_sql('DisasterResponse', engine, index=False, if_exists='replace')  

def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')

if __name__ == '__main__':
    main()