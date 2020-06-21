from app.nanoleaf import Aurora


class TestAurora:

    def test_info(self):
        aurora = Aurora()
        print(aurora.state.color_mode)
