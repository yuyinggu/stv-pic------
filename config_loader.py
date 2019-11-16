# -*- coding: utf-8 -*-
import os
import configparser
import logging
conf_file_path = 'downloader.conf'


class ConfLoader:
    def __init__(self):
        self.LOGGER = None
        self.set_logger()
        self.configs = self.conf_loader()

    # conf file loader
    def conf_loader(self):
        config = {}
        if os.path.exists(conf_file_path):
            config = configparser.ConfigParser()
            config.read(conf_file_path, encoding='utf8')
        else:
            self.LOGGER.error(F"{conf_file_path} not exists")
        return config

    def conf_finder(self, section, conf_name, default_val=None):
        try:
            return self.configs[section].get(conf_name, default_val)
        except Exception as e:
            self.LOGGER.error(e)

    def set_logger(self):
        LOGGER = logging.getLogger('config_loader')
        LOGGER.setLevel(logging.INFO)
        LOGFILE = 'popnews_csv.log'
        fileHandler = logging.FileHandler(LOGFILE, 'w', 'utf-8')
        LOGFORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
        fileHandler.setFormatter(LOGFORMAT)
        LOGGER.addHandler(fileHandler)
        self.LOGGER = LOGGER