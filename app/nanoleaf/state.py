import colorsys
import re

from app.nanoleaf.model import AuroraObject


class State(AuroraObject):

    def __init__(self, requester):
        super().__init__(requester)

    @property
    def color_mode(self):
        """Returns the current color mode."""
        return self.__requester.request(method="GET", endpoint="state/colorMode")

    @property
    def on(self):
        """Returns True if the device is on, False if it's off"""
        return self.__requester.request(method="GET", endpoint="state/on/value")

    @on.setter
    def on(self, value: bool):
        """Turns the device on/off. True = on, False = off"""
        data = {"on": value}
        self.__requester.request(method="PUT", endpoint="state", data=data)

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

    @property
    def brightness(self):
        """Returns the brightness of the device (0-100)"""
        return self.__requester.request(method="GET", endpoint="state/brightness/value")

    @brightness.setter
    def brightness(self, level):
        """Sets the brightness to the given level (0-100)"""
        data = {"brightness": {"value": level}}
        self.__requester.request(method="PUT", endpoint="state", data=data)

    @property
    def brightness_min(self):
        """Returns the minimum brightness possible. (This always returns 0)"""
        return self.__requester.request(method="GET", endpoint="state/brightness/min")

    @property
    def brightness_max(self):
        """Returns the maximum brightness possible. (This always returns 100)"""
        return self.__requester.request(method="GET", endpoint="state/brightness/max")

    def brightness_raise(self, level):
        """Raise the brightness of the device by a relative amount (negative lowers brightness)"""
        data = {"brightness": {"increment": level}}
        self.__requester.request(method="PUT", endpoint="state", data=data)

    def brightness_lower(self, level):
        """Lower the brightness of the device by a relative amount (negative raises brightness)"""
        self.brightness_raise(-level)

    @property
    def hue(self):
        """Returns the hue of the device (0-360)"""
        return self.__requester.request(method="GET", endpoint="state/hue/value")

    @hue.setter
    def hue(self, level):
        """Sets the hue to the given level (0-360)"""
        data = {"hue": {"value": level}}
        self.__requester.request(method="PUT", endpoint="state", data=data)

    @property
    def hue_min(self):
        """Returns the minimum hue possible. (This always returns 0)"""
        return self.__requester.request(method="GET", endpoint="state/hue/min")

    @property
    def hue_max(self):
        """Returns the maximum hue possible. (This always returns 360)"""
        return self.__requester.request(method="GET", endpoint="state/hue/max")

    def hue_raise(self, level):
        """Raise the hue of the device by a relative amount (negative lowers hue)"""
        data = {"hue": {"increment": level}}
        self.__requester.request(method="PUT", endpoint="state", data=data)

    def hue_lower(self, level):
        """Lower the hue of the device by a relative amount (negative raises hue)"""
        self.hue_raise(-level)

    @property
    def saturation(self):
        """Returns the saturation of the device (0-100)"""
        return self.__requester.request(method="GET", endpoint="state/sat/value")

    @saturation.setter
    def saturation(self, level):
        """Sets the saturation to the given level (0-100)"""
        data = {"sat": {"value": level}}
        self.__requester.request(method="PUT", endpoint="state", data=data)

    @property
    def saturation_min(self):
        """Returns the minimum saturation possible. (This always returns 0)"""
        self.__requester.request(method="GET", endpoint="state/sat/min")

    @property
    def saturation_max(self):
        """Returns the maximum saturation possible. (This always returns 100)"""
        self.__requester.request(method="GET", endpoint="state/sat/max")

    def saturation_raise(self, level):
        """Raise the saturation of the device by a relative amount (negative lowers saturation)"""
        data = {"sat": {"increment": level}}
        self.__requester.request(method="PUT", endpoint="state", data=data)

    def saturation_lower(self, level):
        """Lower the saturation of the device by a relative amount (negative raises saturation)"""
        self.saturation_raise(-level)

    @property
    def color_temperature(self):
        """Returns the color temperature of the device (0-100)"""
        return self.__requester.request(method="GET", endpoint="state/ct/value")

    @color_temperature.setter
    def color_temperature(self, level):
        """Sets the color temperature to the given level (0-100)"""
        data = {"ct": {"value": level}}
        self.__requester.request(method="PUT", endpoint="state", data=data)

    @property
    def color_temperature_min(self):
        """Returns the minimum color temperature possible. (This always returns 1200)"""
        return self.__requester.request(method="GET", endpoint="state/ct/min")

    @property
    def color_temperature_max(self):
        """Returns the maximum color temperature possible. (This always returns 6500)"""
        return self.__requester.request(method="GET", endpoint="state/ct/max")

    def color_temperature_raise(self, level):
        """Raise the color temperature of the device by a relative amount (negative lowers color temperature)"""
        data = {"ct": {"increment": level}}
        self.__requester.request(method="PUT", endpoint="state", data=data)

    def color_temperature_lower(self, level):
        """Lower the color temperature of the device by a relative amount (negative raises color temperature)"""
        self.color_temperature_raise(-level)

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
        self.__requester.request(method="PUT", endpoint="state", data=data)
