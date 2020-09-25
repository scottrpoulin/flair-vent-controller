import logging

logger = logging.getLogger('flair_app')
class Room:
    def __init__(self, flair=None,
                 name=None,
                 desiredTemperature=None,
                 temperature=None,
                 season=None,
                 location='',
                 heatException=True,
                 coolException=True,
                 vent=None):
        self.flair = flair
        self.name = self.setName(flair, name)
        self.desiredTemperature = self.setDesiredTemperature(flair, desiredTemperature)
        self.temperature = self.setCurrentTemperature(flair, temperature)
        self.season = season
        self.location = location
        self.heatException = heatException
        self.coolException = coolException
        self.vent = vent

    def openVent(self, percentage=100):
        percentageOpen = self.ventStatus()
        if self.vent is not None and percentageOpen != percentage:
            self.vent.update(attributes={'percent-open': percentage})
        elif percentageOpen == percentage:
            logger.debug("Vent is Already Open")
        else:
            logger.debug("Can't Open Vent due to Vent Doesn't Exist")

    def closeVent(self, percentage=0):
        percentageOpen = self.ventStatus()
        if self.vent is not None and percentageOpen != percentage:
            self.vent.update(attributes={'percent-open': percentage})
        elif percentageOpen == percentage:
            logger.debug("Vent is Already Closed")
        else:
            logger.debug("Can't Close Vent due to Vent Doesn't Exist")

    def ventStatus(self):
        if self.vent is not None:
            return self.vent.attributes.get('percent-open')

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
        if self.season == 'cool':
            return self.desiredTemperature >= self.temperature
        elif self.season == 'heat':
            return self.desiredTemperature <= self.temperature

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
        if flair is None and desiredTemperature is not None:
            return self.convertToFahrenheit(desiredTemperature)
        else:
            return self.convertToFahrenheit(flair.attributes.get('set-point-c'))

    def setCurrentTemperature(self, flair, currentTemperature):
        if flair is None and currentTemperature is not None:
            return currentTemperature
        else:
            try:
                return self.convertToFahrenheit(flair.attributes.get('current-temperature-c'))
            except Exception:
                logger.exception("Exception Occurred when trying to convert temperature to Fahrenheit")