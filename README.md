# Compressed ramdisk unpack tool

![License](https://img.shields.io/github/license/Mashopy/android-unpack-ramdisk)
![GitHub Issues](https://img.shields.io/github/issues-raw/Mashopy/android-unpack-ramdisk?color=red)

## Description

* `unpack-ramdisk.py`: Script designed to extract the content of compressed ramdisk files present in Android boot/init_boot/recovery/vendor_boot images extracted with AOSP `unpack_bootimg.py` tool.

## Dependencies

To run the script, you will need to have `python-magic` package installed.

## Usage
Just run `python unpack-ramdisk.py` where your compressed ramdisk at. It will extract anything that have `ramdisk` in it's name.
If you want to run the script but your compressed ramdisk is on a different directory, specify the path at the end.

Right now, the script only support GZIP, LZ4, LZMA, LZOP and XZ compressed ramdisk files.

## License
This project is licensed under the GPL-3.0 License - see the [LICENSE](https://github.com/Mashopy/android-unpack-ramdisk/tree/main/LICENSE) file for details.
