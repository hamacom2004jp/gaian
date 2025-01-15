from gaian import version
from iinfer.app.features.web import iinfer_web_gui


class Gui(iinfer_web_gui.Gui):
    def __init__(self, appcls, ver):
        super().__init__(appcls=appcls, ver=ver)
        self.version_info.append(dict(tabid='versions_gaian', title=version.__appid__,
                                      icon=f'assets/gaian/icon.png', url='versions_gaian'))
