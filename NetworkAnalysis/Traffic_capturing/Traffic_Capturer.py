import asyncio
import os
import signal
import sys
from subprocess import Popen, PIPE
import subprocess


class TrafficCapturer:
    def __init__(self, skill, persona, output_traffic_dir):
        self.SKILL = skill
        file_id = output_traffic_dir + "/" +self.SKILL + '.pcap'  #"/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/Traffic_echo/"
        command = f"tcpdump -i wlo1 -tttt -vvv -w {file_id}"
        self.COMMAND = command
        self._running = True

    def capture_process(self):
        print("\ntcpdump running...\n")
        p = subprocess.Popen(self.COMMAND, shell=True)

    def terminate_process(self):
        # tcpdump_pids = subprocess.check_output(['pidof', 'tcpdump']).split()
        # for pid in tcpdump_pids:
        #     print("[+] Killing PID: ", pid)
        #     os.kill(int(pid), signal.Sugkill)

        command = f"pkill -f tcpdump"
        subprocess.Popen(command, shell=True)


