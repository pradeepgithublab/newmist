import time
import argparse
import json
from prettytable import PrettyTable

# Mock Config class to replace the config module
class Config:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.data = json.load(file)

# Mock logger to replace the logger module
class Logger:
    @staticmethod
    def setLevel(level):
        print(f"Logger level set to {level}")

# Mock API class to replace the api module
class API:
    def __init__(self, config):
        self.config = config
        self.base_url = "https://api.mockservice.com"
    
    def get(self, endpoint):
        # Mock response data
        if endpoint == f"orgs/{self.config.data['org_id']}/sites":
            return [{'id': 'site1', 'name': 'Site 1'}, {'id': 'site2', 'name': 'Site 2'}]
        elif 'stats/devices' in endpoint:
            return [
                {
                    'type': 'ap',
                    'name': 'AP1',
                    'status': 'connected',
                    'radio_stat': {
                        'band_24': {'channel': 1, 'util_all': 50, 'num_clients': 5},
                        'band_5': {'channel': 36, 'bandwidth': 80, 'util_all': 30, 'num_clients': 10}
                    }
                },
                {
                    'type': 'ap',
                    'name': 'AP2',
                    'status': 'connected',
                    'radio_stat': {
                        'band_24': {'channel': 6, 'util_all': 70, 'num_clients': 7},
                        'band_5': {'channel': 44, 'bandwidth': 40, 'util_all': 60, 'num_clients': 15}
                    }
                }
            ]
        return []

    def __exit__(self):
        pass

def script_args_parser():
    """PARSE THE ARGUMENTS AND RETURN CONFIG."""
    parser = argparse.ArgumentParser(
        description='Monitor Channel Utilization of all APs part of a site')
    parser.add_argument('--config', metavar='config_file', type=argparse.FileType(
        'r'), default='config.json', help='file containing all the configuration information')
    parser.add_argument("-v", "--verbose", help="See DEBUG level messages", action="store_true")
    args = parser.parse_args()

    # Create a config object based on the config filename
    config_obj = Config(args.config.name)

    # configure the logger based on the level of verbose
    if args.verbose:
        Logger.setLevel("DEBUG")

    return config_obj

def main():
    """MONITOR CHANNEL UTILIZATION OF ALL APS OF A SITE."""
    config = script_args_parser()
    api_client = API(config)

    # Retrieve the list of sites within my Org
    sites = api_client.get(f"orgs/{config.data['org_id']}/sites")

    for site in sites:
        # Retrieve list of APs and their current stats
        aps = api_client.get(f"sites/{site['id']}/stats/devices")

        # Creation of the table header (for printing results)
        table = PrettyTable(['AP Name', '2.4 Ch.', '2.4 Util.', '2.4 Clts', '5 Ch.', '5 Util.', '5 Clts'])

        # Looping on each AP to retrieve relevant stats (channel utilizations)
        nb_ap_connected = 0
        for ap in aps:
            if ap['type'] == 'ap':
                ap_mon_data = []
                ap_mon_data.append(ap['name'])

                if ap['status'] == 'connected':
                    nb_ap_connected += 1
                    ap_mon_data.append(ap['radio_stat']['band_24']['channel'])
                    ap_mon_data.append(f"{ap['radio_stat']['band_24']['util_all']}%")
                    ap_mon_data.append(ap['radio_stat']['band_24']['num_clients'])
                    ap_mon_data.append(f"{ap['radio_stat']['band_5']['channel']}({ap['radio_stat']['band_5']['bandwidth']})")
                    ap_mon_data.append(f"{ap['radio_stat']['band_5']['util_all']}%")
                    ap_mon_data.append(ap['radio_stat']['band_5']['num_clients'])
                    table.add_row(ap_mon_data)

        # Displaying the results sorting them by 5GHz channel utilization
        print(f"SITE: {site['name']}\t\tAPs Online: {nb_ap_connected}")
        if nb_ap_connected != 0:
            print(table.get_string(sortby="5 Util.", reversesort=True))
        print()

    api_client.__exit__()

if __name__ == '__main__':
    start_time = time.time()
    print('** MONITORING CHANNEL UTILIZATION...\n')
    main()
    run_time = time.time() - start_time
    print(f"\n** Time to run: {round(run_time, 2)} sec")
