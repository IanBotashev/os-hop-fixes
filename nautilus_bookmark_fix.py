#!/usr/bin/env python3
import argparse
import os
import pwd
import shutil


def main(args):
    """
    Entrypoint
    :param args: Args given
    :return: None
    """
    if args.backup:
        files_backedup = backup_files(args.files)
        print("Backup completed. In case of unsuccessful completion, the following files were created:")
        for file in files_backedup:
            print("    " + file)
    else:
        input("Please backup the following files:\n    " + '\n    '.join(args.files) + "\nthen press enter...")

    print("Applying fix...")
    apply_fix(args.files)

    # If we have a backup, and we're supposed to remove it, remove it.
    if args.remove and args.backup:
        print("Removing backup files...")
        remove_backup(files_backedup)
        print("Done.")

    print("Files edited, to finalize changes log out then back in.")


def backup_files(files):
    """
    Automatically backup files given to us in the same directory as the given files
    :param files: Files to create backups of
    :return: List of files backed up
    """
    files_backedup = []
    for file in files:
        files_backedup.append(file + ".backup")
        shutil.copy(file, file + ".backup")

    return files_backedup


def remove_backup(files):
    """
    Removes backup we created
    :param files: Files that we edited
    :return: None
    """
    for file in files:
        os.remove(file)


def apply_fix(files):
    """
    Applies the fix
    :param files:
    :return:
    """
    verify_files_exist(files)
    for file in files:
        print(f"    Editing {file}")
        with open(file, "r+") as f:
            data = f.readlines()
            f.seek(0)  # Go back to start of file
            f.truncate(0)  # Blank out file

            # Comment out any lines
            for line in data:
                if not line.strip().startswith("#"):
                    line = "# " + line

                f.write(line)


def verify_files_exist(files):
    """
    Makes sure that all of the passed-in files actually exist in the filesystem.
    :param files: Files to check over
    :return: None, raises FileNotFoundError if file does not exist
    """
    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} does not exist")


def get_original_user_home():
    """
    :return: Path to the home folder of the user who ran sudo
    """
    # Check if the script is run with sudo
    sudo_user = os.environ.get('SUDO_USER')
    if sudo_user:
        # Get the home directory of the user who invoked sudo
        user_home = pwd.getpwnam(sudo_user).pw_dir
    else:
        # Fallback to the current user's home directory if not run with sudo
        user_home = os.environ.get('HOME')
    return user_home


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Removes default Nautilus bookmarks.')
    parser.add_argument('-f',
                        '--files',
                        nargs="+",
                        default=[get_original_user_home() + '/.config/user-dirs.dirs', '/etc/xdg/user-dirs.defaults'],
                        help='The files that this tool will edit. Default values should work.')

    # Argparse has really counterintuitive action names...
    parser.add_argument('-b',
                        '--backup',
                        action='store_false',
                        help="Backs up files beforehand in the same directory, appending .backup extension. Default true.")
    parser.add_argument('-r',
                        '--remove',
                        action='store_false',
                        help="Remove backups on successful execution. Default true.")
    args = parser.parse_args()
    main(args)
