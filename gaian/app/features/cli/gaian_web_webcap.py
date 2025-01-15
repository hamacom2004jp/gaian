from iinfer.app.features.cli import iinfer_web_webcap
from typing import Union, List


class WebWebcap(iinfer_web_webcap.WebWebcap):
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
        return 'webcap'
