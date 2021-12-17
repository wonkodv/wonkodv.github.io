+++
title               = "Convert GTA Vice City  ADF files"
description         = "GTA Vice City Radio Station audio files are obfuscated MP3s. Convert them with 5 lines of python."
date                = 2023-03-12
taxonomies.category = ["Programming", "Playing"]
taxonomies.tags     = ["python"]
+++

# Convert GTA Vice City Radio station ADF audio files


On the "Game" CD of GTA Vice City is a `Audio` Directory, which contains all the radio stations as `.adf` files.
These are MP3 files "encrypted" using the sophisticated XOR algorithm with password `"` that is, `0x22`.
You can convert them to mp3 files with this python snippet.

Listening might make you nostalgic though.


```python
import pathlib
import sys

for p_from in pathlib.Path(sys.argv[1]).glob("*.adf"):
    pathlib.Path(
        sys.argv[2],
        f"GTA Vice City Radio - {p_from.stem.capitalize()}.mp3",
    ).write_bytes(bytes(b ^ 0x22 for b in p_from.read_bytes()))
```

Call as `python foo.py /mnt/Audio/ /path/to/your/music`
