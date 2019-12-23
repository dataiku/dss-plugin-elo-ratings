# Code for custom code recipe compute_Team_ELOs (imported from a Python recipe)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# -*- coding: utf-8 -*-
import dataiku
import numpy as np
import pandas as pd
from dataiku.customrecipe import *
from Elo_Classes import Match,Team

# Sub engine
def create_team(dictTeams,teamId):
    if teamId not in dictTeams:
        dictTeams[teamId] = 1000
    return dictTeams, Team(teamId,dictTeams[teamId])

def get_schema(matchId_col, match_datetime_col, homeTeamId_col, awayTeamId_col, homeTeam_goals_col, awayTeam_goals_col):
    sch = [{"name":matchId_col,"type":"int"}]
    sch+=[{"name":el,"type":"string"} for el in [match_datetime_col,
                                                       homeTeamId_col,awayTeamId_col, 
                                                       homeTeam_goals_col,awayTeam_goals_col,
                                                       str(homeTeamId_col)+"_rank",str(homeTeamId_col)+"_new_rank",
                                                       str(awayTeamId_col)+"_rank",str(awayTeamId_col)+"_new_rank",
                                                       "rank_change_"+str(homeTeamId_col),"ELOprob_"+str(homeTeamId_col),
                                                       "rank_change_"+str(awayTeamId_col),"ELOprob_"+str(awayTeamId_col)]]
    for col in input_df.columns.values.tolist():
            if col not in [column["name"] for column in sch]:
                sch+=[{"name":col,"type":"string"}]
    return sch

input_name = get_input_names_for_role('input_dataset')[0]

# The dataset objects themselves can then be created like this:
input_dataset = dataiku.Dataset(input_name)
input_df = input_dataset.get_dataframe()

#############################
# Recipe Parameters
#############################

recipe_config = get_recipe_config()

matchId_col = recipe_config.get('matchId', None)
if matchId_col == None:
    raise ValueError("You did not choose a matchId column.")
    
match_datetime_col = recipe_config.get('match_datetime', None)
if match_datetime_col == None:
    raise ValueError("You did not choose a match_datetime column.")
    
homeTeamId_col = recipe_config.get('homeTeamId', None)
if homeTeamId_col == None:
    raise ValueError("You did not choose a homeTeamId column.")
    
awayTeamId_col = recipe_config.get('awayTeamId', None)
if awayTeamId_col == None:
    raise ValueError("You did not choose a awayTeamId column.")
    
homeTeam_goals_col = recipe_config.get('homeTeam_goals', None)
if homeTeam_goals_col == None:
    raise ValueError("You did not choose a homeTeam_goals column.")
    
awayTeam_goals_col = recipe_config.get('awayTeam_goals', None)
if awayTeam_goals_col == None:
    raise ValueError("You did not choose a awayTeam_goals column.")

match_level_col = recipe_config.get('match_level', None)

input_df = input_df.sort_values(match_datetime_col)

output_name = get_output_names_for_role('output_dataset')[0]
output_dataset = dataiku.Dataset(output_name)
output_dataset.write_schema(get_schema(matchId_col, match_datetime_col, homeTeamId_col, awayTeamId_col, homeTeam_goals_col, awayTeam_goals_col))

match_dts = input_df[match_datetime_col].values
home_teams, away_teams = input_df[homeTeamId_col].values,input_df[awayTeamId_col].values
matches, goals_home, goals_away = input_df[matchId_col].values, input_df[homeTeam_goals_col].values, input_df[awayTeam_goals_col].values

if match_level_col == None:
    input_df['match_level'] = 30
    match_levels = input_df['match_level'].values
else:
    input_df[match_level_col] *= 30
    match_levels = input_df[match_level_col].values

avg_goalDiff = sum(abs(goals_home - goals_away))/len(input_df[matchId_col].values)

dictTeams = {}

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
with output_dataset.get_writer() as writer:
    for idx, matchId in enumerate(input_df[matchId_col].values):
        
        matchLevel, goalsHome, goalsAway, datetime = match_levels[idx], goals_home[idx], goals_away[idx], match_dts[idx]

        dictTeams,homeTeam = create_team(dictTeams,home_teams[idx])
        dictTeams,awayTeam = create_team(dictTeams,away_teams[idx])

        match = Match(matchId, matchLevel, homeTeam, awayTeam, goalsHome, goalsAway)

        match.update_team_rank(avg_goalDiff)

        rankingsDict = match.write_rankings()
    
        dicToWrite = {}
        dicToWrite[matchId_col] = rankingsDict["matchId"]
        dicToWrite[match_datetime_col] = pd.to_datetime(input_df[match_datetime_col]).values[idx]
        dicToWrite[homeTeamId_col] = rankingsDict["homeTeamId"]
        dicToWrite[awayTeamId_col] = rankingsDict["awayTeamId"]
        dicToWrite[homeTeam_goals_col] = rankingsDict["homeTeam_goals"]
        dicToWrite[awayTeam_goals_col] = rankingsDict["awayTeam_goals"]
        dicToWrite[str(homeTeamId_col)+"_rank"] = rankingsDict["homeTeam_rank"]
        dicToWrite[str(awayTeamId_col)+"_rank"] = rankingsDict["awayTeam_rank"]
        dicToWrite[str(homeTeamId_col)+"_new_rank"] = rankingsDict["homeTeam_new_rank"]
        dicToWrite[str(awayTeamId_col)+"_new_rank"] = rankingsDict["awayTeam_new_rank"]
        dicToWrite["rank_change_"+str(homeTeamId_col)] = rankingsDict["rank_change_home"]
        dicToWrite["rank_change_"+str(awayTeamId_col)] = rankingsDict["rank_change_away"]
        dicToWrite["ELOprob_"+str(homeTeamId_col)] = rankingsDict["ELOprob_home"]
        dicToWrite["ELOprob_"+str(awayTeamId_col)] = rankingsDict["ELOprob_away"]
        for col in input_df.columns.values.tolist():
            if col not in dicToWrite.keys():
                    dicToWrite[col] = str(input_df[col].values[idx]).decode('utf-8','replace')
        writer.write_row_dict(dicToWrite)

        dictTeams[home_teams[idx]] = match.homeTeam.new_rank
        dictTeams[away_teams[idx]] = match.awayTeam.new_rank