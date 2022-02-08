#!/usr/bin/python

'''
This script calls the other scripts in the data_preparation directory to perform the second phase of the pipeline.
Basically, the scripts perform:
1) Merge PCAP files for each app into one PCAP file for encrypted traffic and one PCAP file for decrypted traffic.
2) Produce tshark JSON files, each for encrypted and decrypted traffic PCAP files.
3) Produce a unified JSON file in NoMoAds-style.
4) Run the unified JSON file through the filter-list matching script.
5) Finally, produce a CSV file that contains the flow of traffic for further processing (e.g., ATS analyses, policy analyses, etc.)
'''
# /home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/Traffic_echo

import argparse
import os
import subprocess
import shutil
import pandas as pd

from NetworkAnalysis.utils.utils import DIR_DELIMITER
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

# Filter list result directory
FL_RESULT_DIR = "filters_matching_results"

if __name__ == '__main__':
    # ap = argparse.ArgumentParser(description='Runs the full Alexa pipeline')
    # ap.add_argument('dataset_root_dir', type=str, help='root directory of dataset')
    # ap.add_argument('category_csvs_dir', type=str, help='directory of csvs about categories')
    #
    # args = ap.parse_args()

    # Get the absolute paths
    # dataset_root_abs_dir = os.path.abspath(args.dataset_root_dir)
    # category_csvs_abs_dir = os.path.abspath(args.category_csvs_dir)
    dataset_root_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_sdk"
    category_csvs_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/post_processed/encrypted_sdk"
    dataset_root_abs_dir = os.path.abspath(dataset_root_dir)
    category_csvs_abs_dir = os.path.abspath(category_csvs_dir)

    # TEMP_OUTPUT_NAME = "temp_output"
    # CSV_TMP_NAME = "csv"
    # output_tmp_dir = dataset_root_abs_dir + os.sep + TEMP_OUTPUT_NAME
    # if os.path.isdir(output_tmp_dir):
    #     shutil.rmtree(output_tmp_dir)
    # os.makedirs(output_tmp_dir)

    # keep track of dfs per category
    data_frames = []

    # For each category:
    #   Iterate over category subdirectories that contain the PCAP files and call the necessary scripts
    for category_name in os.listdir(dataset_root_abs_dir):

        # skill_dir_path_tuple = []
        category_dir = os.path.join(dataset_root_abs_dir, category_name)
        print(f"Processing data from Category: {category_name}")

        # The pipeline
        # 1) Merge PCAP files for each category into one PCAP file for encrypted traffic
        # 2) Produce tshark JSON files, for encrypted PCAP files.
        print(f"[+] {category_name}: Merging encrypted PCAP files and creating a JSON file using tshark...")
        ret = subprocess.check_call(["python3", "merge_cap.py", "-enc", category_dir])

        # 3) Produce a unified JSON file in NoMoAds-style.
        # print(f"[+] {category_name}: Creating a unified JSON file...\n")
        # ret = subprocess.check_call(["python3", "extract_from_tshark.py",
        #                              "--enc_file",
        #                              os.path.join(category_dir + "-ENC-out.json"),
        #                              "--out_file",
        #                              os.path.join(category_dir + "-out-nomoads.json"),
        #                              "--include_http_body"
        #                              ])




