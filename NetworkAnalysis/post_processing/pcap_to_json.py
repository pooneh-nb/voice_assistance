#!/usr/bin/python

import os
import subprocess
import utilities
from subprocess import check_call
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())


base_traffic_echo_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo_0307_new"
categories = utilities.get_directories_in_a_directory(base_traffic_echo_dir)

for category in categories:
    jsons_dir = os.path.join(category, "jsons")
    if not os.path.exists(jsons_dir):
        os.mkdir(os.path.join(category, "jsons"))

for category in categories:

    print(category)
    pcaps = utilities.get_files_in_a_directory(category)
    for pcap in pcaps:
        pcap_name = pcap.split('/')[-1].split('.')[0]
        if pcap.split('/')[-1].split('.')[-1] != 'pcap':
            continue

        outFile = os.path.join(category, "jsons", pcap_name+".json")
        cmd = ["tshark",
               "-o", "tcp.analyze_sequence_numbers:TRUE",
               "-o", "tcp.desegment_tcp_streams:TRUE",
               "-o", "http.desegment_body:TRUE",
               "-r", pcap, "-T", "json"]

        with open(outFile, "wb") as jf:
            check_call(cmd, stdout=jf)
print("DONE!")

