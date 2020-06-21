from app.nanoleaf import AuroraObject


class PanelLayout(AuroraObject):

    def __init__(self, requester, rhythm):
        super().__init__(requester)
        self.rhythm = rhythm

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
        if self.rhythm.rhythm_connected:
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