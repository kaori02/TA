# - Init condition:
#   - 2 LiDAR tersambung, 1 LiDAR nyambung ke pin tertentu dengan kabel orange.
# - Matiin dlu si LiDAR via kabel orange.
# - Set alamat buat yg ga pake kabel orange ke `0x44`. RUN LiDAR ini
# - Turn on lagi kabel orange (dia bakal pake addr default `0x62`). RUN
# - Ambil data dari kedua LiDAR sekaligus algonya pake script py
# - Done

import subprocess

list_files = subprocess.run(["ls", "-l"])
print("The exit code was: %d" % list_files.returncode)