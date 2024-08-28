import subprocess


def create_skeleton():
    subprocess.run(["reflex", "init"], check=True)


def main():
    create_skeleton()


if __name__ == "__main__":
    main()
