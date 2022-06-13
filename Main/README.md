# Main

This is the directory where you want to run the porgram.

## Prerequisite
- **Olympe** installed (check out [this link](https://forum.developer.parrot.com/t/olympe-1-01-on-raspberry-pi-zero-and-pi3-a/9487) or [this link](https://gist.github.com/prolifel/6df88190a51a48787efda767515b3267#file-olympe-md) to know how)

## How To Run

Make sure that `Main` directory is your current working directory before running this program.

```sh
$ source ~/parrot-groundsdk/products/olympe/linux/env/shell
$ chmod +x make_all.sh
$ ./make_all.sh
$ python3 py/Main.py
```