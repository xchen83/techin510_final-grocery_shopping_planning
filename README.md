# Introduction
For my final project, I aim to develop an application dedicated to addressing
the issue of global food waste within individual households. The United Nations
reports that 50% of all fruits and vegetables produced worldwide are wasted
annually. In Toronto, over half of the food waste in single-family households is
avoidable, including leftovers and untouched food. Motivated by these findings,
my project will focus on aiding individuals in reducing food waste through
enhanced planning and utilization of their purchased items.

# Technologies & Methodologies
The application will be designed to assist users in more effectively planning
their grocery shopping. Several techniques I learnt from the course will be applied on the following pags:
1. 🛒 Fresh Food on Walmart.com
    - Web Crawling from Walmart and Storing the Data into Postgres Database
    - To obtain the real time price and foods for users to plan grocery shopping
    - Using API to crawl the data
2. 📝 Grocery Planning List
    - Data Storage with into local SQLite database
    - Incorporating a grocery shopping list for users to keep track of the items
3. 📦 Track Fridge Inventory
    - Used streamlit to create a form to allow users keep track of fridge inventory and the food items expiration date
4. 🏦 Purchasing Insights
    - Data visualization using altair to provide purchasing insights for users to save money

# How to Run
## 1. Installing the following
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
## 2. Usage
    - streamlit run app.py

# Reflection
1. What you learned
    - During the coding process, I attempted to utilize the SQLite database I had established for the Grocery Planning List page on the Track Inventory page to enhance efficiency. However, I discovered that the SQLite database could not be shared across different pages, prompting me to create a new database for inventory management.
    
2. What questions/problems did you face?
    - Overall, the most difficult part was scraping information from the website of a major grocery company. There were significant limitations based on authorization. Consequently, I discovered a free API that allowed me to access data from Walmart.com.

    - Another challenge I encountered was attempting to incorporate the database I retrieved from the website into the shopping list app. However, because the search function from the database is not supported by the BaseModel, achieving this functionality became too difficult. As a result, I opted to allow users to manually input items instead.