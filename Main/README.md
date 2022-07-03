# Main

This is the directory where you want to run the program.

## Prerequisite

- Install **Olympe** (check out [this](https://forum.developer.parrot.com/t/olympe-1-01-on-raspberry-pi-zero-and-pi3-a/9487) or [this](https://gist.github.com/prolifel/6df88190a51a48787efda767515b3267#file-olympe-md) to know how)

- Callibrate the compass
- Setup bluetooth in raspi. You can use [this](https://howchoo.com/pi/bluetooth-raspberry-pi#setting-up-bluetooth-using-a-terminal-or-ssh-connection).
- Install Pybluez
- Use [this](https://stackoverflow.com/questions/36675931/bluetooth-btcommon-bluetootherror-2-no-such-file-or-directory) to prevent `bluetooth.btcommon.BluetoothError: (2, 'No such file or directory')` error
- Use [this](https://stackoverflow.com/questions/34599703/rfcomm-bluetooth-permission-denied-error-raspberry-pi) to prevent rfcomm bluetooth permission denied error raspberry pi

## How To Run

- Setup bluetooth
  ```sh
  sudo bluetoothctl
  ```
  then
  ```sh
  [bluetooth] discoverable on
  [bluetooth] pairable on
  [bluetooth] agent on
  [bluetooth] default-agent
  ```
- Connect your phone to raspi
  
- Make sure that `Main` directory is your current working directory before running this program.

  ```sh
  > source ~/parrot-groundsdk/products/olympe/linux/env/shell
  > chmod +x make_all.sh
  > chmod +x make_run.sh
  > ./make_all.sh
  > python3 py/Main.py
  ```
- Get location via android app

## Testing Checklist
- [ ] Callibrate compass
- [ ] Input loc
- [ ] Check LiDAR
- [ ] Change wifi to connect to drone
- [ ] Test vincenty      (3 times)
- [ ] Test obs_avo CLEAR (3 times)
- [ ] Test obs_avo FRONT (3 times)
- [ ] Test obs_avo RIGHT (3 times)
- [ ] Test obs_avo LEFT  (3 times)