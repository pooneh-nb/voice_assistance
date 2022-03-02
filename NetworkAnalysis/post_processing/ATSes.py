import utilities
import os


def disconnectme(base):
    disconnect_tracker = []
    disconnect_ad = []
    general_disconnect = utilities.read_json(os.path.join(base, "original_files", "disconnect_services.json"))
    # advertising
    for entity in general_disconnect['categories']['Advertising']:
        for name, values in entity.items():
            for fqdn, domainName in values.items():
                disconnect_ad.extend(domainName)
    utilities.write_json(os.path.join(base, "advertising", "disconnect_ad.json"), disconnect_ad)

    # tracking
    for entity in general_disconnect['categories']['Analytics']:
        for name, values in entity.items():
            for fqdn, domainName in values.items():
                disconnect_tracker.extend(domainName)
    utilities.write_json(os.path.join(base, "analytics", "disconnect_tracker.json"), disconnect_tracker)


def advertising(base):
    pihole_ads = []
    ad_files = utilities.get_files_in_a_directory(os.path.join(base, "original_files", "advertising"))
    for adFile in ad_files:
        text_file = open(adFile, "r")
        for line in text_file:
            if not line.startswith("#") and line != '\n':
                stripped_line = line.strip()
                line_list = str(stripped_line.split()[0])
                pihole_ads.append(line_list)
        text_file.close()

    utilities.write_json(os.path.join(base, "advertising", "pihole_ad.json"), pihole_ads)


def tracking(base):
    pihole_tracking = []
    ad_files = utilities.get_files_in_a_directory(os.path.join(base, "original_files", "tracking"))
    for adFile in ad_files:
        text_file = open(adFile, "r")
        for line in text_file:
            if not line.startswith("#") and line != '\n':
                stripped_line = line.strip()
                line_list = str(stripped_line.split()[0])
                pihole_tracking.append(line_list)
        text_file.close()

    utilities.write_json(os.path.join(base, "tracking", "pihole_tracking.json"), pihole_tracking)

def combine_lists(base):
    tracking_lists = utilities.get_files_in_a_directory(os.path.join(base, tracking()))
    for tracking_file in tracking_lists:
        tracking_list = utilities.read_json()

def main():
    base_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/filter_lists"
    # disconnectme(base_dir)
    #advertising(base_dir)
    tracking(base_dir)


if __name__ == '__main__':
    main()