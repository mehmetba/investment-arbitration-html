import fitz
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np


def format_text(row):
    if row['Font'] == '8.0pt':
        return f'<sup class="footnote-ref" id="footnote-ref-id-{row["Text"]}">{row["Text"]}</sup>'
    else:
        return row['Text']


def extract_headings_v11(df):
    current_heading = ''
    start_index = -1
    initial_parent_tag = None
    df['is_heading_part'] = False
    for i in range(2, len(df)):
        if df.iloc[i-2]['left'] == '72.0pt' and df.iloc[i-1]['left'] == '72.0pt' and df.iloc[i]['left'] == '108.0pt' and (df.iloc[i]['Parent Tag'] == 'b' or df.iloc[i]['Parent Tag'] == 'i'):
            start_index = i - 2
            initial_parent_tag = df.iloc[start_index]['Parent Tag']
            current_heading = str(df.iloc[start_index]['Text']).strip()
            df.at[start_index, 'is_heading_part'] = True
        if start_index != -1 and df.iloc[i]['Parent Tag'] == initial_parent_tag:
            current_heading += ' ' + str(df.iloc[i]['Text']).strip()
            df.at[i, 'is_heading_part'] = True
        if start_index != -1 and df.iloc[i]['Parent Tag'] != initial_parent_tag:
            df.at[start_index, 'heading'] = current_heading.strip()
            df.at[start_index, 'is_heading_part'] = False # Here is the modification: we set 'is_heading_part' to False for the heading row
            start_index = -1
            initial_parent_tag = None
    return df






#open output csv to df
df = pd.read_csv("/home/ubuntu/pdf_to_html/output.csv")

df['Text'] = df.apply(format_text, axis=1)


# Assuming your DataFrame is named 'df'
distinct_values = df['Parent Tag'].unique()

# Print the distinct values
print(distinct_values)


df = extract_headings_v11(df)

df = df.dropna(subset=['Text'])

# Step 1: Copy the 'heading' column to the 'Text' column for the heading rows
df.loc[df['heading'].notnull(), 'Text'] = df.loc[df['heading'].notnull(), 'heading']

# Step 2: Drop the rows that are part of the headings
df = df.drop(df[df['is_heading_part']].index)


print(df)

df.to_csv("/home/ubuntu/pdf_to_html/9REN.csv", index=False, encoding='utf-8-sig')