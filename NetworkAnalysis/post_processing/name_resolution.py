import pyshark
import subprocess
import utilities
import os
import csv
from IPy import IP
from dns import resolver,reversename
import socket
import argparse

'''
Basically, the scripts perform:
1) Merge PCAP files for each category into one PCAP file for encrypted traffic.
2) Produce tshark JSON files, each for encrypted and decrypted traffic PCAP files.
3) Produce a unified JSON file in NoMoAds-style.
'''

if __name__ == '__main__':



def extract_ips():
    base_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/Traffic"
    categories = utilities.get_directories_in_a_directory(base_dir)
    for category in categories:
        if not os.path.exists(os.path.join(category, "tshark_report")):
            os.makedirs(os.path.join(category, "tshark_report"))
        pcapFiles = utilities.get_files_in_a_directory(category)

        for pcap in pcapFiles:
            pcapName = pcap.split('/')[-1].split('.')[0]
            out = os.path.join(category, "tshark_report", pcapName)
            command = f"tshark -r {pcap}  -T fields -E separator=, -e ip.src -e ip.dst  > {out}.csv"
            print(command)
            p = subprocess.Popen(command, shell=True)


def unify_category_ips():
    base_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/Traffic"
    categories = utilities.get_directories_in_a_directory(base_dir)
    for category in categories:
        dic_ip = {"src": {}, "dst":{}}
        csvs = utilities.get_files_in_a_directory(os.path.join(category, "tshark_report"))
        for csv_f in csvs:
            with open(csv_f) as csvfile:
                csvReader = csv.reader(csvfile, delimiter=',')
                for row in csvReader:
                    try:
                        src_ip = row[0]
                        dst_ip = row[1]
                        dic_ip["src"][src_ip] = socket.gethostbyaddr(src_ip)[0]
                        dic_ip["dst"][dst_ip] = socket.gethostbyaddr(dst_ip)[0]
                        print(row)
                    except Exception as e:
                        pass
                        #print(e)
def text()
    cmd = ["tshark",
           "-o", "tcp.analyze_sequence_numbers:TRUE",
           "-o", "tcp.desegment_tcp_streams:TRUE",
           "-o", "http.desegment_body:TRUE",
           "-r", outFile, "-T", "json"]
    
unify_category_ips()
