import requests
from bs4 import BeautifulSoup
import pprint
import json
import argparse

f = open('objects2.txt')
data = json.load(f)

item = 'hello'

while item != 'stop':
    item = input("Search for")
    pprint.pprint(data[item])