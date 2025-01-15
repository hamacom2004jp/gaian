from cmdbox.app import client, common, feature
from cmdbox.app.commons import redis_client
from pathlib import Path
from typing import Dict, Any, Tuple, Union, List
import argparse
import logging
import json


class VoiceDeploy(feature.Feature):
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
        return 'deploy'

    def get_option(self):
        """
        この機能のオプションを返します

        Returns:
            Dict[str, Any]: オプション
        """
        return dict(
            type="str", default=None, required=False, multi=False, hide=False, use_redis=self.USE_REDIS_FALSE,
            discription_ja="音声を操作するモジュールを配備します。",
            discription_en="Deploy a module to control the voice.",
            choice=[
                dict(opt="host", type="str", default=self.default_host, required=True, multi=False, hide=True, choice=None,
                     discription_ja="Redisサーバーのサービスホストを指定します。",
                     discription_en="Specify the service host of the Redis server.",),
                dict(opt="port", type="int", default=self.default_port, required=True, multi=False, hide=True, choice=None,
                     discription_ja="Redisサーバーのサービスポートを指定します。",
                     discription_en="Specify the service port of the Redis server.",),
                dict(opt="password", type="str", default=self.default_pass, required=True, multi=False, hide=True, choice=None,
                     discription_ja="Redisサーバーのアクセスパスワード(任意)を指定します。省略時は `password` を使用します。",
                     discription_en="Specify the access password of the Redis server (optional). If omitted, `password` is used.",),
                dict(opt="svname", type="str", default="server", required=True, multi=False, hide=True, choice=None,
                     discription_ja="推論サーバーのサービス名を指定します。省略時は `server` を使用します。",
                     discription_en="Specify the service name of the inference server. If omitted, `server` is used.",),
                dict(opt="name", type="str", default="", required=True, multi=False, hide=False, choice=None,
                     discription_ja="AIモデルの登録名を指定します。",
                     discription_en="Specifies the registration name of the AI model.",),
                dict(opt="model_type", type="str", default="faster_whisper", required=True, multi=False, hide=False, choice=["faster_whisper"],
                     discription_ja="音声のテキスト生成モデルの種類を指定します。",
                     discription_en="Specifies the type of text generation model for speech.",
                     choice_show={"faster_whisper":[
                         "faster_whisper_model",
                         "faster_whisper_compute_type",
                         "faster_whisper_device",
                         "faster_whisper_beam_size"]},),
                dict(opt="faster_whisper_model", type="str", default="distil-large-v3", required=False, multi=False, hide=False,
                     choice=["distil-large-v3","large-v3","large-v2","large-v1","medium","base","small","tiny","medium.en","base.en","small.en","tiny.en"],
                     discription_ja="faster_whisperのモデルを指定します。",
                     discription_en="Specifies the model of FASTER_WHISPER."),
                dict(opt="faster_whisper_compute_type", type="str", default="int8_float16", required=False, multi=False, hide=False,
                     choice=["float16","int8_float16","int8"],
                     discription_ja="faster_whisperのモデルを指定します。",
                     discription_en="Specifies the model of FASTER_WHISPER."),
                dict(opt="faster_whisper_device", type="str", default="cuda", required=False, multi=False, hide=False, choice=["cuda","cpu"],
                     discription_ja="faster_whisperのディバイスを指定します。",
                     discription_en="Specify the divice of FASTER_WHISPER."),
                dict(opt="faster_whisper_beam_size", type="int", default=5, required=False, multi=False, hide=False, choice=None,
                     discription_ja="faster_whisperのbeam_sizeを指定します。",
                     discription_en="Specify the beam_size of FASTER_WHISPER."),
                dict(opt="retry_count", type="int", default=3, required=False, multi=False, hide=True, choice=None,
                     discription_ja="Redisサーバーへの再接続回数を指定します。0以下を指定すると永遠に再接続を行います。",
                     discription_en="Specifies the number of reconnections to the Redis server.If less than 0 is specified, reconnection is forever.",),
                dict(opt="retry_interval", type="int", default=5, required=False, multi=False, hide=True, choice=None,
                     discription_ja="Redisサーバーに再接続までの秒数を指定します。",
                     discription_en="Specifies the number of seconds before reconnecting to the Redis server.",),
                dict(opt="timeout", type="int", default=120, required=False, multi=False, hide=False, choice=None,
                     discription_ja="サーバーの応答が返ってくるまでの最大待ち時間を指定。",
                     discription_en="Specify the maximum waiting time until the server responds.",),
                dict(opt="output_json", short="o", type="file", default="", required=False, multi=False, hide=True, choice=None, fileio="out",
                     discription_ja="処理結果jsonの保存先ファイルを指定。",
                     discription_en="Specify the destination file for saving the processing result json.",),
                dict(opt="output_json_append", short="a", type="bool", default=False, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="処理結果jsonファイルを追記保存します。",
                     discription_en="Save the processing result json file by appending.",),
                dict(opt="stdout_log", type="bool", default=True, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力をConsole logに出力します。",
                     discription_en="Available only in GUI mode. Outputs standard output during command execution to Console log."),
                dict(opt="capture_stdout", type="bool", default=True, required=False, multi=False, hide=True, choice=[True, False],
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力をキャプチャーし、実行結果画面に表示します。",
                     discription_en="Available only in GUI mode. Captures standard output during command execution and displays it on the execution result screen."),
                dict(opt="capture_maxsize", type="int", default=self.DEFAULT_CAPTURE_MAXSIZE, required=False, multi=False, hide=True, choice=None,
                     discription_ja="GUIモードでのみ使用可能です。コマンド実行時の標準出力の最大キャプチャーサイズを指定します。",
                     discription_en="Available only in GUI mode. Specifies the maximum capture size of standard output when executing commands."),
            ])

    def apprun(self, logger:logging.Logger, args:argparse.Namespace, tm:float, pf:List[Dict[str, float]]=[]) -> Tuple[int, Dict[str, Any], Any]:
        """
        この機能の実行を行います

        Args:
            logger (logging.Logger): ロガー
            args (argparse.Namespace): 引数
            tm (float): 実行開始時間
            pf (List[Dict[str, float]]): 呼出元のパフォーマンス情報

        Returns:
            Tuple[int, Dict[str, Any], Any]: 終了コード, 結果, オブジェクト
        """
        if args.svname is None:
            msg = {"warn":f"Please specify the --svname option."}
            common.print_format(msg, args.format, tm, args.output_json, args.output_json_append, pf=pf)
            return 1, msg, None
        cl = client.Client(logger, redis_host=args.host, redis_port=args.port, redis_password=args.password, svname=args.svname)

        if args.model_type == "faster_whisper":
            if args.name is None or args.name == "":
                self.logger.warning(f"name is empty.")
                return {"error": f"name is empty."}
            if args.model_type is None or args.model_type == "":
                self.logger.warning(f"model_type is empty.")
                return {"error": f"model_type is empty."}
            if args.faster_whisper_model is None or args.faster_whisper_model == "":
                self.logger.warning(f"faster_whisper_model is empty.")
                return {"error": f"faster_whisper_model is empty."}
            if args.faster_whisper_compute_type is None or args.faster_whisper_compute_type == "":
                self.logger.warning(f"faster_whisper_compute_type is empty.")
                return {"error": f"faster_whisper_compute_type is empty."}
            if args.faster_whisper_device is None or args.faster_whisper_device == "":
                self.logger.warning(f"faster_whisper_device is empty.")
                return {"error": f"faster_whisper_device is empty."}
            if args.faster_whisper_beam_size is None or args.faster_whisper_beam_size == "":
                self.logger.warning(f"faster_whisper_beam_size is empty.")
                return {"error": f"faster_whisper_beam_size is empty."}

            ret = cl.redis_cli.send_cmd('faster_whisper_deploy', [args.name, args.model_type,
                args.faster_whisper_model, args.faster_whisper_compute_type, args.faster_whisper_device, str(args.faster_whisper_beam_size), str(args.overwrite)],
                retry_count=args.retry_count, retry_interval=args.retry_interval, outstatus=False, timeout=args.timeout)

        else:
            ret = {"warn":f"model_type={args.model_type} is not supported."}
            logger.warn(f"model_type={args.model_type} is not supported.")
        common.print_format(ret, args.format, tm, args.output_json, args.output_json_append, pf=pf)
        if 'success' not in ret:
            return 1, ret, cl

        return 0, ret, cl

    def is_cluster_redirect(self):
        """
        クラスター宛のメッセージの場合、メッセージを転送するかどうかを返します

        Returns:
            bool: メッセージを転送する場合はTrue
        """
        return True

    def get_svcmd(self):
        """
        この機能のサーバー側のコマンドを返します

        Returns:
            str: サーバー側のコマンド
        """
        return "faster_whisper_deploy"

    def svrun(self, data_dir:Path, logger:logging.Logger, redis_cli:redis_client.RedisClient, msg:List[str],
              sessions:Dict[str, Dict[str, Any]]) -> int:
        """
        この機能のサーバー側の実行を行います

        Args:
            data_dir (Path): データディレクトリ
            logger (logging.Logger): ロガー
            redis_cli (redis_client.RedisClient): Redisクライアント
            msg (List[str]): 受信メッセージ
            sessions (Dict[str, Dict[str, Any]]): セッション情報
        
        Returns:
            int: 終了コード
        """
        if len(msg) < 8:
            logger.error(f"Invalid message: {msg}")
            return self.RESP_WARN
        if msg[7] == "None":
            faster_whisper_beam_size = None
        else:
            faster_whisper_beam_size = int(msg[7])
        if msg[8] == "None":
            overwrite = False
        else:
            overwrite = bool(msg[8])

        st = self.faster_whisper_deploy(msg[1], msg[2], msg[3], msg[4], msg[5], msg[6], faster_whisper_beam_size, overwrite,
                                        data_dir, logger, redis_cli, sessions)
        return st

    def faster_whisper_deploy(self, reskey:str, name:str, model_type:str,
        faster_whisper_model:str, faster_whisper_compute_type:str, faster_whisper_device:str, faster_whisper_beam_size:int, overwrite:bool,
        data_dir:Path, logger:logging.Logger, redis_cli:redis_client.RedisClient, sessions:Dict[str, Dict[str, Any]]) -> int:
        """
        faster_whisperモデルをサーバーにデプロイする

        Args:
            reskey (str): 結果キー
            name (str): モデル名
            model_type (str): モデルの種類
            faster_whisper_model (str): モデルの種類
            faster_whisper_compute_type (str): 計算タイプ
            faster_whisper_device (str): デバイス
            faster_whisper_beam_size (int): ビームサイズ
            overwrite (bool): モデルを上書きするかどうか
            data_dir (Path): データディレクトリ
            logger (logging.Logger): ロガー
            redis_cli (redis_client.RedisClient): Redisクライアント
            sessions (Dict[str, Dict[str, Any]]): セッション情報

        Returns:
            int: 終了コード
        """
        if name is None or name == "":
            logger.warning(f"Name is empty.")
            redis_cli.rpush(reskey, {"warn": f"Name is empty."})
            return self.RESP_WARN
        if model_type is None or model_type == "":
            logger.warning(f"model_type is empty.")
            redis_cli.rpush(reskey, {"warn": f"model_type is empty."})
            return self.RESP_WARN
        if faster_whisper_model is None or faster_whisper_model == "":
            logger.warning(f"faster_whisper_model is empty.")
            redis_cli.rpush(reskey, {"warn": f"faster_whisper_model is empty."})
            return self.RESP_WARN
        if faster_whisper_compute_type is None or faster_whisper_compute_type == "":
            logger.warning(f"faster_whisper_compute_type is empty.")
            redis_cli.rpush(reskey, {"warn": f"faster_whisper_compute_type is empty."})
            return self.RESP_WARN
        if faster_whisper_device is None or faster_whisper_device == "":
            logger.warning(f"faster_whisper_device is empty.")
            redis_cli.rpush(reskey, {"warn": f"faster_whisper_device is empty."})
            return self.RESP_WARN
        if faster_whisper_beam_size is None or faster_whisper_beam_size == "":
            logger.warning(f"faster_whisper_beam_size is empty.")
            redis_cli.rpush(reskey, {"warn": f"faster_whisper_beam_size is empty."})
            return self.RESP_WARN

        deploy_dir = data_dir / name
        if name in sessions:
            logger.warning(f"{name} has already started a session.")
            redis_cli.rpush(reskey, {"warn": f"{name} has already started a session."})
            return self.RESP_WARN
        if not overwrite and deploy_dir.exists():
            logger.warning(f"Could not be deployed. '{deploy_dir}' already exists")
            redis_cli.rpush(reskey, {"warn": f"Could not be deployed. '{deploy_dir}' already exists"})
            return self.RESP_WARN

        common.mkdirs(deploy_dir)

        with open(deploy_dir / "conf.json", "w") as f:
            conf = dict(model_type=model_type,
                        faster_whisper_model=faster_whisper_model,
                        faster_whisper_compute_type=faster_whisper_compute_type,
                        faster_whisper_device=faster_whisper_device,
                        faster_whisper_beam_size=faster_whisper_beam_size,
                        deploy_dir=deploy_dir)
            json.dump(conf, f, default=common.default_json_enc, indent=4)
            logger.info(f"Save conf.json to {str(deploy_dir)}")

        redis_cli.rpush(reskey, {"success": f"Save conf.json to {str(deploy_dir)}"})
        return self.RESP_SCCESS
