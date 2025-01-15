from cmdbox.app import app
from gaian import version


def main(args_list:list=None):
    _app = app.CmdBoxApp.getInstance(appcls=GaianApp, ver=version)
    return _app.main(args_list)[0]

class GaianApp(app.CmdBoxApp):
    pass