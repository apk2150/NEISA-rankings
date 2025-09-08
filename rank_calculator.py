import pandas as pd
import numpy as np
import google_sheets
import techscore_reader
import csv

#socres for 15-18 teams
SA_18=[108.00,105.00, 102.00, 99.00, 96.00, 93.00, 90.00, 87.00, 84.00, 81.00, 78.00, 75.00, 72.00, 69.00, 66.00, 63.00, 60.00, 57.00]
A_18=[90.00,85.00,80.00,75.00,70.00,65.00,60.00,55.00,50.00,45.00,40.00,35.00,30.00,25.00,20.00,15.00,10.00,5.00]
AM_18=[54.00,51.00,48.00,45.00,42.00,39.00,36.00,33.00,30.00,27.00,24.00,21.00,18.00,15.00,12.00,9.00,6.00,3.00]
B_18=[36.00,34.00,32.00,30.00,28.00,26.00,24.00,22.00,20.00,18.00,16.00,14.00,12.00,10.00,8.00,6.00,4.00,2.00]
C_18 =[18.00,17.00,16.00,15.00,14.00,13.00,12.00,11.00,10.00,9.00,8.00,7.00,6.00,5.00,4.00,3.00,2.00,1.00]

POINTS_15_18={"SA":SA_18, "A": A_18, "AM":AM_18, "B": B_18, "C":C_18}
#scores for 11-14 teams
A_14=[84.00,78.00,72.00,66.00,60.00,54.00,48.00,42.00,36.00,30.00,24.00,18.00,12.00,6.00]
AM_14=[49.00,45.50,42.00,38.50,35.00,31.50,28.00,24.50,21.00,17.50,14.00,10.50,7.00,3.50]
B_14=[35.00,32.50,30.00,27.50,25.00,22.50,20.00,17.50,15.00,12.50,10.00,7.50,5.00,2.50]
C_14=[17.50,16.25,15.00,13.75,12.50,11.25,10.00,8.75,7.50,6.25,5.00,3.75,2.50,1.25]
POINTS_11_14 = {"A": A_14, "AM": AM_14, "B": B_14, "C": C_14}

#scores for 7-10 teams
B_10 = [30.00,27.00,24.00,21.00,18.00,15.00,12.00,9.00,6.00,3.00]
C_10 = [15.00,13.50,12.00,10.50,9.00,7.50,6.00,4.50,3.00,1.50]
POINTS_7_10 = {"B": B_10, "C": C_10}
#note: do not get points for regattas with less than 7 teams


class School:
    def __init__(self, name):
        self.name = name
        self.points = []
        self.s_regatta_score = (0, None)
        self.counted_points = [] #if this is empty then all the points are counted

    def add_points(self,x,regatta_name):
        self.points.append((round(x, 2), regatta_name))
        self.points = sorted(self.points, key=lambda x: x[0], reverse=True)

    def get_points_total(self):
        if len(self.points) > 3:
            self.counted_points = [self.points[0], self.points[1], self.points[2], self.points[3]]
        else:
            self.counted_points = self.points

        return sum([pair[0] for pair in self.counted_points]) + self.s_regatta_score[0]

def calculate_rank(type, total_teams, score):
    #determine num of teams
    if total_teams >=15:
        points = POINTS_15_18[type]
    elif total_teams >= 11:
        points = POINTS_11_14[type]
    elif total_teams >= 7:
        points = POINTS_7_10[type]
    else:
        return 0
    #determine rank
    rankvalue= points[score]
    return rankvalue

def enter_scores(school_objects, data, type, total_teams, regatta_name):
    data = list(data)
    for scoreind in range(len(data)):
        team = data[scoreind]
        score = calculate_rank(type, total_teams, scoreind)
        if team in school_objects:
            school_objects[team].add_points(score, regatta_name)

# def enter_s_scores(school_objects, data, type, total_teams, regatta_name):
#     data = list(data)
#     if type == "SC_A":
#         type = "SC"
#     elif type == "SC_B":
#         type = "B"
#         if (total_teams < 18):
#             total_teams = 18
#     elif type == "WSC_A": #TODO: why was it WSC_A in the first place? why not just WSC?
#         type = "WSC"
#     else:
#         print("enter_s_scores doesnt understand the regatta type")

#     for scoreind in range(len(data)):
#         team = data[scoreind]
#         score = calculate_rank(type, total_teams, scoreind+1)
#         if team in school_objects:
#             if school_objects[team].s_regatta_score[0] == 0:
#                 school_objects[team].s_regatta_score = (round(score, 2), regatta_name)
#             else:
#                 print("hmm you tried to add two s scores to the same school object")

def get_rank(school_objects):
    tuplist = []
    for school_name in school_objects:
        school = school_objects[school_name]
        tuplist.append((school.name, school.get_points_total()))
    tuplist.sort(key=lambda x: x[1], reverse = True)
    return tuplist

def add_school_objects(schools_link):
    schools = google_sheets.read_sheet(schools_link).Schools
    school_objects = {}
    for school in schools:
        school_objects[school] = School(school)
    return school_objects

def calculate_ranks(regatta_link, schools_link):
    df = google_sheets.read_sheet(regatta_link)
    school_objects = add_school_objects(schools_link)
    for index, regatta in df.iterrows():
        regatta_type = regatta.Type
        regatta_finishes, total_teams = techscore_reader.get_regatta_results_and_num_teams(regatta.Link, regatta_type)
        lateDrops = regatta.LateDrops
        if not pd.isnull(lateDrops):
            total_teams += lateDrops
        regatta_name = (regatta.Link.split("/"))[-2]
        print("\n\nregatta name", regatta_name)
        print("regatta type", regatta_type)
        # if regatta_type in ("SC_A", "WSC_A", "SC_B"):
        #     enter_s_scores(school_objects, regatta_finishes, regatta_type, total_teams, regatta_name)
        #     continue

        # if (regatta_type == "A") and (total_teams < 18):
        #     total_teams = 18

        # if (regatta_type == "B") and (total_teams < 16):
        #     total_teams = 16

        # if regatta_type == "special_A": #sidesteps the total team minimum
        #     regatta_type = "A"

        #TODO: where is the WSC one the line below coming from?
        regattaTypes = ["A", "SA", "AM", "B", "C"]
        if regatta_type not in regattaTypes:
            print("Regatta type " + regatta_type + " is incorrect for " + regatta.Link)
            print("Possible regatta type options for this regatta are: " + str(regattaTypes))
            continue

        enter_scores(school_objects, regatta_finishes, regatta_type, total_teams, regatta_name)

    return (get_rank(school_objects), school_objects)


def calculate_score_table(total_teams_maximum, total_teams_minimum, regatta_type):
    total_teams = total_teams_maximum
    while total_teams >= total_teams_minimum:
        print("for teams:", total_teams)
        for i in range(1, total_teams+1):
            print(calculate_rank(regatta_type, total_teams, i))
        total_teams = total_teams - 1

def export_team_regatta_points_and_placements(school_objects, regatta_link, points_csv_path, placements_csv_path):
    # Read regatta names in order from regatta_link
    df = google_sheets.read_sheet(regatta_link)
    regatta_names = []
    for _, regatta in df.iterrows():
        regatta_name = (regatta.Link.split("/"))[-2]
        regatta_names.append(regatta_name)

    # Build a mapping: regatta_name -> list of (team, points)
    regatta_results = {regatta: [] for regatta in regatta_names}
    for school in school_objects.values():
        for pts, regatta in school.points:
            regatta_results[regatta].append((school.name, pts))
        if school.s_regatta_score[0] != 0 and school.s_regatta_score[1]:
            regatta_results[school.s_regatta_score[1]].append((school.name, school.s_regatta_score[0]))

    # For each regatta, sort teams by points (descending), assign placement
    regatta_placements = {regatta: {} for regatta in regatta_names}
    regatta_points = {regatta: {} for regatta in regatta_names}
    for regatta in regatta_names:
        teams_points = regatta_results[regatta]
        # Sort by points descending, then assign placement (1-based)
        sorted_teams = sorted(teams_points, key=lambda x: x[1], reverse=True)
        for place, (team, pts) in enumerate(sorted_teams, start=1):
            regatta_placements[regatta][team] = place
            regatta_points[regatta][team] = pts

    # Build rows for points
    points_rows = []
    for school in school_objects.values():
        row = [school.name]
        for regatta in regatta_names:
            pts = regatta_points[regatta].get(school.name, "")
            row.append(pts)
        points_rows.append(row)

    # Build rows for placements
    placements_rows = []
    for school in school_objects.values():
        row = [school.name]
        for regatta in regatta_names:
            placement = regatta_placements[regatta].get(school.name, "")
            row.append(placement)
        placements_rows.append(row)

    # Write points CSV
    with open(points_csv_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Team"] + regatta_names)
        writer.writerows(points_rows)

    # Write placements CSV
    with open(placements_csv_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Team"] + regatta_names)
        writer.writerows(placements_rows)