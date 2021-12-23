import pandas as pd
import os

def round_decimals(num):
  return round(num,1)

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv(os.getcwd() + "/adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df.groupby(['race']).size().sort_values(ascending=False)

    # What is the average age of men?
    average_age_men = df[df.sex == 'Male'].mean()['age']
    average_age_men = round_decimals(average_age_men)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = (df.groupby('education').size()/df.count()['education'])['Bachelors'] * 100

    percentage_bachelors = round_decimals(percentage_bachelors)


    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[df.education.isin(['Bachelors', 'Masters', 'Doctorate'])]
    lower_education = df[~df.education.isin(['Bachelors', 'Masters', 'Doctorate'])]

    # percentage with salary >50K
    higher_education_rich = (higher_education.groupby('salary').size()/higher_education.count()['salary'])['>50K'] * 100.0000
    higher_education_rich = round_decimals(higher_education_rich)

    lower_education_rich = (lower_education.groupby('salary').size()/lower_education.count()['salary'])['>50K'] * 100.0000
    lower_education_rich = round_decimals(lower_education_rich)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = min(df['hours-per-week'])

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_hour_data = df[df['hours-per-week'] == 1]
    num_min_workers = min_hour_data.count()['salary']
    
    rich_percentage = (min_hour_data.groupby('salary').size()/num_min_workers)['>50K'] * 100

    rich_percentage = round_decimals(rich_percentage)

    # What country has the highest percentage of people that earn >50K?

    rich_country_counts = df[df['salary'] == '>50K'].groupby('native-country').size().reset_index()
    country_counts = df.groupby('native-country').size().reset_index()
    comb = country_counts.merge(rich_country_counts, on='native-country', how='left')
    comb = comb.fillna(0)
    comb['rich_perc'] = comb.apply (lambda row: row['0_y']/row['0_x'], axis=1)
    rich_country_data = comb.sort_values(by=['rich_perc'], ascending=False)

    highest_earning_country = rich_country_data['native-country'].iloc[0]
    highest_earning_country_percentage = rich_country_data['rich_perc'].iloc[0] * 100
    highest_earning_country_percentage = round_decimals(highest_earning_country_percentage)

    # Identify the most popular occupation for those who earn >50K in India.
    ind_rich_data = df[(df['salary'] == '>50K') & (df['native-country'] == 'India')]
    top_IN_occupation = ind_rich_data.groupby('occupation').size().reset_index().sort_values(by=[0], ascending=False)['occupation'].iloc[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
