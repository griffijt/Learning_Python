"""
From: DataCamp Python Data Science Toolbox (Part 1), Writing your own functions
Author: Hugo Bowne-Anderson
Source: https://www.datacamp.com/courses/intermediate-python

Modified by: Justin Griffith

Modifications: 
Rather than counting the number of languages in the Twitter data, 
the function counts the candidates mentioned in the tweet data from Kaggle.

Data from: https://www.kaggle.com/crowdflower/first-gop-debate-twitter-sentiment
"""

# import libraries
import pandas as pd

# import data saved in working directory
tweets_df = pd.read_csv('Sentiment.csv')

# Define count_entries()
def count_entries(df, col_name):
    """Return a dictionary with counts of 
    Candidates as value for each key."""

    # Initialize an empty dictionary: candidate_count
    candidate_count = {}
    
    # Extract column from DataFrame: col
    col = df[col_name]
    
    # Iterate over candidate column in DataFrame
    for entry in col:

        # If the candidate is in candidate_count, add 1
        if entry in candidate_count.keys():
            candidate_count[entry] += 1
        # Else add the candidate to candidate_count, set the value to 1
        else:
            candidate_count[entry] = 1

    # Return the candidate_count dictionary
    return(candidate_count)

# Call count_entries(): result
result = count_entries(tweets_df, 'candidate')

# Print the result
print(result)
