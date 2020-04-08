
import os
import logging
from datetime import date,time
from logging.handlers import TimedRotatingFileHandler

class DvalLogger:

   __today = date.today()
   __log_directory = None
   __instance = None
   __logger = None

   @staticmethod
   def get_instance():
       if DvalLogger.__instance is None:
           DvalLogger.__instance = DvalLogger()
       return DvalLogger.__instance


   def initialise_logging(self,log_directory):
       self.__log_directory = log_directory
       try:
           os.makedirs(self.__log_directory)
       except FileExistsError:
           pass

       logname = os.path.join(log_directory,"e-KYC.log")

       self.__logger = logging.getLogger()
       self.__logger.setLevel(logging.DEBUG)
       logFormatter = logging.Formatter("%(asctime)s %(message)s")
       fileHandler = TimedRotatingFileHandler(logname,when="midnight", interval=1)
       # "{0}/{1}.log".format(self.__log_directory, 'query_extraction' +'_'+ str(date.today())+'.log')
       fileHandler.suffix = "%Y%m%d"
       fileHandler.setFormatter(logFormatter)
       self.__logger.addHandler(fileHandler)




   def log(self,message:str, log_level=logging.DEBUG):
       if log_level == logging.DEBUG:
           self.__logger.debug(message)
       if log_level == logging.WARNING:
           self.__logger.warning(message)
       if log_level == logging.INFO:
           self.__logger.info(message)
       if log_level == logging.ERROR:
           self.__logger.error(message)