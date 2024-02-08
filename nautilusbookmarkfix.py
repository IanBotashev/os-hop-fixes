import argparse
import os


def main(files):
    """
    Meat and potatoes for this utility
    :param files:
    :return:
    """
    assert_files_exist(files)
    for file in files:
        with open(file, "r") as f:
            data = f.readlines()

        with open(file, "w") as f:
            for line in data:
                if not line.strip().startswith("#"):
                    line = "# " + line

                f.write(line)


def assert_files_exist(files):
    """
    Makes sure that all of the passed-in files actually exist in the filesystem.
    :param files:
    :return:
    """
    for file in files:
        if not os.path.exists(file):
            raise FileNotFoundError(f"{file} does not exist")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Removes default Nautilus bookmarks.')
    parser.add_argument('-f',
                        '--files',
                        nargs="+",
                        help='The files that this tool will edit. Default values should work.')
    args = parser.parse_args()

    # Default files to edit
    if args.files is None:
        args.files = [os.path.expanduser('~') + '/.config/user-dirs.dirs', '/etc/xdg/user-dirs.defaults']

    input(f"Please backup the following files:\n  {"\n  ".join(args.files)}\nthen press enter...")
    print("Starting job...")
    main(args.files)
    print("Finished.")
