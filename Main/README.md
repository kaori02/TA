# Main (One LiDAR Usage)

This is the directory where you want to run the porgram.

## Prerequisite

- **Olympe** installed (check out [this](https://forum.developer.parrot.com/t/olympe-1-01-on-raspberry-pi-zero-and-pi3-a/9487) or [this](https://gist.github.com/prolifel/6df88190a51a48787efda767515b3267#file-olympe-md) to know how)

- Callibrate the compass
## How To Run

Make sure that `Main` directory is your current working directory before running this program.

```sh
> source ~/parrot-groundsdk/products/olympe/linux/env/shell
> make
> python3 py/Main.py
```

## Testing Checklist
- [ ] Callibrate compass
- [ ] Input loc
- [ ] Check LiDAR
- [ ] Change wifi to connect to drone
- [ ] [ ] [ ] Test vincenty      (3 times)
- [ ] [ ] [ ] Test obs_avo CLEAR (3 times)
- [ ] [ ] [ ] Test obs_avo FRONT (3 times)
- [ ] [ ] [ ] Test obs_avo RIGHT (3 times)
- [ ] [ ] [ ] Test obs_avo LEFT  (3 times)