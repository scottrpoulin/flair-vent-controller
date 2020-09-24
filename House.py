

class House:
    def __init__(self, rooms, upstairs, downstairs, season, equipmentStatus):
        self.rooms = rooms
        self.upstairs = upstairs
        self.downstairs = downstairs
        self.season = season
        self.fanStatus = self.fanState(equipmentStatus)
        self.hvacStatus = self.hvacState(equipmentStatus)

    def openAllVents(self):
        for room in self.rooms:
            if room.vent is not None:
                room.openVent()

    def hvacState(self, equipmentStatus):
        if 'heat' == equipmentStatus:
            return 'heat'
        elif 'cool' == equipmentStatus:
            return 'cool'
        else:
            return equipmentStatus

    def fanState(self, equipmentStatus):
        if 'fan' == equipmentStatus:
            return 'on'
        else:
            return 'off'

