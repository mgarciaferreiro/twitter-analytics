# twitter-analytics
Flask and Python app for Twitter Analytics 
Webapp using Python and Flask for Twitter Analytics, using both the Twitter REST API and the Streaming API to access different data. 
Packages:
•	Tweepy: to manage the authorization to access the API and use its functions to extract Twitter data
•	TextBlob: to do sentiment analysis on the text in the tweets collected (polarity and subjectivity)
•	Csv: to organize the data collected in a structured format (comma separated values)
•	Unidecode
•	Pandas: to read the data in the csv file
•	Matplotlib: to create graphs
•	WordCloud: to create a wordcloud with the most repeated terms in a specific search
•	Datetime: to get the current date and time so I could save files 
•	Json: to collect data in a json file and access it in an organized way
•	Counter: to count the number of times each term is repeated in a list

Features:
•	Accessing the Twitter API with a Twitter Developer account and extracting data
•	Creating a webpage using Flask, creating my own html templates, and running it on a browser
•	Searching a term on Twitter, displaying its polarity (how positively or negatively people feel about it), and displaying a wordcloud with the terms related to it
•	Finding trends in a specific area of the world and showing the intersection between the trends in that place and the trends in the whole world
•	Displaying a pie chart with the percentage of tweets in each language using the Streaming API, so you can see how these percentages change at different times of the day.

Note: you will need to get your own authorization tokens for the API in order to run the app https://developer.twitter.com/en/docs/basics/authentication/overview
