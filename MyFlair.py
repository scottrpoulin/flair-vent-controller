from flair_api import make_client


class MyFlair:
    def __init__(self, client_id, client_secret):
        self.client = make_client(client_id, client_secret, 'https://api.flair.co/')

    def getRoomVent(self, id):
        return self.client.get('vents', id)

    def getRoom(self, id):
        return self.client.get('rooms', id)

    def getHvacMode(self):
        return self.client.get('structures').resources[0].attributes.get('structure-heat-cool-mode')

    def getThermostatOperatingState(self):
        return self.client.get('thermostat-states').resources[0].attributes.get('operating-state')

    def getDesiredTemperature(self):
        return self.client.get('structures').resources[0].attributes.get('set-point-temperature-c')