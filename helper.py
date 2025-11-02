import numpy as np

def fetch_medal_tally(df,year,country):
  medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
  flag = 0
  if year == 'Overall' and country == 'Overall':
    temp_df = medal_df

  if year == 'Overall' and country != 'Overall':
    temp_df = medal_df[medal_df['region'] == country]
    flag = 1

  if year != 'Overall' and country == 'Overall':
    temp_df = medal_df[medal_df['Year'] == int(year)]

  if year != 'Overall' and country != 'Overall':
    temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

  if flag == 1:
      x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
  else:
      x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

  x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

  x['Gold'] = x['Gold'].astype(int)
  x['Silver'] = x['Silver'].astype(int)
  x['Bronze'] = x['Bronze'].astype(int)
  x['total'] = x['total'].astype(int)

  return x




######
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()

    medal_tally['total'] = medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    medal_tally['total'] = medal_tally['total'].astype(int)

    return medal_tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country

# //////////////////
#Participating Nations over time

def data_over_time(df, col):
    # """
    # Returns a DataFrame showing how many unique values of `col`
    # (like 'region', 'Event', 'Name') exist per Olympic year.
    # """
    data = (
        df.drop_duplicates(['Year', col])
          .groupby('Year')[col]
          .count()
          .reset_index()
          .rename(columns={'Year': 'Edition', col: f'No of {col.title()}s'})
    )
    return data



# Most Successful Athletes



import pandas as pd

def most_successful(df, sport):
    # Filter for only medal winners
    temp_df = df.dropna(subset=['Medal'])

    # If sport is selected, filter further
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals by Athlete, Region, and Sport
    x = (temp_df.groupby(['Name', 'region', 'Sport'])['Medal']
                .count()
                .reset_index()
                .sort_values('Medal', ascending=False)
                .head(15))

    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)


    new_df = temp_df[temp_df['region']==country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
   temp_df = df.dropna(subset=['Medal'])
   temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)


   new_df = temp_df[temp_df['region']==country]
   pt = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
   return pt

# - Most successful Athletes(Top 10)

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    # Count medals by Athlete, Region, and Sport
    x = (temp_df.groupby(['Name','Sport'])['Medal']
                .count()
                .reset_index()
                .sort_values('Medal', ascending=False)
                .head(10))

    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df


def men_vs_women(df):
   athlete_df = df.drop_duplicates(subset=['Name', 'region'])
   men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
   women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

   final = men.merge(women,on='Year',how='left')
   final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)

   final.fillna(0,inplace=True)

   return final
   