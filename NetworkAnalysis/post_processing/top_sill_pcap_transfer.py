import utilities
import os
import shutil


traffic_original = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo_0307"
traffic_new = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo_0307_new"
top_skills = utilities.read_json("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/skills_data/top_skills.json")

for category, skills in top_skills.items():
    if not os.path.exists(os.path.join(traffic_new, category)):
        os.makedirs(os.path.join(traffic_new, category))
    for skill in skills:
        src = os.path.join(traffic_original, category, skill+'.pcap')
        dst = os.path.join(traffic_new, category)
        shutil.copy(src, dst)

