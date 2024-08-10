from bs4 import BeautifulSoup
import chardet
import re

with open('output.html', 'rb') as file:
    raw_data = file.read()

result = chardet.detect(raw_data)
encoding = result['encoding']
html_content = raw_data.decode(encoding)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the span containing the date text
date_span = soup.find_all('span', {'data-text': 'true'})

if date_span:
    # Extract the text from the span
    date_text = date_span[1].text
    date_text = date_text[-17:]
    # Extract the dates from the text
    last_date = date_text.split('-')[0]
    print(f"Extracted dates: {last_date}")

# Get DF
attacks_israel = {}
attacks_hesbolla = {}
data = html_content.split('<script>')[1]
attacks_data = data.split('"data":[[[')[2:]

attacks_data[0] = attacks_data[0].split(']]]')[0]
attacks_data[1] = attacks_data[1].split(']]]')[0]

for idx, dir in enumerate(attacks_data):
    attacks_data[idx] = attacks_data[idx].split('],[')
    locations = []
    descriptions = []
    with open(f'attacks_{idx}.txt', 'w', encoding='utf-8') as file:
        for attack in attacks_data[idx]:
            location = attack.split('"value":"')[1].split('"')[0]
            locations.append(location)
            description = attack.split('"value":')
            description = max(description, key=len).split('},{')[0].split('}')[0]
            descriptions.append(description)
            file.write(f'{location=}' + '\n' + f'{description=}' + '\n')

    if idx == 0:
        attacks_israel['locations'] = locations
        attacks_israel['descriptions'] = descriptions
    else:
        attacks_hesbolla['locations'] = locations
        attacks_hesbolla['descriptions'] = descriptions
