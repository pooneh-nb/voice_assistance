# Voice Assistant Central

## Modifying AVS SDK Code for Logging
**NOTE:** The following steps have been tested with the AVS SDK being installed on a Raspberry Pi 4 as per [the instructions here](https://developer.amazon.com/en-US/docs/alexa/avs-device-sdk/raspberry-pi-script.html).
1) Follow the [steps to install the AVS SDK on a Raspberry Pi 4](https://developer.amazon.com/en-US/docs/alexa/avs-device-sdk/raspberry-pi.html).
2) Right before [running the install.sh script](https://developer.amazon.com/en-US/docs/alexa/avs-device-sdk/raspberry-pi-script.html#run-the-install-script), we need to patch the AVS SDK code with the [code changes from this repository](https://github.com/UmarIqbal/voice-assistant-central/tree/main/avs-sdk-changes).
3) We have to download this repository into the path on the Raspberry Pi we have downloaded the AVS SDK code into. Normally, we will download the AVS SDK code to the `/home/pi` directory if we follow the instructions in step 2) above. Let's do the same for this repository.
```
$ git clone https://github.com/UmarIqbal/voice-assistant-central.git
```
4) Next, we go into `voice-assistant-central/avs-sdk-changes` and execute the `copy.sh` script to copy these files into their respective directories in the AVS SDK code structure. The first argument of the script is the path to the directory that contains the AVS SDK code (i.e., `avs-device-sdk`).
```
$ cd voice-assistant-central/avs-sdk-changes
voice-assistant-central/avs-sdk-changes $ sudo bash copy.sh /home/pi/
```
5) We then continue [the next steps to build the AVS SDK code](https://developer.amazon.com/en-US/docs/alexa/avs-device-sdk/raspberry-pi.html#step-4-build-the-avs-device-sdk).
6) When running our experiments, we will execute the command `sudo bash startsample.sh` as per these instructions that explain [how we authorize and run the sample app](https://developer.amazon.com/en-US/docs/alexa/avs-device-sdk/raspberry-pi.html#step-7-run-and-authorize-the-sample-app). For every run, the AVS SDK will create a new CSV file called `avs-network-traffic-log.csv` in `/home/pi/`. The file name is declared [in this line](https://github.com/UmarIqbal/voice-assistant-central/blob/077081946dad9e0da0d349ca818ac3ace45a438f/avs-sdk-changes/LibcurlHTTP2Request.h#L39)---we can change this path and file name in the future if needed.
7) This logger will stay active as long as the sample Alexa app is run. During our experiments, we can run third-party Alexa skills on the sample Alexa app. Our logger will log all the network packet payload into the CSV file. [A sample CSV file can be seen here](https://drive.google.com/drive/u/1/folders/1zUtPcuQ-f8uvyVuNt1c2lr_qx8hAPE2R). The `direction` value `READ` means that the network traffic goes from the Alexa device to the Amazon cloud server (i.e., client to server). Consequently, `WRITE` means that the network traffic goes from server to client. We are tapping into [the `readCallback()` and `writeCallback()` functions of the LibcurlHTTP2Request class (see the comments of the functions)](https://github.com/alexa/avs-device-sdk/blob/e40477e9f512a9e22cdaac35956488cc8e115011/AVSCommon/Utils/include/AVSCommon/Utils/LibcurlUtils/LibcurlHTTP2Request.h#L128). This function is printed out in the full DEBUG comments when running the sample app.

**NOTE:** All the changes in the patch files are marked by the comment `// NOTE: Added for the ProperData Alexa project network traffic logging.`.
