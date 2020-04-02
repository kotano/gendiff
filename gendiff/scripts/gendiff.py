import argparse

parser = argparse.ArgumentParser(description='Generate diff')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format', help='set format of output')


def main():
    try:
        parser.parse_args()
    except SystemExit:
        pass


if __name__ == "__main__":
    main()
