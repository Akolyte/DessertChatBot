# DessertChatBot

Site to scrape:
https://www.allrecipes.com/recipes/79/desserts/

BeautifulSoup Documentation: 
https://www.crummy.com/software/BeautifulSoup/bs4/doc/

we could turn the recipes into a relational database
OR
we could use a document (JSON) database like MongoDB

recipe -> entity
1. How are we going to collect our data
2. What is our schema
3. How are we going to clean it
4. Can we automate
4(5). How do we automate it

Systems:
1. Data Pipeline
2. AWS Lex + Lambda Functions
3. Frontend Website

## Problem 1: Getting a list with every dessert recipe url at allrecipes.com

Issues:
1.
  Problem: Recipe categories are nested, and are also repeated at different levels of nesting.
  Solution: Retain a set of recipe categories, and exit early if the recipe category has already been covered. 

## Problem 2: Writing and Reading from MongoDB Collection

## Problem 3: Configuring AWS Lambda functions to communicate with AWS Lex Chatbot

### Problem 3a: Create intent to handle requests for specific recipes

### Problem 3b: Create intent so that when prompted, the chatbot will return 3 random recipes and let the user pick one

## Problem 4: Create frontend to host chatbot
