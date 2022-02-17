import utilities
import os
import socket

Traffic = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo_1.1.1.1"
categories = utilities.get_directories_in_a_directory(Traffic)
base_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/post_processed/encrypted_echo"

general_dns_resolutions = {}
for category in categories:
    category_name = category.split('/')[-1]
    dns_resolutions = utilities.read_json(os.path.join(Traffic, category_name, "dns_resolutions.json"))
    for ip, dns_name in dns_resolutions.items():
        if ip not in general_dns_resolutions:
            general_dns_resolutions[ip] = dns_name
    print(category)
utilities.write_json(os.path.join(base_dir, "general_dns_resolutions.json"), general_dns_resolutions)