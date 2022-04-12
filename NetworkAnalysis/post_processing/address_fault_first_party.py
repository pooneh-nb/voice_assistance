import os
import utilities
import pandas as pd

df_unique = pd.read_csv("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/report_unique_0307.csv")
df_full = pd.read_csv("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/report_0307.csv")

list_of_faulty_skills = ['B0763CSFD9', 'B06XD6KGS2']

# DF unique
for index, row in df_unique.iterrows():
    if row['skill_name'] == 'B0763CSFD9':
        if row['Domain Name'] == 'youversionapi.com':
            print('yes')
            df_unique.at[index, 'Party'] = 'Third-Party'

    if row['skill_name'] == 'B06XD6KGS2':
        if row['Domain Name'] == 'youversionapi.com':
            df_unique.at[index, 'Party'] = 'Third-Party'

df_unique.to_csv("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/report_unique_0307.csv", index=False)

# DF full
for index, row in df_full.iterrows():
    if row['skill_name'] == 'B0763CSFD9':
        if row['Domain Name'] == 'youversionapi.com':
            df_full.at[index, 'Party'] = 'Third-Party'

    if row['skill_name'] == 'B06XD6KGS2':
        if row['Domain Name'] == 'youversionapi.com':
            df_full.at[index, 'Party'] = 'Third-Party'

df_full.to_csv("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/report_0307.csv", index=False)