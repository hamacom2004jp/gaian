from iinfer.app.features.cli import iinfer_client_undeploy
from typing import Dict, Any, Tuple, Union, List


class VoiceUndeploy(iinfer_client_undeploy.ClientUndeploy):
    def get_mode(self) -> Union[str, List[str]]:
        """
        この機能のモードを返します

        Returns:
            Union[str, List[str]]: モード
        """
        return "voice"

    def get_cmd(self):
        """
        この機能のコマンドを返します

        Returns:
            str: コマンド
        """
        return 'undeploy'
