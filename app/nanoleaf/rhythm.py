from app.nanoleaf.model import AuroraObject

class Rhythm(AuroraObject):

    def __init__(self, requester):
        super().__init__(requester)

    @property
    def rhythm_connected(self):
        """Returns True if the rhythm module is connected, False if it's not"""
        return self.__requester.request(method="GET", endpoint="rhythm/rhythmConnected")

    @property
    def rhythm_active(self):
        """Returns True if the rhythm microphone is active, False if it's not"""
        return self.__requester.request(method="GET", endpoint="rhythm/rhythmActive")

    @property
    def rhythm_id(self):
        """Returns the ID of the rhythm module"""
        return self.__requester.request(method="GET", endpoint="rhythm/rhythmId")

    @property
    def rhythm_hardware_version(self):
        """Returns the hardware version of the rhythm module"""
        return self.__requester.request(method="GET", endpoint="rhythm/hardwareVersion")

    @property
    def rhythm_firmware_version(self):
        """Returns the firmware version of the rhythm module"""
        return self.__requester.request(method="GET", endpoint="rhythm/firmwareVersion")

    @property
    def rhythm_aux_available(self):
        """Returns True if an aux cable is connected to the rhythm module, False if it's not"""
        return self.__requester.request(method="GET", endpoint="rhythm/auxAvailable")

    @property
    def rhythm_mode(self):
        """Returns the sound source of the rhythm module. 0 for microphone, 1 for aux cable"""
        return self.__requester.request(method="GET", endpoint="rhythm/rhythmMode")

    @rhythm_mode.setter
    def rhythm_mode(self, value):
        """Set the sound source of the rhythm module. 0 for microphone, 1 for aux cable"""
        data = {"rhythmMode": value}
        self.__requester.request(method="PUT", endpoint="rhythm", data=data)

    @property
    def rhythm_position(self):
        """Returns the position and orientation of the rhythm module represented in a dict.

        x - X-coordinate
        y - Y-coordinate
        o - Rotational orientation
        """
        return self.__requester.request(method="GET", endpoint="rhythm/rhythmPos")
