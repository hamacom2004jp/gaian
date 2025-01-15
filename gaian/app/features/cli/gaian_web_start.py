from iinfer.app.features.cli import iinfer_web_start
from typing import Union, List


class WebStart(iinfer_web_start.WebStart):
    def get_mode(self) -> Union[str, List[str]]:
        """
        この機能のモードを返します

        Returns:
            Union[str, List[str]]: モード
        """
        return "web"

    def get_cmd(self):
        """
        この機能のコマンドを返します

        Returns:
            str: コマンド
        """
        return 'start'
