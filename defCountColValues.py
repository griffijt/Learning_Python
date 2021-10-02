"""
From: DataCamp Python Data Science Toolbox (Part 1), Writing your own functions
Author: Hugo Bowne-Anderson
Source: https://campus.datacamp.com/courses/python-data-science-toolbox-part-1/default-arguments-variable-length-arguments-and-scope?ex=16

Modified by: Justin

Modifications: 
Counts values contained in any given column names in the tweet data from https://www.kaggle.com/crowdflower/first-gop-debate-twitter-sentiment
Combines column name and value counts intos single dictionary.
"""

# import libraries
import pandas as pd

# import data
tweets_df = pd.read_csv('Sentiment.csv')

# Define count_entries()
def count_entries(df, *args):
    """Return a dictionary with counts of 
    column values for each key."""

    # Initialize an empty dictionary: cols_count
    cols_count = {}
    
    for col_name in args:

        # Extract column from DataFrame: col
        col = df[col_name]
        
        # Iterate over candidate column in DataFrame
        for entry in col:

            # If the candidate is in cols_count, add 1
            if entry in cols_count.keys():
                cols_count[entry] += 1
            # Else add the candidate to cols_count, set the value to 1
            else:
                cols_count[entry] = 1

    # Return the cols_count dictionary
    return(cols_count)

# Call count_entries
result1 = count_entries(tweets_df, 'candidate')
result2 = count_entries(tweets_df, 'candidate', 'sentiment')

# Print the result
print(result1)
print(result2)
