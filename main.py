import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_colwidth', None)

file_path = './LinkedIn_jobs.csv'  
jobs_df = pd.read_csv(file_path)

exclude_companies = ['TalentKompass Deutschland', 'LHR Global - Saudi Arabia']
jobs_df['Company'] = jobs_df['Company'].str.lower().str.strip()

exclude_companies = [company.lower() for company in exclude_companies]

jobs_df = jobs_df[~jobs_df['Company'].isin(exclude_companies)]

jobs_df = jobs_df.dropna(subset=['Date', 'Company', 'Location'])

jobs_df['Date'] = pd.to_datetime(jobs_df['Date'], errors='coerce')

jobs_df = jobs_df[jobs_df['Date'].notna()]

jobs_df['Date'] = pd.to_datetime(jobs_df['Date'], errors='coerce')

jobs_df = jobs_df.dropna(subset=['Date'])

# Data Refining
jobs_df['Title'] = jobs_df['Title'].str.lower()
jobs_df['Title'] = jobs_df['Title'].str.replace('\n', '').str.strip()

ignore_words = ['senior', 'junior', 'jr', 'entry-level', 'trainee', 'lead', 'associate', 'intern', 'internship', 'internships']

for word in ignore_words:
    jobs_df['Title'] = jobs_df['Title'].str.replace(fr'\b{word}\b', '', regex=True)

jobs_df['Title'] = jobs_df['Title'].apply(lambda title: 'software engineer' if title == 'engineer' else title)

jobs_df = jobs_df.dropna(subset=['Title'])

total_posts = len(jobs_df) 

most_wanted_title = jobs_df['Title'].value_counts().idxmax()
print(f"The most wanted job title is: {most_wanted_title}")

percentage_data = (jobs_df['Title'].value_counts(normalize=True) * 1000).nlargest(15)
percentage_data /= 100  

plt.figure(figsize=(12, 6))
percentage_data.plot(kind='bar')
plt.title('Most 15 Posted Tech Job Titles In LinkedIn in 2023 Between First And Second Quarter In KSA')
plt.xlabel('Job Title')
plt.ylabel('Percentage Out Of Total Tech Related Job Posts')
plt.tight_layout()  
plt.show()
