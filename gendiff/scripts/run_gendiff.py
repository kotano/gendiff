from gendiff import cli, core


def main():
    args = cli.get_arg_parser().parse_args()
    print(core.generate_diff(args.first_file, args.second_file, args.format))


if __name__ == "__main__":
    main()
