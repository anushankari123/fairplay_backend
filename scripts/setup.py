import subprocess
import sys


def install():
    """
    Installs the dependencies with poetry
    """
    try:
        subprocess.run(["poetry", "install"], check=True)
        print("Package installion with poetry has completed successfully.")
    except subprocess.CalledProcessError as err:
        print("Error while installing the packages with poetry", err)
        sys.exit(1)


def hook_activation():
    """
    Activates the hook using autohook package
    """
    try:
        subprocess.run(["poetry", "run", "autohooks", "activate", "--mode", "poetry"], check=True)
        print("Git hooks have been setup successfully.")
    except subprocess.CalledProcessError as err:
        print("Error while setting up the git hooks", err)
        sys.exit(1)


def setup():
    install()
    hook_activation()
