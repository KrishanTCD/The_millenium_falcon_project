from setuptools import setup
from setuptools.command.install import install
import subprocess
import os
import pkgutil


# Automatically installs required packages from requirements.txt and then creates a logger folder
# The logger folder holds logs for running code including error and stuff
class env_setup(install):
    def run(self):
        install.run(self)

        # Checking if the logger folders exists if it doesn't then it creates it
        if not os.path.exists('static'):
            os.makedirs('static')
            print("Created 'static' folder.")

        # Read requirements from requirements.txt
        with open('requirements.txt', 'r') as f:
            requirements = f.read().splitlines()

        # Check if the packages needed are there or not, if not pip install them
        for requirement in requirements:
            installed = False
            for _, modname, ispkg in pkgutil.iter_modules():
                if modname == requirement:
                    installed = True
                    print(f"{requirement} is already installed.")
                    break

            if not installed:
                print(f"{requirement} is not installed. Installing...")
                subprocess.call(['pip', 'install', requirement])

        # Run the main file
        # subprocess.call(['python', 'main.py'])


setup(
    name='The_millenium_falcon_project',
    version='1.0',
    cmdclass={'install': env_setup},
)
