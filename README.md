# GoPro Fixer
© 2025 Simon Fredsted

## Purpose

Due to filesystem limitations, long-running GoPro video camera recordings are split up in approximately 4 GB files. Managing these files is annoying and cumbersome. Therefore this script was created to easily merge these video file sequences into 1 file per sequence.

## How it works

GoPro Fixer uses `ffmpeg` to merge all video files in a specific folder.

For example, in a folder with the following GoPro mp4s (2 sequences with 3 and 2 files, respectively):

* GX010102.MP4
* GX020102.MP4
* GX030102.MP4
* GX010103.MP4
* GX020103.MP4

The following files are created:

* 0102.mp4
* 0103.mp4

Additionally, the file modification date of the *first* file in the sequence is copied to the new file.

## Requirements

* Python 3
* ffmpeg

## How to use

You can either run the program from the terminal or, if you're running macOS, double-click the `goprofixer.command` file - it will automatically show a folder selection dialog. 

### Run in terminal

```bash
python3 goprofixer.py <path>
```

### macOS

Before starting, install ffmpeg ([installation guide](https://phoenixnap.com/kb/ffmpeg-mac)).

1) Download the repository: [goprofixer.zip](https://github.com/fredsted/goprofixer/archive/refs/heads/main.zip)
2) Double-click the `goprofixer.command` file. (You might need to use Ctrl-Click -> Run)
3) Select the directory containing GoPro mp4 files