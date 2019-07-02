from getpass import getpass

from CiscoPrimeAPI.ciscoprimeapi import CiscoPrimeAPI


filename = 'high_avail_info.json'

# AD credentials for object instantiation.
ad_username = input('Enter ad username: ')
ad_pwd = getpass('Enter ad password: ')

# Instantiate CiscoPrimeAPI object with credentials.
r1 = CiscoPrimeAPI(ad_username, ad_pwd)

# Retrieve high availability and parameter info from file, push to APs.
c_list = r1.get_json_high_avail_info(filename)
payload = r1.set_high_avail_payload(c_list)
ap_list = r1.get_ap_id_list(filename)
r1.put_ap_high_avail(ap_list, payload)

