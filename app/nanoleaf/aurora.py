from app.nanoleaf.model import AuroraObject
from app.nanoleaf.state import State
from app.nanoleaf.rhythm import Rhythm
from app.nanoleaf.effect import Effect
from app.nanoleaf.layout import PanelLayout

from app.nanoleaf.utils import Requester


# Primary interface for an Aurora light
# For instructions or bug reports, please visit
# https://github.com/software-2/nanoleaf


class Aurora(AuroraObject):

    def __init__(self, ip_address: str = None, auth_token: str = None):
        super().__init__(Requester(ip_address, auth_token))
        self.state = State(self._requester)
        self.effect = Effect(self._requester)
        self.rhythm = Rhythm(self._requester)
        self.panel_layout = PanelLayout(self._requester, self.rhythm)

    def __repr__(self):
        return f"<Aurora({self._requester.ip_address})>"

    @property
    def info(self):
        """Returns the full Aurora Info request. 
        
        Useful for debugging since it's just a fat dump."""
        return self._requester.request(method="GET")

    def identify(self):
        """Briefly flash the panels on and off"""
        self._requester.request(method="PUT", endpoint="identify", data={})

    @property
    def firmware(self):
        """Returns the firmware version of the device"""
        return self._requester.request(method="GET")["firmwareVersion"]

    @property
    def model(self):
        """Returns the model number of the device. (Always returns 'NL22')"""
        return self._requester.request(method="GET")["model"]

    @property
    def serial_number(self):
        """Returns the serial number of the device"""
        return self._requester.request(method="GET")["serialNo"]

    def delete_user(self):
        """CAUTION: Revokes your auth token from the device."""
        self._requester.request(method="DELETE")
