import utilities
import os


base_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/Traffic"
categories = utilities.get_directories_in_a_directory(base_dir)

for category in categories:
    category_name = category.split('/')[-1]
    network_json_dir = os.path.join(category, category_name+"-ENC-out.json")
    network_json = dict(utilities.read_json(network_json_dir))
    print(len(network_json))
    print(type(network_json))


    # for key, val in network_json.items():
    #     print(len(key))
    #     print(len(val))