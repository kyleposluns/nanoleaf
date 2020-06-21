import colorsys
import random
import re
import socket

from app.nanoleaf.requester import Requester


# Primary interface for an Aurora light
# For instructions or bug reports, please visit
# https://github.com/software-2/nanoleaf


class AuroraStream:
    def __init__(self, addr: str, port: int):
        self._prepare = []
        self.addr = (addr, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)

    def __send(self, msg: bytes):
        self.sock.sendto(msg, self.addr)

    def panel_set(self, panel_id: int, red: int, green: int, blue: int,
                  white: int = 0, transition_time: int = 1):
        b = bytes([1, panel_id, 1, red, green, blue, white, transition_time])
        self.__send(b)

    def panel_prepare(self, panel_id: int, red: int, green: int, blue: int,
                      white: int = 0, transition_time: int = 1):
        self._prepare = self._prepare + [panel_id, 1, red, green, blue, white, transition_time]

    def panel_strobe(self):
        data = [len(self._prepare)] + self._prepare
        self._prepare = []
        self.__send(bytes(data))


class Aurora:

    def __init__(self, ip_address: str = None, auth_token: str = None):
        self.requester = Requester(ip_address, auth_token)

    def __repr__(self):
        return f"<Aurora({self.requester.ip_address})>"

    ###########################################
    # General functionality methods
    ###########################################

    @property
    def info(self):
        """Returns the full Aurora Info request. 
        
        Useful for debugging since it's just a fat dump."""
        return self.requester.request(method="GET")

    @property
    def color_mode(self):
        """Returns the current color mode."""
        return self.requester.request(method="GET", endpoint="state/colorMode")

    def identify(self):
        """Briefly flash the panels on and off"""
        self.requester.request(method="PUT", endpoint="identify", data={})

    @property
    def firmware(self):
        """Returns the firmware version of the device"""
        return self.requester.request(method="GET")["firmwareVersion"]

    @property
    def model(self):
        """Returns the model number of the device. (Always returns 'NL22')"""
        return self.requester.request(method="GET")["model"]

    @property
    def serial_number(self):
        """Returns the serial number of the device"""
        return self.requester.request(method="GET")["serialNo"]

    def delete_user(self):
        """CAUTION: Revokes your auth token from the device."""
        self.requester.request(method="DELETE")

    ###########################################
    # On / Off methods
    ###########################################

    @property
    def on(self):
        """Returns True if the device is on, False if it's off"""
        return self.requester.request(method="GET", endpoint="state/on/value")

    @on.setter
    def on(self, value: bool):
        """Turns the device on/off. True = on, False = off"""
        data = {"on": value}
        self.requester.request(method="PUT", endpoint="state", data=data)

    @property
    def off(self):
        """Returns True if the device is off, False if it's on"""
        return not self.on

    @off.setter
    def off(self, value: bool):
        """Turns the device on/off. True = off, False = on"""
        self.on = not value

    def on_toggle(self):
        """Switches the on/off state of the device"""
        self.on = not self.on

    ###########################################
    # Brightness methods
    ###########################################

    @property
    def brightness(self):
        """Returns the brightness of the device (0-100)"""
        return self.requester.request(method="GET", endpoint="state/brightness/value")

    @brightness.setter
    def brightness(self, level):
        """Sets the brightness to the given level (0-100)"""
        data = {"brightness": {"value": level}}
        self.requester.request(method="PUT", endpoint="state", data=data)

    @property
    def brightness_min(self):
        """Returns the minimum brightness possible. (This always returns 0)"""
        return self.requester.request(method="GET", endpoint="state/brightness/min")

    @property
    def brightness_max(self):
        """Returns the maximum brightness possible. (This always returns 100)"""
        return self.requester.request(method="GET", endpoint="state/brightness/max")

    def brightness_raise(self, level):
        """Raise the brightness of the device by a relative amount (negative lowers brightness)"""
        data = {"brightness": {"increment": level}}
        self.requester.request(method="PUT", endpoint="state", data=data)

    def brightness_lower(self, level):
        """Lower the brightness of the device by a relative amount (negative raises brightness)"""
        self.brightness_raise(-level)

    ###########################################
    # Hue methods
    ###########################################

    @property
    def hue(self):
        """Returns the hue of the device (0-360)"""
        return self.requester.request(method="GET", endpoint="state/hue/value")

    @hue.setter
    def hue(self, level):
        """Sets the hue to the given level (0-360)"""
        data = {"hue": {"value": level}}
        self.requester.request(method="PUT", endpoint="state", data=data)

    @property
    def hue_min(self):
        """Returns the minimum hue possible. (This always returns 0)"""
        return self.requester.request(method="GET", endpoint="state/hue/min")

    @property
    def hue_max(self):
        """Returns the maximum hue possible. (This always returns 360)"""
        return self.requester.request(method="GET", endpoint="state/hue/max")

    def hue_raise(self, level):
        """Raise the hue of the device by a relative amount (negative lowers hue)"""
        data = {"hue": {"increment": level}}
        self.requester.request(method="PUT", endpoint="state", data=data)

    def hue_lower(self, level):
        """Lower the hue of the device by a relative amount (negative raises hue)"""
        self.hue_raise(-level)

    ###########################################
    # Saturation methods
    ###########################################

    @property
    def saturation(self):
        """Returns the saturation of the device (0-100)"""
        return self.requester.request(method="GET", endpoint="state/sat/value")

    @saturation.setter
    def saturation(self, level):
        """Sets the saturation to the given level (0-100)"""
        data = {"sat": {"value": level}}
        self.requester.request(method="PUT", endpoint="state", data=data)

    @property
    def saturation_min(self):
        """Returns the minimum saturation possible. (This always returns 0)"""
        self.requester.request(method="GET", endpoint="state/sat/min")

    @property
    def saturation_max(self):
        """Returns the maximum saturation possible. (This always returns 100)"""
        self.requester.request(method="GET", endpoint="state/sat/max")

    def saturation_raise(self, level):
        """Raise the saturation of the device by a relative amount (negative lowers saturation)"""
        data = {"sat": {"increment": level}}
        self.requester.request(method="PUT", endpoint="state", data=data)

    def saturation_lower(self, level):
        """Lower the saturation of the device by a relative amount (negative raises saturation)"""
        self.saturation_raise(-level)

    ###########################################
    # Color Temperature methods
    ###########################################

    @property
    def color_temperature(self):
        """Returns the color temperature of the device (0-100)"""
        return self.requester.request(method="GET", endpoint="state/ct/value")

    @color_temperature.setter
    def color_temperature(self, level):
        """Sets the color temperature to the given level (0-100)"""
        data = {"ct": {"value": level}}
        self.requester.request(method="PUT", endpoint="state", data=data)

    @property
    def color_temperature_min(self):
        """Returns the minimum color temperature possible. (This always returns 1200)"""
        return self.requester.request(method="GET", endpoint="state/ct/min")

    @property
    def color_temperature_max(self):
        """Returns the maximum color temperature possible. (This always returns 6500)"""
        return self.requester.request(method="GET", endpoint="state/ct/max")

    def color_temperature_raise(self, level):
        """Raise the color temperature of the device by a relative amount (negative lowers color temperature)"""
        data = {"ct": {"increment": level}}
        self.requester.request(method="PUT", endpoint="state", data=data)

    def color_temperature_lower(self, level):
        """Lower the color temperature of the device by a relative amount (negative raises color temperature)"""
        self.color_temperature_raise(-level)

    ###########################################
    # Color RGB/HSB methods
    ###########################################

    # TODO: Shame on all these magic numbers. SHAME.

    @property
    def rgb(self):
        """The color of the device, as represented by 0-255 RGB values"""
        hue = self.hue
        saturation = self.saturation
        brightness = self.brightness
        if hue is None or saturation is None or brightness is None:
            return None
        rgb = colorsys.hsv_to_rgb(hue / 360, saturation / 100, brightness / 100)
        return [int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)]

    @rgb.setter
    def rgb(self, color):
        """Set the color of the device, as represented by either a hex string or a list of 0-255 RGB values"""
        try:
            red, green, blue = color
        except ValueError:
            try:
                hexcolor = color
                reg_match = re.match("^([A-Fa-f0-9]{6})$", hexcolor)
                if reg_match:
                    red = int(hexcolor[:2], 16)
                    green = int(hexcolor[2:-2], 16)
                    blue = int(hexcolor[-2:], 16)
                else:
                    print("Error: Color must be in valid hex format.")
                    return
            except ValueError:
                print("Error: Color must have one hex value or three 0-255 values.")
                return
        if not 0 <= red <= 255:
            print("Error: Red value out of range! (0-255)")
            return
        if not 0 <= green <= 255:
            print("Error: Green value out of range! (0-255)")
            return
        if not 0 <= blue <= 255:
            print("Error: Blue value out of range! (0-255)")
            return

        hsv = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        hue = int(hsv[0] * 360)
        saturation = int(hsv[1] * 100)
        brightness = int(hsv[2] * 100)
        data = {"hue": {"value": hue}, "sat": {"value": saturation}, "brightness": {"value": brightness}}
        self.__put("state", data)

    ###########################################
    # Layout methods
    ###########################################

    @property
    def orientation(self):
        """Returns the orientation of the device (0-360)"""
        return self.requester.request(method="GET", endpoint="panelLayout/globalOrientation/value")

    @property
    def orientation_min(self):
        """Returns the minimum orientation possible. (This always returns 0)"""
        return self.requester.request(method="GET", endpoint="panelLayout/globalOrientation/min")

    @property
    def orientation_max(self):
        """Returns the maximum orientation possible. (This always returns 360)"""
        return self.requester.request(method="GET", endpoint="panelLayout/globalOrientation/max")

    @property
    def panel_count(self):
        """Returns the number of panels connected to the device"""
        count = int(self.requester.request(method="GET", endpoint="panelLayout/layout/numPanels"))
        if self.rhythm_connected:
            count -= 1
        return count

    @property
    def panel_length(self):
        """Returns the length of a single panel. (This always returns 150)"""
        return self.requester.request(method="GET", endpoint="panelLayout/layout/sideLength")

    @property
    def panel_positions(self):
        """Returns a list of all panels with their attributes represented in a dict.
        
        panelId - Unique identifier for this panel
        x - X-coordinate
        y - Y-coordinate
        o - Rotational orientation
        """
        return self.requester.request(method="GET", endpoint="panelLayout/layout/positionData")

    ###########################################
    # Effect methods
    ###########################################

    _reserved_effect_names = ["*Static*", "*Dynamic*", "*Solid*"]

    @property
    def effect(self):
        """Returns the active effect"""
        return self.requester.request(method="GET", endpoint="effects/select")

    @effect.setter
    def effect(self, effect_name: str):
        """Sets the active effect to the name specified"""
        data = {"select": effect_name}
        self.requester.request(method="PUT", endpoint="effects", data=data)

    @property
    def effects_list(self):
        """Returns a list of all effects stored on the device"""
        return self.requester.request(method="GET", endpoint="effects/effectsList")

    def effect_random(self) -> str:
        """Sets the active effect to a new random effect stored on the device.
        
        Returns the name of the new effect."""
        effect_list = self.effects_list
        active_effect = self.effect
        if active_effect not in self._reserved_effect_names:
            effect_list.remove(self.effect)
        new_effect = random.choice(effect_list)
        self.effect = new_effect
        return new_effect

    def effect_set_raw(self, effect_data: dict):
        """Sends a raw dict containing effect data to the device.

        The dict given must match the json structure specified in the API docs."""
        data = {"write": effect_data}
        self.requester.request(method="PUT", endpoint="effects", data=data)

    def effect_details(self, name: str) -> dict:
        """Returns the dict containing details for the effect specified"""
        data = {"write": {"command": "request",
                          "animName": name}}
        return self.requester.request(method="PUT", endpoint="effects", data=data)

    def effect_details_all(self) -> dict:
        """Returns a dict containing details for all effects on the device"""
        data = {"write": {"command": "requestAll"}}
        return self.requester.request(method="PUT", endpoint="effects", data=data)

    def effect_delete(self, name: str):
        """Removed the specified effect from the device"""
        data = {"write": {"command": "delete",
                          "animName": name}}
        self.requester.request(method="PUT", endpoint="effects", data=data)

    def effect_rename(self, old_name: str, new_name: str):
        """Renames the specified effect saved on the device to a new name"""
        data = {"write": {"command": "rename",
                          "animName": old_name,
                          "newName": new_name}}
        self.requester.request(method="PUT", endpoint="effects", data=data)

    def effect_stream(self):
        """Open an external control stream"""
        data = {"write": {"command": "display",
                          "animType": "extControl"}}

        udp_info = self.requester.request(method="PUT", endpoint="effects", data=data)
        return AuroraStream(udp_info["streamControlIpAddr"], udp_info["streamControlPort"])

    ###########################################
    # Rhythm methods
    ###########################################

    @property
    def rhythm_connected(self):
        """Returns True if the rhythm module is connected, False if it's not"""
        return self.requester.request(method="GET", endpoint="rhythm/rhythmConnected")

    @property
    def rhythm_active(self):
        """Returns True if the rhythm microphone is active, False if it's not"""
        return self.requester.request(method="GET", endpoint="rhythm/rhythmActive")

    @property
    def rhythm_id(self):
        """Returns the ID of the rhythm module"""
        return self.requester.request(method="GET", endpoint="rhythm/rhythmId")

    @property
    def rhythm_hardware_version(self):
        """Returns the hardware version of the rhythm module"""
        return self.requester.request(method="GET", endpoint="rhythm/hardwareVersion")

    @property
    def rhythm_firmware_version(self):
        """Returns the firmware version of the rhythm module"""
        return self.requester.request(method="GET", endpoint="rhythm/firmwareVersion")

    @property
    def rhythm_aux_available(self):
        """Returns True if an aux cable is connected to the rhythm module, False if it's not"""
        return self.requester.request(method="GET", endpoint="rhythm/auxAvailable")

    @property
    def rhythm_mode(self):
        """Returns the sound source of the rhythm module. 0 for microphone, 1 for aux cable"""
        return self.requester.request(method="GET", endpoint="rhythm/rhythmMode")

    @rhythm_mode.setter
    def rhythm_mode(self, value):
        """Set the sound source of the rhythm module. 0 for microphone, 1 for aux cable"""
        data = {"rhythmMode": value}
        self.requester.request(method="PUT", endpoint="rhythm", data=data)

    @property
    def rhythm_position(self):
        """Returns the position and orientation of the rhythm module represented in a dict.

        x - X-coordinate
        y - Y-coordinate
        o - Rotational orientation
        """
        return self.requester.request(method="GET", endpoint="rhythm/rhythmPos")
