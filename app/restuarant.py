class Restaurant(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{0}'.format(self.name)

    @staticmethod
    def from_json(json_restaurant):
        return Restaurant(json_restaurant['name'])



