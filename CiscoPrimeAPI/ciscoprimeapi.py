import json
import time

import requests


class CiscoPrimeAPI:
    # Set api url values.
    base_url = "https://[ciscoprimedomainname]"
    ap_url = f"{base_url}/webacs/api/v4/data/AccessPoints.json"
    ap_detail_url = f"{base_url}/webacs/api/v4/data/AccessPointDetails/"
    ap_put_url = f"{base_url}/webacs/api/v4/op/apService/accessPoint"

    # Set check security certificate to false for web session.
    verify = False

    # Cisco Prime credentials passed to create object.
    def __init__(self, ad_username, ad_pwd):
        self.ad_username = ad_username
        self.ad_pwd = ad_pwd

    def __repr__(self):
        return f'Cisco Prime API Config Object'

    # Creates dictionary from json file.
    def load_json_file(self, filename):
        with open(filename) as j_obj:
            ap_cfg_file = json.load(j_obj)
            ap_cfg_data = ap_cfg_file['ap_cfg_data']
            return ap_cfg_data

    # Extracts controllers list from json dict.
    def get_json_high_avail_info(self, filename):
        ap_cfg_data = self.load_json_file(filename)
        if not 1 <= len(ap_cfg_data['high_avail_controllers']) <= 3:
            raise Exception('Cisco Prime only allows 1 to 3 '
                            'controllers for high availability.')
        controller_list = ap_cfg_data['high_avail_controllers']
        return controller_list

    # Fill in high availability payload with controller in list.
    def set_high_avail_payload(self, controller_list):
        high_avail_payload = {
          "unifiedApDetailsDTO": {
            "accessPointId": None,
            "primaryMwar": {
              "ipAddress": {
                "address": ""
                  },
              "sysName": ""
                },
            "secondaryMwar": {
              "ipAddress": {
                "address": ""
                  },
              "sysName": ""
                },
            "tertiaryMwar": {
              "ipAddress": {
                "address": ""
                  },
              "sysName": ""
                }
              }
            }
        payload_list = list(high_avail_payload['unifiedApDetailsDTO'])
        for i in range(len(controller_list)):
            high_avail_payload['unifiedApDetailsDTO'][payload_list[i + 1]][
                'ipAddress']['address'] = controller_list[i]['ip_add']
            high_avail_payload['unifiedApDetailsDTO'][payload_list[i + 1]][
                'sysName'] = controller_list[i]['host_name']
        return high_avail_payload

    # Retrieves list of AP IDs that match the criteria in json file.
    def get_ap_id_list(self, filename):
        ap_cfg_data = self.load_json_file(filename)
        parameters = ap_cfg_data['parameters']
        # Establish requests session.
        with requests.Session() as s:
            s.auth = (self.ad_username, self.ad_pwd)
            s.verify = self.verify
            s.params = parameters
            # Get request for list of APs that match criteria in json file.
            r = s.get(f'{self.ap_detail_url}.json', timeout=5)
            r.raise_for_status()
            response_dict = r.json()
            if not response_dict['queryResponse']['@count']:
                ap_id_list = []
                return ap_id_list
            # Extract AP IDs from response.
            raw_ap_list = response_dict['queryResponse']['entityId']
            ap_id_list = [ap['$'] for ap in raw_ap_list]

        return ap_id_list

    # Retrieve AP information for APs in list.
    def get_ap_details(self, ap_id_list):
        ap_detail_list = []
        # Establish requests session.
        with requests.Session() as s:
            s.auth = (self.ad_username, self.ad_pwd)
            s.verify = self.verify
            # AP detail request for each AP in list.
            for ap in ap_id_list:
                ap_detail_dict = {}
                r = s.get(f"{self.ap_detail_url}{ap}.json")
                r.raise_for_status()
                ap_raw_dict = r.json()
                ap_dict = ap_raw_dict['queryResponse']['entity'][0][
                    'accessPointDetailsDTO']
                ap_detail_dict['name'] = ap_dict['name']
                ap_detail_dict['ipAddress'] = ap_dict['ipAddress']['address']
                ap_detail_dict['model'] = ap_dict['model']
                ap_detail_dict['cdpNeighborName'] = ap_dict['cdpNeighbors'][
                    'cdpNeighbor'][0]['neighborName']
                ap_detail_dict['cdpNeighborIP'] = ap_dict['cdpNeighbors'][
                    'cdpNeighbor'][0]['neighborIpAddress']['address']
                ap_detail_dict['cdpNeighborPort'] = ap_dict['cdpNeighbors'][
                    'cdpNeighbor'][0]['neighborPort']
                ap_detail_list.append(ap_detail_dict)
                # Sleep timer to avoid api call threshold.
                time.sleep(0.4)

        return ap_detail_list

    # Set high availability for APs in list with controllers in payload.
    def put_ap_high_avail(self, ap_id_list, payload):
        # Establish requests session.
        with requests.Session() as s:
            s.auth = (self.ad_username, self.ad_pwd)
            s.verify = False
            # Send put request for each AP.
            for ap in ap_id_list:
                # Set accessPointId in payload.
                payload['unifiedApDetailsDTO']['accessPointId'] = ap
                r = s.put(f"{self.ap_put_url}.json", timeout=5, json=payload)
                r.raise_for_status()
                # Sleep timer to avoid api call threshold.
                time.sleep(0.4)
