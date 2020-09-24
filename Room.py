import logging
logger = logging.getLogger('flair_app')


class Room:
    def __init__(self, flair=None,
                 name=None,
                 desiredTemperature=None,
                 temperature=None,
                 location='',
                 heatException=True,
                 coolException=True,
                 vent=None):
        self.flair = flair
        self.name = self.setName(flair, name)
        self.desiredTemperature = self.setDesiredTemperature(flair, desiredTemperature)
        self.temperature = self.setCurrentTemperature(flair, temperature)
        self.location = location
        self.heatException = heatException
        self.coolException = coolException
        self.vent = vent

    def openVent(self, percentage=100):
        if self.vent is not None and self.vent.attributes.get('percent-open') != percentage:
            self.vent.update(attributes={'percent-open': percentage})
        else:
            logger.debug("Can't Open Vent due to Vent Doesn't Exist or Vent is Already Open")

    def closeVent(self, percentage=0):
        if self.vent is not None and self.vent.attributes.get('percent-open') != percentage:
            self.vent.update(attributes={'percent-open': percentage})
        else:
            logger.debug("Can't Close Vent due to Vent Doesn't Exist or Vent is Already Closed")

    def convertToFahrenheit(self, temp):
        return (temp * (9 / 5)) + 32

    def isDownStairs(self):
        if self.location == 'downstairs':
            return True
        else:
            return False

    def isUpStairs(self):
        if self.location == 'upstairs':
            return True
        else:
            return False

    def isDesiredTemperatureReached(self):
        return self.desiredTemperature >= self.temperature

    def isHeatException(self):
        return self.heatException

    def isCoolException(self):
        return self.coolException

    def setName(self, flair, name):
        if flair is None or name is not None:
            return name
        else:
            return flair.attributes.get('name')

    def setDesiredTemperature(self, flair, desiredTemperature):
        if flair is None:
            return desiredTemperature
        else:
            return self.convertToFahrenheit(flair.attributes.get('set-point-c'))

    def setCurrentTemperature(self, flair, currentTemperature):
        if flair is None:
            return currentTemperature
        else:
            try:
                return self.convertToFahrenheit(flair.attributes.get('current-temperature-c'))
            except Exception:
                logger.warning("Exception Occurred when trying to convert temperature to Fahrenheit")