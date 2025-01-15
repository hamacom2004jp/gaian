from iinfer.app.features.cli import iinfer_postprocess_det_face_store
from typing import Union, List


class ImagePostDetFaseStore(iinfer_postprocess_det_face_store.PostprocessDetFaceStore):
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
        return 'post_det_face_store'
