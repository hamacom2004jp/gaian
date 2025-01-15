from iinfer.app.features.cli import iinfer_install_insightface
from typing import Union, List


class ImageInstallFace(iinfer_install_insightface.InstallInsightface):
    def get_mode(self) -> Union[str, List[str]]:
        """
        この機能のモードを返します

        Returns:
            Union[str, List[str]]: モード
        """
        return "image"

    def get_cmd(self):
        """
        この機能のコマンドを返します

        Returns:
            str: コマンド
        """
        return 'install_face'
