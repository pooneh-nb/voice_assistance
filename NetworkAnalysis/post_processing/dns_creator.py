import utilities
import os

Traffics = ["/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo_0307_new",
            "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo_0307"]


# "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo_1.1.1.1",
# "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/Traffic/Traffic_echo"

dns_resolutions = {}
for Traffic in Traffics:
    categories = utilities.get_directories_in_a_directory(Traffic)
    # base_dir = "/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/post_processed/encrypted_echo/"

    for category in categories:
        # print(category)
        category_name = category.split('/')[-1]
        print(category)
        network_json_dir = os.path.join(Traffic, category_name, category_name + "-ENC-out.json")
        network_json = utilities.read_json(network_json_dir)

        for i in range(len(network_json)):
            if network_json[i]["_source"]["layers"]["frame"]["frame.protocols"] == 'eth:ethertype:ip:udp:dns':
                if "Answers" in network_json[i]["_source"]["layers"]["dns"].keys():
                    dns_name = list(network_json[i]["_source"]["layers"]["dns"]["Queries"].keys())[0].split(':')[0]

                    if dns_name not in dns_resolutions:
                        dns_resolutions[dns_name] = set()

                    answers_key = network_json[i]["_source"]["layers"]["dns"]["Answers"].keys()
                    # print(dns_name)
                    for key in answers_key:
                        if "CNAME" in key:
                            continue
                        try:
                            ip = network_json[i]["_source"]["layers"]["dns"]["Answers"][key]["dns.a"]
                            # print(type(dns_resolutions[dns_name]))
                            dns_resolutions[dns_name].add(ip)
                        except Exception as ex:
                            print(ex)
                            pass

for dns_n in dns_resolutions:
    dns_resolutions[dns_n] = list(dns_resolutions[dns_n])
utilities.write_json("/home/c2/alexa/source/voice-assistant-central/NetworkAnalysis/data/DNS/dns_0307.json", dns_resolutions)
