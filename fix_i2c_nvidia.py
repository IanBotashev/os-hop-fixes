#!/usr/bin/env python3

# There's an error with certain nvidia drivers which attempt to load the i2c driver without a USB-c interface on the
# card. This script follows the fix on this askubuntu thread:
# https://askubuntu.com/questions/1278399/dual-system-ubuntu-20-04nvidia-gpu-i2c-timeout-error-ucsi-ccg-i2c-transfer
import argparse
import os
import subprocess


def main(args):
    """
    Entrypoint
    """
    # Do a before-hand check for root privileges incase of -u flag being set, to not edit files unnecessarily and error out.
    # Could be a bit panicky for someone, especially considering we're essentially messing w/ drivers.
    if args.update and not is_root():
        raise PermissionError("Update flag is set but we don't have permission to update initramfs, exiting. No files were edited.")

    if is_already_applied(args.file, args.contents) and not args.force:
        print("Fix has already been applied. To force reapplication, use --force flag.")
        exit()

    print("Applying...")
    apply_fix(args.file, args.contents)
    if args.update:
        print("File created, attempting to run update-initramfs...")
        update_initramfs()
        print("Finished.")
    else:
        print("Finished. To finalize, run 'sudo update-initramfs -u'")


def apply_fix(file, contents):
    """
    Creates a file with specified contents
    :param file: Path to file
    :param contents: Contents to populate file with
    :return: None
    """
    with open(file, "w") as f:
        f.write(contents)


def update_initramfs():
    """
    Attempts to run update-initramfs -u
    If an error occurs, prints it
    :return: None
    """
    try:
        subprocess.check_call(["update-initramfs", "-u"])
        print("Successfully updated initramfs.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating initramfs: {e}")


def is_root():
    """
    Checks if the current user is root.
    :return:
    """
    return os.geteuid() == 0


def is_already_applied(file, contents):
    """
    Checks if the fix has already been applied.
    :param file: File to check
    :param contents: What the contents of the file should be
    :return: bool
    """
    try:
        with open(file, 'r') as f:
            return f.read() == contents
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fixes i2c timeout error')
    parser.add_argument('-f',
                        '--file',
                        default="/etc/modprobe.d/blacklist_i2c-nvidia-gpu.conf",
                        help='File to create')
    parser.add_argument('-c',
                        '--contents',
                        default="blacklist i2c_nvidia_gpu",
                        help='Contents to fill the created file with')
    parser.add_argument('-u',
                        '--update',
                        action="store_true",
                        help='Attempts to update the initramfs image automatically. Requires root privileges. Default true')
    parser.add_argument('--force',
                        action="store_true",
                        help='Forces reapplication of the fix even if already applied.')
    args = parser.parse_args()
    main(args)
