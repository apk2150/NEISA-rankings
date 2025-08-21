import rank_calculator
import csv

schoolslink = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ2O1cDbUtwrHTIfpCXKQ8Ue7JsJE6PJo-DoSMPt3HdKxV-6_gSP27hSRhN20pT2Vbe48j0Ec1yqLL6/pub?output=csv"
coedRegattaLink = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQm-fcet5nzTCvBvHAL_-kz_qrly5SwPJ2nsZYWX_sMgn63Ji8jHffjRDmX1Ha0Qv-wy_pLz5O7aEQP/pub?output=csv"
womensRegattaLink = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQm-fcet5nzTCvBvHAL_-kz_qrly5SwPJ2nsZYWX_sMgn63Ji8jHffjRDmX1Ha0Qv-wy_pLz5O7aEQP/pub?output=csv"

coed_rankings_output_file = "rankings.csv"
coed_component_scores_file = "component_scores.csv"

womens_rankings_output_file = "womensrankings.csv"
womens_component_scores_file = "womens_component_scores.csv"

################## COED ######################
# ranks, school_objects = rank_calculator.calculate_ranks(coedRegattaLink, schoolslink)

# f = open(coed_rankings_output_file, "w")
# f.truncate()
# f.close()

# with open(coed_rankings_output_file, 'w') as result:
#     writer = csv.writer(result, delimiter=",")
#     writer.writerow(('School', 'Score'))
#     for row in ranks:
#         row = (row[0], str(row[1]))
#         writer.writerow(row)


# f = open(coed_component_scores_file, "w")
# f.truncate()
# f.close()

# with open(coed_component_scores_file, 'w') as result:
#     writer = csv.writer(result, delimiter=",")
#     writer.writerow(('School', 'Counted Scores Regular Regattas', 'Championship Score'))
#     for school in school_objects:
#         obje = school_objects[school]
#         row = (obje.name, obje.counted_points, obje.s_regatta_score)
#         writer.writerow(row)


# Example usage after calculate_ranks:
ranks, school_objects = rank_calculator.calculate_ranks(coedRegattaLink, schoolslink)
rank_calculator.export_team_regatta_points(school_objects, coedRegattaLink, "team_regatta_points.csv")
print("results written to team_regatta_points.csv")
######################################################


# ################### WOMENS ###########################
# ranks, school_objects = rank_calculator.calculate_ranks(womensRegattaLink, schoolslink)

# f = open(womens_rankings_output_file, "w")
# f.truncate()
# f.close()

# with open(womens_rankings_output_file, 'w') as result:
#     writer = csv.writer(result, delimiter=",")
#     writer.writerow(('School', 'Score'))
#     for row in ranks:
#         row = (row[0], str(row[1]))
#         writer.writerow(row)


# f = open(womens_component_scores_file, "w")
# f.truncate()
# f.close()

# with open(womens_component_scores_file, 'w') as result:
#     writer = csv.writer(result, delimiter=",")
#     writer.writerow(('School', 'Counted Scores Regular Regattas', 'Championship Score'))
#     for school in school_objects:
#         obje = school_objects[school]
#         row = (obje.name, obje.counted_points, obje.s_regatta_score)
#         writer.writerow(row)
