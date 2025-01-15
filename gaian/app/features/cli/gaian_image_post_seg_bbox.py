from iinfer.app.features.cli import iinfer_postprocess_seg_bbox
from typing import Union, List


class ImagePostSegBbox(iinfer_postprocess_seg_bbox.PostprocessSegBbox):
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
        return 'post_seg_bbox'
