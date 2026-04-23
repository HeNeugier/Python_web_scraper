import sys

def main():
    argv_len = len(sys.argv)
    if argv_len < 2:
        print("no website provided")
        sys.exit(1)
    if argv_len > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {sys.argv[1]}")


if __name__ == "__main__":
    main()
