import utilities
import os

third_category_name = ['35.208.24.246', '192.173.29.77', '208.80.55.212', '103.103.196.113', '103.89.74.186', '87.230.23.99', '147.160.138.27']
categories_echo = utilities.get_directories_in_a_directory(
    "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo/")

for category in categories_echo:
    #print(category)

    category_name = category.split('/')[-1]
    pcap_jsons_dir = os.path.join(
        "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo/", category_name, "jsons")
    pcap_jsons = utilities.get_files_in_a_directory(pcap_jsons_dir)

    for pcap in pcap_jsons:
        pcap_name = pcap.split('/')[-1].split('.')[0]
        ip_set = set()
        network_json = utilities.read_json(pcap)

        for i in range(len(network_json)):
            if 'ip' in network_json[i]["_source"]["layers"].keys():
                ip_set.add(network_json[i]["_source"]["layers"]['ip']['ip.src'])
                ip_set.add(network_json[i]["_source"]["layers"]['ip']['ip.dst'])
        for ip in ip_set:
            if ip in third_category_name:
                print(ip, pcap_name, category)
