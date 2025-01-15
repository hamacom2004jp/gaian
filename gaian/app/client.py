from cmdbox.app import client
from cmdbox.app.commons import convert
from pathlib import Path
from typing import List
import base64
import datetime
import glob
import logging
import json
import numpy as np
import time


class Client(client.Client):
    def __init__(self, logger:logging.Logger, redis_host:str = "localhost", redis_port:int = 6379, redis_password:str = None, svname:str = 'server'):
        """
        Redisサーバーとの通信を行うクラス

        Args:
            logger (logging): ロガー
            redis_host (str, optional): Redisサーバーのホスト名. Defaults to "localhost".
            redis_port (int, optional): Redisサーバーのポート番号. Defaults to 6379.
            redis_password (str, optional): Redisサーバーのパスワード. Defaults to None.
            svname (str, optional): 推論サーバーのサービス名. Defaults to 'server'.
        """
        super().__init__(logger, redis_host, redis_port, redis_password, svname)

    def faster_whisper_deploy(self,
        name:str, model_type:str, faster_whisper_model:str, faster_whisper_compute_type:str, faster_whisper_device:str, faster_whisper_beam_size:int,
        overwrite:bool, retry_count:int=3, retry_interval:int=5, timeout:int=60):
        """
        モデルをRedisサーバーにデプロイする

        Args:
            name (str): モデル名
            model_type (str): モデルタイプ
            faster_whisper_model (str): モデルの種類
            faster_whisper_compute_type (str): 計算タイプ
            faster_whisper_device (str): デバイス
            faster_whisper_beam_size (int): ビームサイズ
            overwrite (bool): モデルを上書きするかどうか
            retry_count (int, optional): リトライ回数. Defaults to 3.
            retry_interval (int, optional): リトライ間隔. Defaults to 5.
            timeout (int, optional): タイムアウト時間. Defaults to 60.

        Returns:
            dict: Redisサーバーからの応答
        """
        if name is None or name == "":
            self.logger.warning(f"name is empty.")
            return {"error": f"name is empty."}
        if model_type is None or model_type == "":
            self.logger.warning(f"model_type is empty.")
            return {"error": f"model_type is empty."}
        if faster_whisper_model is None or faster_whisper_model == "":
            self.logger.warning(f"faster_whisper_model is empty.")
            return {"error": f"faster_whisper_model is empty."}
        if faster_whisper_compute_type is None or faster_whisper_compute_type == "":
            self.logger.warning(f"faster_whisper_compute_type is empty.")
            return {"error": f"faster_whisper_compute_type is empty."}
        if faster_whisper_device is None or faster_whisper_device == "":
            self.logger.warning(f"faster_whisper_device is empty.")
            return {"error": f"faster_whisper_device is empty."}
        if faster_whisper_beam_size is None or faster_whisper_beam_size == "":
            self.logger.warning(f"faster_whisper_beam_size is empty.")
            return {"error": f"faster_whisper_beam_size is empty."}

        res_json = self.redis_cli.send_cmd('faster_whisper_deploy',
            [name, model_type, faster_whisper_model, faster_whisper_compute_type, faster_whisper_device, str(faster_whisper_beam_size), overwrite],
            retry_count=retry_count, retry_interval=retry_interval, outstatus=False, timeout=timeout)

        return res_json

    def faster_whisper_undeploy(self, name:str, retry_count:int=3, retry_interval:int=5, timeout:int = 60):
        """
        モデルをRedisサーバーからアンデプロイする

        Args:
            name (str): モデル名
            retry_count (int, optional): リトライ回数. Defaults to 3.
            retry_interval (int, optional): リトライ間隔. Defaults to 5.
            timeout (int, optional): タイムアウト時間. Defaults to 60.

        Returns:
            dict: Redisサーバーからの応答
        """
        if name is None or name == "":
            self.logger.warning(f"name is empty.")
            return {"error": f"name is empty."}
        res_json = self.redis_cli.send_cmd('undeploy', [name],
                                           retry_count=retry_count, retry_interval=retry_interval, timeout=timeout)
        return res_json

    def faster_whisper_start(self, name:str, model_provider:str = 'CPUExecutionProvider', use_track:bool=False, gpuid:int=None,
              retry_count:int=3, retry_interval:int=5, timeout:int = 60):
        """
        モデルをRedisサーバーで起動する

        Args:
            name (str): モデル名
            model_provider (str, optional): 推論実行時のモデルプロバイダー。デフォルトは'CPUExecutionProvider'。
            use_track (bool): Multi Object Trackerを使用するかどうか, by default False
            gpuid (int): GPU ID, by default None
            retry_count (int, optional): リトライ回数. Defaults to 3.
            retry_interval (int, optional): リトライ間隔. Defaults to 5.
            timeout (int, optional): タイムアウト時間. Defaults to 60.

        Returns:
            dict: Redisサーバーからの応答
        """
        if name is None or name == "":
            self.logger.warning(f"name is empty.")
            return {"error": f"name is empty."}
        if model_provider is None or model_provider == "":
            self.logger.warning(f"model_provider is empty.")
            return {"error": f"model_provider is empty."}
        res_json = self.redis_cli.send_cmd('start', [name, model_provider, str(use_track), str(gpuid)],
                                           retry_count=retry_count, retry_interval=retry_interval, timeout=timeout)
        return res_json

    def faster_whisper_stop(self, name:str,
             retry_count:int=3, retry_interval:int=5, timeout:int = 60):
        """
        モデルをRedisサーバーで停止する

        Args:
            name (str): モデル名
            retry_count (int, optional): リトライ回数. Defaults to 3.
            retry_interval (int, optional): リトライ間隔. Defaults to 5.
            timeout (int, optional): タイムアウト時間. Defaults to 60.

        Returns:
            dict: Redisサーバーからの応答
        """
        if name is None or name == "":
            self.logger.warning(f"name is empty.")
            return {"error": f"name is empty."}
        res_json = self.redis_cli.send_cmd('stop', [name],
                                           retry_count=retry_count, retry_interval=retry_interval, timeout=timeout)
        return res_json
