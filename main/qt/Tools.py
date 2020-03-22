import configparser
import logging
import os

import main.qt.Vars as mVars


class CTools(object):

    def __init__(self, logger_name, file_path):
        self.logger = CTools.setLogger(logger_name, file_path)

    @staticmethod
    def isEmpty(obj):
        return obj is None

    @staticmethod
    def readConfig(path):
        config = configparser.ConfigParser()
        path = str(path) if not CTools.isEmpty(path) and str(path).endswith(".ini") else '../resources/config.ini'
        config.read(path, 'utf8')
        mVars.host = config.get('datasource', 'host')
        mVars.database_name = config.get('datasource', 'database_name')
        mVars.username = config.get('datasource', 'username')
        mVars.password = config.get('datasource', 'password')

    @staticmethod
    def setLogger(logger_name, file_path):
        # 创建一个logger,可以考虑如何将它封装
        logger = logging.getLogger(logger_name or 'myLogger')
        logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(os.path.join(os.getcwd(), file_path or './logs/info.log'), encoding='utf8')
        fh.setLevel(logging.DEBUG)
        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        # 记录一条日志
        return logger

    def delBlank(self, srcStr):
        return srcStr.strip()

    def decorator(print_debug=True, *args):
        def inner1(f, *args):
            def inner2(*args, **kwargs):
                try:
                    res = f(*args, **kwargs)
                except Exception as err:
                    if print_debug:
                        import sys  # 这里导入模块是为了方便直接复制使用，现实中这个应该放到文件头部
                        info = sys.exc_info()[2].tb_frame.f_back
                        temp = "filename:{}\nlines:{}\tfuncation:{}\terror:{}"
                        cTool.logger.info(temp.format(info.f_code.co_filename, info.f_lineno, f.__name__, repr(err)))
                    res = None
                return res

            return inner2

        return inner1


cTool = CTools(None, None)
