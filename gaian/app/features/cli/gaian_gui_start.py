from iinfer.app.features.cli import iinfer_gui_start
from typing import Union, List


class GuiStart(iinfer_gui_start.GuiStart):
    def get_mode(self) -> Union[str, List[str]]:
        """
        この機能のモードを返します

        Returns:
            Union[str, List[str]]: モード
        """
        return "gui"

    def get_cmd(self):
        """
        この機能のコマンドを返します

        Returns:
            str: コマンド
        """
        return 'start'
