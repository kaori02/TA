import logging

class Log:
  def __init__(self):
    self.logger = logging.getLogger("ObstacleAvoidanceLog")
    self.logger.setLevel(level=logging.DEBUG)

    self.ch = logging.StreamHandler()
    self.fh = logging.FileHandler("ObstacleAvoidanceLog.log")

    # self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
    self.formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')

    self.ch.setFormatter(self.formatter)
    self.fh.setFormatter(self.formatter)

    self.logger.addHandler(self.ch)
    self.logger.addHandler(self.fh)

  def debug(self, message):
    self.logger.debug(message)

  def info(self, message):
    self.logger.info(message)  
  
  def warning(self, message):
    self.logger.warning(message)

  def error(self, message):
    self.logger.error(message)

  def critical(self, message):
    self.logger.critical(message)