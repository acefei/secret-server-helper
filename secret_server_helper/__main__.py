import requests
import argparse
from pprint import pprint


class SecretSeverHelper:
    def __init__(self, username, password, base_url):
        self.token = self.get_auth_token(username, password, base_url)
        self.api_url = base_url + '/api/v1'

    @staticmethod
    def get_auth_token(username, password, site):
        """Authenticate to Secret Server"""
        creds = {}
        creds['username'] = username
        creds['password'] = password
        creds['grant_type'] = 'password'

        uri = site +  '/oauth2/token'
        headers = {'Accept':'application/json', 'content-type':'application/x-www-form-urlencoded'}
        resp = requests.post(uri, data=creds, headers=headers)

        if resp.status_code not in (200, 304):
            raise Exception("Problems getting a token from Secret Server for %s. %s %s" % (username, resp.status_code, resp))
        return resp.json()["access_token"]

    def get_secret(self, secret_id):
        """REST call to retrieve a secret by ID"""
        headers = {'Authorization':'Bearer ' + self.token, 'content-type':'application/json'}
        resp = requests.get(self.api_url + '/secrets/' + str(secret_id), headers=headers)    

        if resp.status_code not in (200, 304):
            raise Exception("Error retrieving Secret. %s %s" % (resp.status_code, resp))    
        return resp.json()

    @staticmethod
    def __get_or_update_secret_item(secret, field_name, new_value=None):
        """Get or Update the secret item on the secret"""
        for x in secret['items']:
            if x['fieldName'] == field_name:
                if new_value:
                    x['itemValue'] = new_value
                    return
                else:
                    return x['itemValue']
        raise Exception('Secret item not found for item name: %s' % field_name)

    def get_value_by_field_name(self, secret_id, field_name):
        secret = self.get_secret(secret_id)
        return self.__get_or_update_secret_item(secret, field_name)

    def update_secret(self, secret_id, field_name, new_value):        
        """REST call method to update the secret on the server"""
        secret = self.get_secret(secret_id)
        self.__get_or_update_secret_item(secret, field_name, new_value)

        headers = {'Authorization':'Bearer ' + self.token, 'content-type':'application/json'}
        resp = requests.put(self.api_url + '/secrets/' + str(secret['id']), json=secret, headers=headers)    

        if resp.status_code not in (200, 304):
            raise Exception("Error updating Secret. %s %s" % (resp.status_code, resp))    
        return resp.json()

def __arg_parse():
    parser = argparse.ArgumentParser(description="""Secret Server Helper""")
    parser.add_argument("-s", "--site",
            required=True,
            help="The site url of secret server")
    parser.add_argument("-u", "--username", 
            required=True,
            help="The username of secret server"
            )
    parser.add_argument("-p", "--password", 
            required=True,
            help="The password of secret server"
            )
    parser.add_argument("-i", "--id", 
            required=True,
            help="The id of secret")
    parser.add_argument("-f", "--field", 
            help="The field name of secret")
    parser.add_argument("-v", "--value", 
            help="The new value of secret")
    return parser.parse_args()

def main():
    args = __arg_parse()
    ss = SecretSeverHelper(args.username, args.password, args.site)
    if args.field and args.value:
        ss.update_secret(args.id, args.field, args.value)
    elif args.field:
        v = ss.get_value_by_field_name(args.id, args.field)
        print(f'{args.field}: {v}')
    elif args.id:
        pprint(ss.get_secret(args.id))
    else:
        args.print_help()
