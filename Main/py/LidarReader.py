from subprocess import Popen, PIPE

class LidarReader:
  def __init__(self, path):
    self.path = path
    self.name = path.replace('_llv3.out', '').replace('./bin/', '')

  def readData(self):
    self.lidar_proc = Popen([self.path], stdout=PIPE)
    return self.lidar_proc.stdout.readline().decode("utf-8").strip()

  def readName(self):
    return self.name

  def __del__(self):
    if hasattr(self, 'self.lidar_proc'):
      self.lidar_proc.kill()
