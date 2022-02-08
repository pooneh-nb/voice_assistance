import pandas as pd
import utilities

report = utilities.read_json("/home/c2//alexa/source/voice-assistant-central/NetworkAnalysis/data/skills_data/third_party_info.json")
df = pd.DataFrame(report, columns = ['PCAP', 'Name', 'URL', 'Category'])
print(df)
