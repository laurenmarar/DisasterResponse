# Data Engineering to Improve Disaster Response

This project creates a tool to analyze authentic messages sent during disaster events, to help classify and prioritize those messages to inform action.

## Project Summary

Training on pre-labeled disaster messages provided by Figure Eight (https://appen.com/), this project classifies messages from disasters so they can be directed to the appropriate relief agencies.

It uses Natural Language Processing and a Machine Learning pipeline to clean the messages and categorizes them into topics such as water, shelter, electricity.

It then uses Plotly and Flask to build a website where users can enter new alert messages for processing.
![image](https://user-images.githubusercontent.com/47547501/112878994-925d1500-9096-11eb-900c-fc59cd0e7b69.png)

To help aid workers identify capacity needs for the immediate future, the website also highlights the total cases identified as belonging to one of the most urgent categories: child alone, search and rescue, fire, earthquake, or flood. 
![image](https://user-images.githubusercontent.com/47547501/112879044-a274f480-9096-11eb-83a4-4edc1e6a8257.png)

## Installation

After cloning the repository, install the requirements. The project uses Python 3.

`pip install -r requirements.txt`

## Navigation

 ┣ 📂app<br />
 ┃ ┣ 📂templates<br />
 ┃ ┃ ┣ 📜go.html<br />
 ┃ ┃ ┗ 📜master.html<br />
 ┃ ┗ 📜run.py<br />
 ┣ 📂data<br />
 ┃ ┣ 📜DisasterResponse.db<br />
 ┃ ┣ 📜disaster_categories.csv<br />
 ┃ ┣ 📜disaster_messages.csv<br />
 ┃ ┗ 📜process_data.py<br />
 ┣ 📂models<br />
 ┃ ┣ 📜question_detector.py<br />
 ┃ ┗ 📜train_classifier.py<br />
 ┣ 📜README.md<br />
 ┣ 📜requirements.txt<br />

## Process

### ETL Pipeline

- Loads pre-classified messages
- Cleans the data
- Stores the data in a SQLite database

### Machine Learning Pipeline

- Loads the data from the SQLite database
- Builds a pipeline for text processing and a machine learning classifier
- Trains and tunes the model using GridSearchCV
- Reports the results 
- Exports the final model into a pickle file

### Flask Web App

- Deploys the model to a Flask web app
- Visualizes the data with Plotly

You can run these scripts on your local machine and access the web app via http://localhost:3001




