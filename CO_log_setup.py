# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 13:21:11 2022

@author: bkmcc
"""
import logging


class Logger_FP_BE:
    def __init__(self):
        self.__log_config()

    def debug(self, errMsg):
        logging.debug(errMsg)

    def info(self, errMsg):
        logging.info(errMsg)

    def __log_config(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)  # i.e. everything
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(relativeCreated)d:%(message)s')

        fh = logging.FileHandler("precip_crime_logs.log", 'w')
        fh.setLevel(logging.DEBUG)  # everything prints to log file
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)  # only INFO and greater print to console
        logger.addHandler(sh)
