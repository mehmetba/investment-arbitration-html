import fitz
import pandas as pd
from bs4 import BeautifulSoup
import re

# Function to extract specific properties from the 'style' attribute
def extract_css_properties(style, properties):
    if not style:
        return [None]*len(properties)
        
    style_dict = dict(item.split(":") for item in style.split(";") if item)
    return [style_dict.get(prop, None) for prop in properties]

# Read the HTML content from the file
with open("/home/ubuntu/pdf_to_html/output.txt", "r") as file:
    html = file.read()

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find all the <div> tags with id starting with 'page'
page_divs = soup.find_all(lambda tag: tag.name == 'div' and tag.get('id', '').startswith('page'))

# Extract the styles, font sizes, and texts from the <p> tags of each page
data = []
page_number = 1
css_properties = ['top', 'left', 'line-height']
for div in page_divs:
    p_tags = div.find_all('p')
    for p in p_tags:
        style = p.get('style')
        p_css_values = extract_css_properties(style, css_properties)

        spans = p.find_all('span', style=lambda s: s and 'font-size' in s)
        for span in spans:
            span_style = span.get('style') if span else None
            font_size = extract_css_properties(span_style, ['font-size'])[0] if span_style else None
            
            text = span.get_text(strip=True)
            
            parent_tag = span.parent.name if span.parent else None
            
            page_data = [f'Page_{page_number}'] + p_css_values + [font_size, parent_tag, text]
            data.append(page_data)
    
    page_number += 1

# Create a pandas DataFrame from the extracted data
columns=['Page'] + css_properties + ['Font', 'Parent Tag', 'Text']
df = pd.DataFrame(data, columns=columns)

# Print the DataFrame
print(df)

df.to_csv("/home/ubuntu/pdf_to_html/output.csv", index=False)
