# Elo Ratings
Plugin to calculate [Elo ratings](https://en.wikipedia.org/wiki/Elo_rating_system) of entities given interaction history. 

The Elo rating system is a method for calculating the relative skill levels of players in zero-sum games such as chess. Elo ratings are numbers that represent the current form of an entity; the probability that one entity will win against another in an interaction can be [deduced from the difference between their Elo ratings](https://en.wikipedia.org/wiki/Elo_rating_system#Theory) (the entity with the greater rating being more likely to win.)

Given a dataset containing a history of interactions between entities (for example, rows containing the results of football matches between given teams), this plugin will order the interactions in chronological order, initialise the Elo rating of each entity before their first interaction to be 1000 and then update the ranking of each entity after each interaction according to the [Elo rating formula](https://en.wikipedia.org/wiki/Elo_rating_system#Theory). Given sufficient interaction history, these ratings should reach approximate equilibirum allowing predictions to be made about the outcome of any given interaction between entities.

This plugin contains one recipe to calculate Elo ratings associated with interactions.

## Plugin Information

Version: 0.0.1

Author: Adam Jelley

Released: 23/12/2019

Last Updated: 23/12/2019

License: Apache License Version 2.0

Source Code: [Github](https://github.com/dataiku/dss-plugin-elo-ratings)

Reporting Issues: [Github](https://github.com/dataiku/dss-plugin-elo-ratings/issues)

## How to Use

**Elo Rating Recipe**

This recipe can be applied to a dataset containing the interaction history between entities to give an output dataset with additional columns containing Elo rating features.

- *Required Columns:* 
Interaction ID, Interaction Datetime, Entity 1 ID, Entity 2 ID, Entity 1 Score, Entity 2 Score

- *Optional Columns:* 
Interaction Importance Level

- *Additional Ouput Columns:* 
Entity 1 Elo Rank (before interaction), Entity 1 New Elo Rank (after interaction), Entity 2 Elo Rank (before interaction), Entity 2 New Elo Rank (after interaction), Entity 1 Rank Change, Entity 2 Rank Change, Probability of Entity 1 Win (using Entity 1 Elo Rank), Probability of Entity 2 Win (using Entity 2 Elo Rank)

Note: Any other additional input columns will be preserved in the output.

## Install in DSS

To install plugin Elo Ratings in DSS go to Plugins -> Store and search for 'Elo Ratings'.