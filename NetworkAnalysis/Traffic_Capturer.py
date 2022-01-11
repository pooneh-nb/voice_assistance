import asyncio
import sys
from subprocess import Popen, PIPE
import subprocess


class TrafficCapturer:
    def __init__(self, skill):
        self.SKILL = skill
        file_id = self.SKILL + '.pcap'
        command = f"tcpdump -i wlo1 src 10.42.0.11 -vvv -w {file_id}"
        self.COMMAND = command

    # def initialize(self):
    #     file_id = self.SKILL + '.pcap'
    #     command = f"tcpdump -i wlo1 src 10.42.0.11 -vvv -w {file_id}"
    #     self.COMMAND = command

    # Async method to start the capture.
    async def dispatch_capture(self):
        #self.initialize()
        print("Capturing command: {0}".format(self.COMMAND))
        capture_pid = None
        print("-- Start Capturing Network Traffic --")

        try:
            capture_pid = await self.capture_process()
            #print("Install skill")
            # await self.kill_process(capture_pid)

        except OSError as err:
            print("-- Exiting due to an operating system failure --")
            # print("-- {0} lines captured in your filter --"
            #       .format(line_count))
            print("Error: {0}".format(err))
            sys.exit(0)
        except AttributeError as err:
            print("-- Exiting due to an AttributeError --")
            # print("-- {0} lines captured in your filter --"
            #       .format(line_count))
            print("Error: {0}".format(err))
        except:
            print("-- Unexpected excpetion received --")
            # print("-- {0} lines captured in your filter --"
            #       .format(line_count))
            print("Errors: {0}".format(sys.exc_info()[0]))
            sys.exit(0)
        finally:
            print("Finally")
            # txt_file_obj.close()
            await self.kill_process(capture_pid)

    async def capture_process(self):
        print("capture_process")
        return await asyncio.create_subprocess_shell(self.COMMAND,
                                                     stdout=asyncio.subprocess.PIPE,
                                                     stderr=asyncio.subprocess.PIPE)

    async def kill_process(self, capture_pid):
        print("kill_process")
        capture_pid.send_signal(subprocess.signal.SIGTERM)
        await capture_pid.wait()