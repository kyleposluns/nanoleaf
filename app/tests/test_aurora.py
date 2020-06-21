from app.nanoleaf import Aurora


class TestAurora:

    def test_info(self):
        aurora = Aurora()
        aurora.state.brightness = -1
        print(aurora.state.brightness)
