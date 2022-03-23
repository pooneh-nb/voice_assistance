import utilities
import os

subgrouped_skills = utilities.read_json("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/skills_data/subgrouped_skills.json")
categories = utilities.read_json("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/skills_data/selected_main.json")
traffic_files_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo_0307"

skill_dict = {}
for category in categories:
    count = 0
    skill_dict[category] = {}
    for skill in subgrouped_skills[category]:
        if count >= 50:
            break
        skill_dict[category][skill] = {}
        skill_dict[category][skill] = subgrouped_skills[category][skill]['Total_customer_that_rate_the_skill']
        count += 1

utilities.write_json("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/skills_data/top_skills.json", skill_dict)

# Extract top 50 skills of each category

for category in categories:
    pcaps = utilities.get_files_in_a_directory(os.path.join(traffic_files_dir, category))
    pcaps_list = [pcap.split('/')[-1].split('.')[0] for pcap in pcaps]
    top_skills = list(skill_dict[category].keys())
    for skill in top_skills:
        if skill not in pcaps_list:
            print(category, skill)


