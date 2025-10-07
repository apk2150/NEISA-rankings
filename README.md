# NEISA-rankings

## Set Up:  
Create 3 google sheets, following this structure:  

1. A sheet with all the schools in NEISA with the header "Schools" at the top.  
Follow this model: https://docs.google.com/spreadsheets/d/e/2PACX-1vQ2O1cDbUtwrHTIfpCXKQ8Ue7JsJE6PJo-DoSMPt3HdKxV-6_gSP27hSRhN20pT2Vbe48j0Ec1yqLL6/pub?output=csv

2. A sheet with each regatta and the type of that regatta for womens and coed. The type is denoted using the same structure we have used in the past. Follow this model exactly: https://docs.google.com/spreadsheets/d/e/2PACX-1vQm-fcet5nzTCvBvHAL_-kz_qrly5SwPJ2nsZYWX_sMgn63Ji8jHffjRDmX1Ha0Qv-wy_pLz5O7aEQP/pub?gid=0&single=true&output=csv

The table will be formated as follows: 
| Type | Link | LateDrops| Regatta_Name| 
|---|---|---|---|
| _type of regatta (SA, A, AM, B, C)_ | _link to tech score for that regatta (https://scores.collegesailing.org/season/regatta-name/)_| _number of late drops (integer, blank if no late drops)_ | _name of regatta_| 
| _example_ C	| https://scores.collegesailing.org/f25/charles-invite/ |	2 |	Charles Invite|


Note: The google sheets you should use is the link you get when going to File > Publish to Web. Change the Web Page setting to CSV using the dropdown. You should get a link from doing this.

In the Runner.py file, paste in the three links  (schools, womens links, and coed links). Put each of these between quotes (like the way it is now). For the way it is currently set up, the results will be exported to the `results` folder and the results files will be `results/coed_team_regatta_points.csv` `results/women_team_regatta_points.csv`. To check that the placements are generated correctly, check the `results/validate` folder
 When everything is set, run the Runner.py script (`python3 Runner.py` from the `neisa` directory).

## To Run the Python File:   
NOTE: Capitals matter in the following commands.

0. Make sure you have updated the links in the google sheets
1. Open Terminal  
2. Type `cd ~/Desktop/NEISA-rankings-master`   
3. Type `python3 Runner.py`  
4. Files will appear in Finder under Desktop/NEISA-rankings-master/results

## To Get Updated Code:
0. Save the links that are at the top of Runner.py somewhere (e.g. Notes)
1. Come to this page! Congrats.  
2. Hit the green *Code* button in the upper right corner of the page.
3. Hit *Download ZIP*
4. The zip should download. Double click the download to unzip it into a folder. (Finder should open). Drag that folder into your Desktop. If it asks you to replace the existing one, say yes.
5. **VERY IMPORTANT**: Make sure the folder is called **NEISA-rankings-master**. Make sure there's no (1) or (2) at the end.
6. Update the links at the top of Runner.py if they are not correct.
7.  See above to run it!

## Scoring Logic Explained
* Rankings are used to determine entries into the Schell/NEDT
* Regatta levels and which regattas count for performance ranking points are determined before the season starts
* For the Open rankings, a school’s top 4 scores are added together to determine their ranking, plus their points from the Schell/NEDT. For Women's, a school’s top 3 scores are added plus their points from Urn. 
* Schools score points for placement at regattas according to the level of the regatta and the number of teams at the regatta
    * If there are fewer than 7 unique teams then no points are allocated
* Duplicate teams are removed from results. Teams scoring behind a duplicate team will have their finish position moved up one spot. The exception to this is women/open singles (see below). 
    * Schools must designate what team is team 1 and what team is team 2. Only team 1 scores points, therefore if team 2 scores higher than team 1 they will receive points for team 1’s placement. 

* Non-NEISA teams are ignored, but do not cause NEISA teams to move up a place. 
    * For example if the results were 1st: Harvard 2nd Stanford 3rd Yale, Harvard would receive points for 1st place and Yale receives points for 3rd place.
* Late drops are added to the total number of teams attending the regatta
* Some regatta size ranges are blank (SA only lists 15-18, A only lists 11-14 and 15-18, etc)
    * If a regatta with one of those ratings is under-enrolled (e.g. only 10 unique teams sail the Harry Anderson), the regatta will be “sized up” (in this example, scored for 11-14 teams)
        * If this happens, the regatta may be evaluated at the end of the season to be re-rated
* For any regatta with more than 18 entries (Danmark, Singlehandeds), finishes outside the top 18 will award no points
#### Special case:
* NEISA Singlehanded Championships
    * The scoring table used is an A level in the range of corresponding fleet size, based on the number of competitors (not unique teams!)
    * Points are scored based on actual finish in the regatta, regardless of unique teams. Previously, a team could finish 30th place, but “12th unique team” and receive an outsized result compared to their dinghy results.
    * Teams will count their best competitor at the event (they do not need to designate a Team 1 beforehand)
    * Ex: 2022 Open Singles Champs
        * Brown scores 1st place
        * Yale scores 2nd place
        * CGA scores 5th (does not move up to 3rd!)
        * Dartmouth scores no points as their top sailor was outside the top 1
* Match Race New Englands 
    * scored as an A level with 11-14 teams, up to 8th place

#### Additional note:
* One of the primary goals for this revamped system was to reduce the need/desire for teams to “point chase” at lower level events, rather than sail the most competitive events available to them
* The conference felt that the best way to prepare for the Schell Trophy is to compete as often as possible in A level regattas, and wanted to enable teams to do so without giving up potential points at B and C level events
* To this end, scores for lower finishes at A levels were scaled up relative to top finishes at B and C levels

#### References: 

2024 Committee Report: https://neisa.collegesailing.org/documents/2024-NEISA-Performance-Rank-Report.pdf 

Old System: https://neisa.collegesailing.org/documents/NEISA_Performance_Ranking_System_Guide.pdf