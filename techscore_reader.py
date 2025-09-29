import pandas
import termcolor
from termcolor import colored, cprint

def get_regatta_results_and_num_teams(regatta_link, regatta_type):
    results_table = ""
    try:
        results_table = pandas.read_html(regatta_link,attrs={"class": "results coordinate divisional"}, header=0, index_col=0)
    except:
        cprint(colored("REGATTA LINK IS BROKEN: " + regatta_link), 'red')
        return
    teams = list(results_table[0].Team)
    result = list(results_table[0].School)
    #truncate to 18 teams if more than 18, those placing higher than 18th don't score points
    teams = teams[:18]
    result = result[:18]
    finishes = []
    for ind in range(len(teams)):
        team = teams[ind]
        if(regatta_type == "special_A"):
            if (result[ind] not in finishes):
                finishes.append(result[ind])
        elif (any(i.isdigit() for i in team) and ("1" in team) or (not any(i.isdigit() for i in team))):
            finishes.append(result[ind])

    return (finishes, len(finishes))
