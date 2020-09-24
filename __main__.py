from Room import Room
from House import House
from MyFlair import MyFlair
import logging.handlers as handlers
import time
import logging
import constant


def convertToFahrenheit(tempInCelcius):
    return (tempInCelcius * (9/5)) + 32


def initialize(client_id, client_secret):
    myflair = MyFlair(client_id, client_secret)
    equipmentStatus = myflair.getThermostatOperatingState()
    hvacMode = myflair.getHvacMode()

    masterBedRoom = Room(flair=myflair.getRoom(constant.MASTER_BEDROOM_ID),
                         location=constant.UPSTAIRS,
                         heatException=False,
                         coolException=False)

    upstairs2ndBedroom = Room(flair=myflair.getRoom(constant.UPSTAIRS_SECOND_ID),
                              location=constant.UPSTAIRS,
                              heatException=False,
                              coolException=False)

    livingRoom = Room(flair=myflair.getRoom(constant.LIVING_ROOM_ID),
                      location=constant.UPSTAIRS,
                      vent=myflair.getRoomVent(constant.LIVING_ROOM_VENT),
                      heatException=False,
                      coolException=True)

    kitchen = Room(flair=myflair.getRoom(constant.KITCHEN_ID),
                   name='Kitchen',
                   location=constant.UPSTAIRS,
                   vent=myflair.getRoomVent(constant.KITCHEN_VENT),
                   heatException=False,
                   coolException=True)

    foyer = Room(flair=myflair.getRoom(constant.FOYER_ID),
                 name='Foyer', location=constant.UPSTAIRS,
                 vent=myflair.getRoomVent(constant.FOYER_VENT),
                 heatException=False,
                 coolException=True)

    office = Room(flair=myflair.getRoom(constant.OFFICE_ID),
                  name='Office',
                  location=constant.UPSTAIRS,
                  vent=myflair.getRoomVent(constant.OFFICE_VENT),
                  heatException=True,
                  coolException=True)

    downstairsBarAndGameRoom = Room(flair=myflair.getRoom(constant.GAME_ROOM_ID),
                                    location=constant.DOWNSTAIRS,
                                    vent=myflair.getRoomVent(constant.GAME_ROOM_VENT),
                                    heatException=False,
                                    coolException=False)

    downstairsMainRoom = Room(flair=myflair.getRoom(constant.DOWNSTAIRS_MAIN_ID),
                              location=constant.DOWNSTAIRS,
                              vent=myflair.getRoomVent(constant.DOWNSTAIRS_MAIN_VENT),
                              heatException=True,
                              coolException=True)

    downstairs2ndBedroom = Room(flair=myflair.getRoom(constant.DOWNSTAIRS_SECOND_ID),
                                location=constant.DOWNSTAIRS,
                                vent=myflair.getRoomVent(constant.DOWNSTAIRS_SECOND_VENT),
                                heatException=True,
                                coolException=False)

    workoutRoom = Room(flair=myflair.getRoom(constant.DOWNSTAIRS_SECOND_ID),
                       name='Workout Room', location=constant.DOWNSTAIRS,
                       vent=myflair.getRoomVent(constant.WORKOUT_ROOM_VENT),
                       heatException=True,
                       coolException=False)


    rooms = [masterBedRoom, upstairs2ndBedroom, livingRoom, kitchen, foyer, office,
             downstairsBarAndGameRoom, downstairsMainRoom, downstairs2ndBedroom, workoutRoom]
    upstairs = [masterBedRoom, upstairs2ndBedroom, livingRoom, kitchen, foyer, office]
    downstairs = [downstairsBarAndGameRoom, downstairsMainRoom, downstairs2ndBedroom, workoutRoom]
    return House(rooms=rooms,
                 upstairs=upstairs,
                 downstairs=downstairs,
                 season=hvacMode,
                 equipmentStatus=equipmentStatus)

client_id = constant.CLIENT_ID
client_secret = constant.CLIENT_SECRET

logger = logging.getLogger('flair_app')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logHandler = handlers.RotatingFileHandler(filename=constant.FILENAME,
                                          maxBytes=constant.MAX_FILE_BYTES,
                                          backupCount=constant.NUM_FILE_HISTORY)
logHandler.setLevel(logging.DEBUG)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

while True:
    logger.info("Running Cycle To Check System")
    house = initialize(client_id, client_secret)
    logger.debug("House Season: "+house.season)
    logger.debug("House Fan State: "+house.fanStatus)
    logger.debug("House HVAC State: " +house.hvacStatus)
    if house.season == 'cool' and house.hvacStatus == 'cool':
        logger.info('Cooling')
        for room in house.downstairs:
            if room.isDesiredTemperatureReached() and not room.isCoolException():
                logger.debug("Closing Vent For Room: " + room.name)
                logger.debug("Room Temperature: {:.2f} F".format(room.temperature))
                logger.debug("Room Desired Temperature: {:.2f} F".format(room.desiredTemperature))
                room.closeVent()
            else:
                logger.debug("Opening Vent For Room: " + room.name)
                logger.debug("Room Temperature: {:.2f} F".format(room.temperature))
                logger.debug("Room Desired Temperature: {:.2f} F".format(room.desiredTemperature))
                room.openVent()
        for room in house.upstairs:
            logger.debug("Opening Vent For Room: " + room.name)
            logger.debug("Room Temperature: {:.2f} F".format(room.temperature))
            logger.debug("Room Desired Temperature: {:.2f} F".format(room.desiredTemperature))
            room.openVent()
    elif house.season == 'heat' and house.hvacStatus == 'heat':
        logger.info('Heating')
        for room in house.rooms:
            if room.isDesiredTemperatureReached() and not room.isHeatException():
                logger.debug("Closing Vent For Room: "+room.name)
                logger.debug("Room Temperature: {:.2f} F".format(room.temperature))
                logger.debug("Room Desired Temperature: {:.2f} F".format(room.desiredTemperature))
                room.closeVent()
            else:
                logger.debug("Opening Vent For Room: " + room.name)
                logger.debug("Room Temperature: {:.2f} F".format(room.temperature))
                logger.debug("Room Desired Temperature: {:.2f} F".format(room.desiredTemperature))
                room.openVent()
    else:
        logger.info('Checking For Fan Running')
        if house.fanStatus == 'on' and house.hvacStatus == 'fan':
            logger.debug("Opening All Vents for Ventilation")
            house.openAllVents()
        else:
            logger.debug("Nothing To Do")
    logger.info("Going To Sleep for 4 Minutes")
    time.sleep(240)



