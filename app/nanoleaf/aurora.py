from app.nanoleaf import (
    Requester,
    State,
    PanelLayout,
    Effect,
    Rhythm)


# Primary interface for an Aurora light
# For instructions or bug reports, please visit
# https://github.com/software-2/nanoleaf


class AuroraObject:

    def __init__(self, requester):
        self.requester = requester


class Aurora(AuroraObject):

    def __init__(self, ip_address: str = None, auth_token: str = None):
        super().__init__(Requester(ip_address, auth_token))
        self.state = State(self.requester)
        self.panel_layout = PanelLayout(self.requester)
        self.effect = Effect(self.requester)
        self.rhythm = Rhythm(self.requester)

    def __repr__(self):
        return f"<Aurora({self.requester.ip_address})>"

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
