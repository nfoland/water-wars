import streamlit as st
import pandas as pd
import numpy as np
import csv
from io import StringIO
from collections import defaultdict


def find_teams(file_path, number_rounds): #Goes through CSV finds all teams and sets up the data structure
    team_data = defaultdict(dict)
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            team = row[2]
            if team not in team_data:
                team_data[team]["Overall_kills"] = 0
                team_data[team]["Overall_deaths"] = 0
                round_num = 0
                for rounds in range(number_rounds):
                    round_num += 1
                    team_data[team]["Round" + str(round_num) + "_kills"] = 0
                    team_data[team]["Round" + str(round_num) + "_deaths"] = 0

    return dict(team_data)

def count_overall_kills(file_path, team_data): #Goes through teams and validation to see how many kills each team has in CSV
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            team = row[2]
            validation = row[7]
            if team in team_data and validation == 'Validated':
                team_data[team]["Overall_kills"] += 1
    
    return team_data

def count_overall_deaths(file_path, team_data): #Goes through teams and validation to see how many deaths each team has in CSV
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            team = row[3]
            validation = row[7]
            if team in team_data and validation == 'Validated':
                team_data[team]["Overall_deaths"] += 1
    
    return team_data

def load_data(team_data): #Puts all data in a form for streamlit and prints the chart

    team_list = [] #Lists out teams
    kill_num_total = [] #Lists out kills per team total
    death_num_total = [] #Lists out deaths per team total

    for teams in team_data:
        team_list.append(teams)
        kill_num_total.append(team_data[teams]['Overall_kills'])
        death_num_total.append(team_data[teams]['Overall_deaths'])


    return pd.DataFrame(
        {
            "Teams": team_list,
            "Total Kills": kill_num_total,
            "Total Deaths": death_num_total,
        }
    )

def load_file(): #Main running function and prints file uploader

    write_title()

    uploaded_file = st.file_uploader("Insert Round Data Here", help='To download the responses from the submissions google form in a .csv format, open the google sheets, click File, and select Download > .csv. ')

    if uploaded_file is not None:
        # Save the uploaded file to disk
        file_path = 'round1_data.csv'
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getvalue())

        # Read the file as a DataFrame
        dataframe = pd.read_csv(file_path)

        number_rounds = 3
        team_data = find_teams(file_path, number_rounds)
        team_data = count_overall_kills(file_path, team_data)
        team_data = count_overall_deaths(file_path, team_data)
        st.write(load_data(team_data))

    else:
        file_path = None
    
    return file_path

def write_title():
    title = 'DZ AND ALPHA SIG WATER WARS'

    st.title(title)

file_path = load_file()