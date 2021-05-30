# ******************IMPORT PACKAGES******************
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px


# ******************IMPORT, READ CSV FILES AND CREATING/MERGING DATAFRAMES******************
#import covid data for world
deaths_cases = pd.read_csv('countries-aggregated.csv')

#check import
print(deaths_cases.info())

# check for missing values
deaths_cases.isnull().sum()

# convert date from an object to datetime format
deaths_cases['date'] = pd.to_datetime(deaths_cases['Date'], format='%Y-%m-%d')

# countries listed
print('The Countries in the dataframe deaths_cases are\n')
print(deaths_cases.Country.unique())

# Make EU/EEA list include UK
EU_EEA_UK_list = ['Latvia', 'Bulgaria', 'Lithuania', 'Croatia', 'Czechia', 'Poland', 'Romania', 'Slovakia', 'Slovenia',
                  'Hungary', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Estonia', 'Austria', 'Belgium', 'Luxembourg',
                  'Netherlands', 'France', 'Germany', 'Ireland', 'Iceland', 'Norway', 'United Kingdom', 'Italy',
                  'Cyprus', 'Malta', 'Portugal', 'Greece', 'Spain']

print(EU_EEA_UK_list[0])
print(EU_EEA_UK_list[2])
print(len(EU_EEA_UK_list))

# create EU/EEA/UK dataframe and print to view
EU_cases_deaths = deaths_cases[deaths_cases['Country'].isin(EU_EEA_UK_list)]
print(EU_cases_deaths.info())

# check for missing values
EU_cases_deaths.isnull().sum()

# delete duplicate keep most recent unique record by country - accumulative death/cases number
df_EU_UK = EU_cases_deaths.drop_duplicates('Country', keep='last')

# Check df
print(df_EU_UK.head(5))

# import population data
POP = pd.read_csv('population_by_country_2020.csv')

# Create EU/EEA/UK dataframe
EUPOP = POP[POP['Country (or dependency)'].isin(EU_EEA_UK_list)]

# Check df
print(EUPOP.head(5))

# remove missing data - i.e non eu/eea uk countries
EUPOP.isnull().sum()

# merge EUPOP and EU/UK dataframe
EU_UK_merged = pd.merge(df_EU_UK, EUPOP, how='right', left_on='Country', right_on='Country (or dependency)')

# Check df
print(EU_UK_merged.info())

# Select columns for analysis and calculation of cases/death per 100,000
EU_UK = pd.DataFrame(EU_UK_merged, columns=['Country', 'Confirmed', 'Deaths', 'Population (2020)'])

# Calculate confirmed cases rate per 100,000 population- create new column
EU_UK['Confirmed cases per 100,000'] = (EU_UK['Confirmed'] / EU_UK['Population (2020)']) * 100000

# Calculate deaths rate per 100,000 population- create new column
EU_UK['Deaths from Covid-19 per 100,000'] = (EU_UK['Deaths'] / EU_UK['Population (2020)']) * 100000

# Check df and calculations
print(EU_UK.head(5))
print(EU_UK.info())

# order by countries with highest number of cases in EU/UK
df_casestot = EU_UK.groupby('Country').max().sort_values('Confirmed cases per 100,000', ascending=False)[0:]

# Check df
print(df_casestot.head(10))

# order by countries with highest number of Deaths in EU/UK
df_deathstot = EU_UK.groupby('Country').max().sort_values('Deaths from Covid-19 per 100,000', ascending=False)[0:]

# Check df
print(df_deathstot.head(10))

# Looking at df to select high, middle, lowest country for cases/deaths
for row in df_casestot.head(29).itertuples():
    print(row)

df_topmidbotcases = (df_casestot.iloc[0], df_casestot.iloc[14], df_casestot.iloc[28])
print(df_topmidbotcases)

for row in df_deathstot.head(29).itertuples():
    print(row)

df_topmidbotdeaths = (df_deathstot.iloc[0], df_deathstot.iloc[14], df_deathstot.iloc[28])
print(df_topmidbotdeaths)

# import government stringency data
stringency = pd.read_csv('covid-stringency-index.csv')

#check df
print(stringency.head(2))
print(stringency.shape)
print(stringency.info())

# convert date from an object to datetime format
stringency['date'] = pd.to_datetime(stringency['Day'], format='%Y-%m-%d')

# create EU dataframe and print to view
EU_EEA_UK_stringe = stringency[stringency['Entity'].isin(EU_EEA_UK_list)]

# check for missing values
EU_EEA_UK_stringe.isnull().sum()

#check df
print(EU_EEA_UK_stringe.head)
print(EU_EEA_UK_stringe.info())

# iN ORDER TO SEE MOST - LEAST STRINGENT COUNTRY, GROUP BY COUNTRY AND GET THE MEAN VALUE OF THE STRINGENCY INDEX.
df_stringency = EU_EEA_UK_stringe.groupby("Entity")["stringency_index"].mean().sort_values(ascending=False).head(29)
print(df_stringency.head())

# merge the cummulative cases/deaths df with stringency dataframe
df_corr = pd.merge(EU_UK, df_stringency, how='right', left_on='Country', right_on='Entity')
print(df_corr.info())

# create df with desired columns only
df_corr = pd.DataFrame(df_corr, columns=['Country', 'Confirmed cases per 100,000', "Deaths from Covid-19 per 100,000",
                                         'stringency_index'])
# Check df
print(df_corr.info())


# ******************Visualisations******************
# create world map of cumulative deaths
deaths_cases = pd.read_csv('countries-aggregated.csv')
deaths_cases = deaths_cases.groupby('Country').max()

fig = px.choropleth(deaths_cases, locations=deaths_cases.index, locationmode='country names',
                    color='Deaths', color_continuous_scale="blugrn")
fig.update_layout(title="Total confirmed deaths due to COVID-19 in the world",
                  titlefont={'size': 20},
                  paper_bgcolor='white'
                  )
fig.show()

# create map with total confirmed cases in the world
fig = px.choropleth(deaths_cases, locations=deaths_cases.index, locationmode='country names',
                    color='Confirmed', color_continuous_scale="blugrn")
fig.update_layout(title="Total confirmed cases in the world",
                  titlefont={'size': 20},
                  paper_bgcolor='white'
                  )
fig.show()

# barplot of total confirmed cases in EU/EEA/UK per 100,000 population
df_casestot = df_casestot.groupby("Country")["Confirmed cases per 100,000"].mean().sort_values(ascending=False).head(29)
sns.set_style("darkgrid")
plt.figure(figsize=(10, 10))
ax = sns.barplot(df_casestot.values, df_casestot.index)
ax.set_xlabel("Confirmed cases per 100,000")
ax.set_ylabel("Country")
ax.set_title("Total confirmed COVID-19 cases per 100,000")
plt.show()

# barplot of total confirmed deaths in EU/EEA/UK per 100,000 population
df_deathstot = df_deathstot.groupby("Country")["Deaths from Covid-19 per 100,000"].mean().sort_values(ascending=False).head(29)
sns.set_style("darkgrid")
plt.figure(figsize=(10, 10))
ax = sns.barplot(df_deathstot.values, df_deathstot.index)
ax.set_xlabel("Confirmed cases per 100,000")
ax.set_ylabel("Country")
ax.set_title("Total Deaths from Covid-19 per 100,000")
plt.show()

# plot lineplot for strincency index over time per country
plt.figure(figsize=(20, 5))
ax = sns.lineplot(x="date", y="stringency_index", data=EU_EEA_UK_stringe, hue="Entity")
plt.title('Stringency Index over time for Countries in EU EEA and UK')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xticks(rotation=45)
plt.show()

# Mean stringency index per country, order from most to least
df_stringency = EU_EEA_UK_stringe.groupby("Entity")["stringency_index"].mean().sort_values(ascending=False).head(29)
sns.set_style("darkgrid")
plt.figure(figsize=(10, 10))
ax = sns.barplot(df_stringency.values, df_stringency.index)
ax.set_xlabel("Government policy Stringency Index ")
ax.set_ylabel("Country")
ax.set_title("Countries in EU/EEA and UK ranked in order of stringency of Government policies")

#import seaborn as sns
sns.set_theme(style="whitegrid")


# Plot relationship between number of deaths per 100,000 and stringency
sns.relplot(x="Deaths from Covid-19 per 100,000", y="stringency_index", hue="Country", alpha=1, palette="dark",
            height=6, data=df_corr)
plt.show()

# Plot relationship between number of deaths per 100,000 and stringency
sns.relplot(x='Confirmed cases per 100,000', y="stringency_index", hue="Country", alpha=1, palette="dark",
            height=6, data=df_corr)

plt.show()

