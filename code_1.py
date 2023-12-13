import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import os
import numpy as np
import mystats  

# Define file paths for the datasets
zip_files = {
    "co2_emission": "co2 emision.zip",
    "forest_area": "Forest area.zip",
    "population_growth": "Population_Growth(annual).zip",
    "renewable_energy_consumption": "Renewable Energy Comsuption.zip",
    "arable_land": "Arable Land (% of land area).zip"
}

# Function to unzip and load data
def load_data(file_path, skip_rows=4):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        extract_dir = f"extracted_{os.path.basename(file_path)}"
        zip_ref.extractall(extract_dir)
        main_file = [f for f in os.listdir(extract_dir) if f.startswith('API') and f.endswith('.csv')][0]
        return pd.read_csv(f"{extract_dir}/{main_file}", skiprows=skip_rows)

# Load datasets
co2_emission_df = load_data(zip_files["co2_emission"]).set_index('Country Name')
population_growth_df = load_data(zip_files["population_growth"]).set_index('Country Name')
renewable_energy_df = load_data(zip_files["renewable_energy_consumption"]).set_index('Country Name')

# Selecting countries and years
selected_countries = ['United States', 'China', 'India', 'Brazil', 'Germany', 'South Africa', 'Australia']
years = [str(year) for year in range(2000, 2011)]

# Extracting data for selected countries and years
co2_selected_df = co2_emission_df.loc[selected_countries, years]
population_growth_selected_df = population_growth_df.loc[selected_countries, years]
renewable_energy_selected_df = renewable_energy_df.loc[selected_countries, years]

# Example base populations for the year 2000 (hypothetical values)
base_population_2000 = {
    'United States': 300000000,
    'China': 1300000000,
    'India': 1000000000,
    'Brazil': 175000000,
    'Germany': 82000000,
    'South Africa': 45000000,
    'Australia': 19000000
}

# Calculate the population for each year from 2000 to 2010
population_data = {}
for country in selected_countries:
    base_pop = base_population_2000[country]
    population_data[country] = [base_pop]
    for year in years[1:]:
        growth_rate = population_growth_selected_df.loc[country, year] / 100
        new_pop = population_data[country][-1] * (1 + growth_rate)
        population_data[country].append(new_pop)

# Converting the dictionary to a DataFrame
population_df = pd.DataFrame.from_dict(population_data, orient='index', columns=years)
population_df = population_df.reset_index().rename(columns={'index': 'Country Name'})
print(population_df)

# Function to plot time series data
def plot_time_series(data, title, ylabel):
    plt.figure(figsize=(10, 6))
    for country in data.index:
        plt.plot(data.columns, data.loc[country], label=country)
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()

# Function to calculate average values for each country
def calculate_average(data):
    return data.mean(axis=1)

# Plotting time series for CO2 emissions
plot_time_series(co2_selected_df, 'CO2 Emissions (kt) from 2000 to 2010', 'CO2 Emissions (kt)')

# Comparative Analysis for 2010
co2_2010 = co2_selected_df.loc[:, '2010']
renewable_energy_2010 = renewable_energy_selected_df.loc[:, '2010']
population_growth_2010 = population_growth_selected_df.loc[:, '2010']

# Function to plot comparative bar charts
def plot_comparative_bars(data1, data2, title1, title2, ylabel1, ylabel2):
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))
    data1.plot(kind='bar', ax=ax[0], colormap='viridis')
    ax[0].set_title(title1)
    ax[0].set_ylabel(ylabel1)
    ax[0].tick_params(axis='x', rotation=45)
    data2.plot(kind='bar', ax=ax[1], colormap='plasma')
    ax[1].set_title(title2)
    ax[1].set_ylabel(ylabel2)
    ax[1].tick_params(axis='x', rotation=45)
    plt.tight_layout()
    plt.show()

plot_comparative_bars(co2_2010, renewable_energy_2010, 'CO2 Emissions in 2010 (kt)', 'Renewable Energy Consumption in 2010 (%)', 'CO2 Emissions (kt)', 'Renewable Energy (%)')

# Correlation Analysis for China across all years
china_data = pd.DataFrame({
    'CO2 Emissions (kt)': co2_selected_df.loc['China'],
    'Renewable Energy (%)': renewable_energy_selected_df.loc['China'],
    'Population Growth (%)': population_growth_selected_df.loc['China']
})
china_correlation = china_data.corr()

# Plotting the correlation as a heatmap for China
plt.figure(figsize=(8, 6))
sns.heatmap(china_correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation among CO2 Emissions, Renewable Energy, and Population Growth for China (2000-2010)')
plt.show()

# Using functions from mystats on US CO2 Emissions
us_co2_emissions = co2_emission_df.loc['United States', years].dropna()
us_co2_skewness = mystats.skew(us_co2_emissions)
us_co2_kurtosis = mystats.kurtosis(us_co2_emissions)

# Displaying the results
print("Skewness of US CO2 Emissions:", us_co2_skewness)
print("Kurtosis of US CO2 Emissions:", us_co2_kurtosis)
