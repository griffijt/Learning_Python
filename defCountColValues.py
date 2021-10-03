"""
From: DataCamp Python Data Science Toolbox (Part 1)
Author: Hugo Bowne-Anderson
Source: https://campus.datacamp.com/courses/python-data-science-toolbox-part-1/default-arguments-variable-length-arguments-and-scope?ex=16
        https://campus.datacamp.com/courses/python-data-science-toolbox-part-1/lambda-functions-and-error-handling?ex=14

Modified by: Justin Griffith

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
    """Return a dictionary with counts of unique column values as the value for each key.
       Raises error is column name does not exist."""

    # Initialize an empty dictionary: cols_count
    cols_count = {}

    for col_name in args:
        
        # If input column name does not exist, raise error message
        if col_name not in df.columns:
            raise ValueError('The DataFrame does not have a ' + col_name + ' column.')

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
    return cols_count

# Call count_entries
result1 = count_entries(tweets_df, 'candidate', 'sentiment')
result2 = count_entries(tweets_df, 'candidate', 'sentiment', 'TEST')

# Print the result
print(result1)
print(result2)
