import httplib, urllib, os
import json


class Connection(object):
    def __init__(self):
        self.client_id = os.environ.get('CLIENT_ID')
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.version = '20170419'
        self.response_style = 'foursquare'
        self.location = 'll=0.347596,32.582520'
        self.auth_params = {'client_id': self.client_id, 'client_secret': self.client_secret,
                            'v': self.version, 'm': self.response_style, 'limit': 4}


class Api(Connection):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.base_url = 'api.foursquare.com'

    def get_data(self, params=None):
        if params:
            self.auth_params.update(params)
        encoded_params = urllib.urlencode(self.auth_params)

        url_params = encoded_params + '&{0}'.format(self.location)
        conn = httplib.HTTPSConnection(self.base_url)
        conn.request('GET', '/v2/venues/search?' + url_params)
        response = conn.getresponse()

        response_code = response.status
        if response_code == 200:
            data = response.read()
            return json.loads(data)
        return 'Error Code: {0}'.format(response_code)


