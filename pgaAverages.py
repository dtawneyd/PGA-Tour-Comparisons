import pandas as pd
import matplotlib.pyplot as plt
import warnings
import ssl
warnings.simplefilter(action='ignore', category=FutureWarning)
ssl._create_default_https_context = ssl._create_unverified_context

# The following code takes a user input to chose year for stats.
year = input('Enter year of season: ')

scraper = pd.read_html(f'https://www.espn.com/golf/stats/player/_/season/{year}/table/general/sort/scoringAverage/dir/asc')

# for idx, table in enumerate(scraper):
#     print('*******************')
#     print(idx)
#     print(table)

# The table that I found on ESPN.com consisted of two separate tables. The following code sets the first table as
# list of players and the second table as the individual stats.
list_of_players = scraper[0]
list_of_stats = scraper[1]
list_of_players.reset_index(inplace=True)
list_of_stats.reset_index(inplace=True)

# The following code merges the two tables scraped from ESPN.com and cleans up unwanted columns for data comparison.
player_stats = pd.merge(list_of_players, list_of_stats)
player_stats.columns = ['index', 'rank', 'player', 'age', 'earnings', 'fedexcup', 'events', 'rounds', 'cuts', 'top10s',
                        'wins', 'Avg Score', 'drive_dist', 'Drive Acc', 'GIR', 'avg_putts', 'sand', 'birds']
player_stats.drop(['index', 'rank', 'age', 'events', 'rounds', 'sand', 'birds',
                   'fedexcup', 'cuts', 'top10s', 'wins','drive_dist'], axis=1, inplace=True)
player_stats = player_stats[['player', 'Avg Score', 'Drive Acc', 'GIR', 'earnings']]
print(f'List of players: \n {player_stats["player"]}')

# The following code takes a user input to select player for comparison and passed the lower method to player
# select to ensure code still runs if user enters name in unconventional way (all lower case/all upper case).
user_player = input('Pick a golfer: ').lower()
# The following code takes the player column and changes to all lowercase to match user input.
player_stats['player'] = [x.lower() for x in player_stats['player']]

# The following code finds the stats for the player selected by the user and then finds the overall tour average without
# the user selection. Instead of finding the tour average including the user player (50 vs 1), this finds the tour average
# excluding the user player (49 vs 1).
player_avg = player_stats.loc[player_stats['player'] == user_player].mean()
tour_avg = player_stats.loc[player_stats['player'] != user_player].mean()


# This section takes the two series (player_avg, tour_avg) and converts them into a dataframe in pandas and uses
# matplotlib to plot a bar graph comparing the stats.
player_comparison = pd.DataFrame({'Tour Avg': tour_avg, user_player.title(): player_avg})
player_graph = player_comparison.plot.bar(color = ['SkyBlue','IndianRed'], rot=0,
                 title=f'PGA Player Stat Comparison for {year} \n by Top 50 Lowest Average Score')
plt.show()



# This section can be used to compare your own stats (if you know them). Just uncomment the code below and input personal
# stats
# full_tour = player_stats.mean()
# my_stats = {'Avg Score': 90, 'Drive Acc': 32.5, 'GIR': 22.2}
# my_series = pd.Series(my_stats)
#
# # THIS WORKS FOR WHAT I WANT !!!!!!
# personal_comparison = pd.DataFrame({'Tour Avg': full_tour, 'My Avg': my_series})
# personal_graph = personal_comparison.plot.bar(color = ['SkyBlue','IndianRed'], rot=0,
#                  title=f'PGA Player Stat Comparison for {year} \n by Top 50 Lowest Average Score')
# plt.show()
