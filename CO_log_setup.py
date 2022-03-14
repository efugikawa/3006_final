# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 13:21:11 2022

@author: bkmcc, ebf
"""
import logging


class Logger_FP_BE:
    def __init__(self, verbose=False):
        self.__log_config(verbose=verbose)

    def debug(self, errMsg):
        logging.debug(errMsg)

    def info(self, errMsg):
        logging.info(errMsg)

    def __log_config(self, verbose=False):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)  # i.e. everything
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s:%(relativeCreated)d:%(message)s')

        # change fileName to variable

        fh = logging.FileHandler("precip_crime_logs.log", 'w')
        fh.setLevel(logging.DEBUG)  # everything prints to log file
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        sh = logging.StreamHandler()
        if verbose:
            sh.setLevel(logging.DEBUG)
        else:
            sh.setLevel(logging.INFO)

        logger.addHandler(sh)
