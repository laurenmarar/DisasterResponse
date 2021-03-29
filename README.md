# Disaster Response Project

## Project Summary

This project processes tweets related to natural disasters, classifying them into various categories to target aid.

Using Natural Language Processing and a Machine Learning pipeline, this project cleans emergency messages and categorizes them into topics such as water, shelter, electricity.

It then uses plotly and Flask to build a website where users can enter new alert messages for processing.
![image](https://user-images.githubusercontent.com/47547501/112878994-925d1500-9096-11eb-900c-fc59cd0e7b69.png)

To help aid workers identify capacity needs, the website also highlights the total cases identified as one of these more urgent categories: child alone, search and rescue, fire, earthquake, or flood. 
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

## Outcomes

