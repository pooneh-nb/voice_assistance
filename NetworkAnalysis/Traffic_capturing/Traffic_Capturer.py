import asyncio
import os
import signal
import sys
from subprocess import Popen, PIPE
import subprocess


class TrafficCapturer:
    def __init__(self, skill, persona, output_traffic_dir):
        self.SKILL = skill

        file_dir = output_traffic_dir + "/" + self.SKILL  #"/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/Traffic_echo/"
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)
        file_id = os.path.join(file_dir, self.SKILL + '.pcap')
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


