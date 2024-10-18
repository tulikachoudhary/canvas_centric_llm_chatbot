import json
from bs4 import BeautifulSoup
import os

json_file_path = os.path.join(os.path.dirname(__file__), '../data/raw/raw.json')

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

html_content = data.get("html_content", "")

