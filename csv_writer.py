import json
import requests
from bs4 import BeautifulSoup

from datetime import timedelta, date

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import csv

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

start_date = date(2003, 10, 13)
end_date = date(2019, 11, 15)

csv_data = [['team_name', 'abbreviation', 'num_matches', 'pts', 'pos', 'prev_pts', 'prev_pos', 'date']]

for single_date in daterange(start_date, end_date):
    date = single_date.strftime("%Y-%m-%d")

    ranking_url = "cmsapi.pulselive.com/rugby/rankings/mru?date=%s&client=pulse" % date
    r  = requests.get("http://" + ranking_url)

    soup = BeautifulSoup(r.text)

    data = json.loads(soup.body.p.text)
    for entry in data['entries']:
        csv_data.append(
            [entry['team']['name'], entry['team']['abbreviation'], 
             entry['matches'], entry['pts'], entry['pos'], entry['previousPts'], 
             entry['previousPos'], date]
        )

with open('rankings.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)
csv_file.close()