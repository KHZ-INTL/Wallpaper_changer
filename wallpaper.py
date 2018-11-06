#!/usr/bin/python3

import os
import argparse
import configparser
import subprocess


"""
A python script that sets wallpapers from randomly selected images from a folder. Also able to search for specific wallpaper.
It can filter for images that have or should'nt have specific words, keyword in image file name using the grep program.
Also able to set wallpapers based on time. If Local time < 4PM, wallpaper is selected from: with "day" in filename. Appropriately for night.
It was developed to be run periodically with crontab, --time flag comes handy sometimes. For more info: wallpaper.py --help.
"""


class wallpaper():

    def __init__(self):
        self.home_dir = self.exec_sh("echo $HOME")[0]
        self.argparse_init()
        self.config_file = "{}/.config/wallpaper.ini".format(self.home_dir)
        self.last_wallpaper = self.get_setting(self.config_file, "last_wallpaper")

        if self.args.dir:
            self.update_setting(self.config_file, "wallpaper_dir", self.args.dir)

        if self.args.delete:
            self.delete_cWall()

        if self.args.info:
            self.info()
            exit()

        if self.args.current:
            self.current()
            exit()

        if self.args.time:
            print("Will set wallpaper based on time !")
            if self.is_day():
                self.args.search = "day"
            else:
                self.args.search = "night"

        if self.args.pywal_random:
            self.update_setting(self.config_file, "pywal_random_theme", "enabled")

        if self.args.pywal_backend:
            self.update_setting(self.config_file, "pywal_backend", self.args.pywal_backend)

        if self.args.pywal:
            self.update_setting(self.config_file, "pywal", self.args.pywal)
            exit()

        if self.args.wallpaper:
            wallpapers = self.args.wallpaper
            # self.exec_sh("nitrogen --set-scaled {}".format(wallpapers))
            self.exec_sh("feh --bg-scale {}".format(wallpapers))
            self.gen_colour(wallpapers)
            self.update_setting(self.config_file, "dont_change_user_set_wallpaper", "true")
            exit()

        if self.get_setting(self.config_file, "dont_change_user_set_wallpaper") == "true":
            print("Dont_change_user_set_wallpaper --> TRUE\nSkipping setting wallpaper")
            exit()

        self.set()

    def argparse_init(self):
        # Argument management
        arg_parser = argparse.ArgumentParser(description="Set desktop wallpaper. Set wallpaper by either specifying a specific an image, select an image randomly from a directory or select an image randomly from a filtered list of images from a directory.")

        arg_parser.add_argument("-d", "--dir", action="store", help="Path of folder that contain wallpapers.")

        arg_parser.add_argument("-w", "--wallpaper", action="store", help="Set wallpaper using file path.")

        arg_parser.add_argument("-p", "--pywal", action="store", help="Enable/disable colour scheme generation using pywal possible value: enabled/disabled")

        arg_parser.add_argument("-b", "--pywal_backend", action="store", help="Change pywal colour scheme backend: haishoku, wal, colorz, schemer2, colorthief")

        arg_parser.add_argument("-r", "--pywal_random", action="store_true", help="Set random colour scheme from pywal predefined themes. Dark/light theme is selected based on file name")

        arg_parser.add_argument("-t", "--time", action="store_true", help="Use time of day to pick Wallpaper")

        arg_parser.add_argument("-i", "--info", action="store_true", help="Show current configuration values")

        arg_parser.add_argument("-c", "--current", action="store_true", help="Show current wallpaper")

        arg_parser.add_argument("-D", "--delete", action="store_true", help="Delete current wallpaper")

        arg_parser.add_argument("-s", "--search", action="store", help="Filter images with keywords in file name. Use comma to seperate keywords.")

        arg_parser.add_argument("-e", "--exclude", action="store", help="Filter images for images without specified keywords in file name. Use comma to seperate keywords.")
        self.args = arg_parser.parse_args()

    def invalid_wall_dir(self):
        print("No wallpaper found in: {}, \n --> Please set the Wallpaper directory variable in the config file.\n --> Config file:  ~/.config/wallpaper.ini".format(self.get_setting(self.config_file, "wallpaper_dir")))
        exit()

    def create_config(self, path):
        config = configparser.ConfigParser()
        config['Settings'] = {"wallpaper_dir": "{}".format(self.home_dir+"/Pictures/"), "last_wallpaper": "", "dont_change_user_set_wallpaper": "true", "pywal": "disabled", "pywal_backend": "colorz", "pywal_random_theme": "disabled"}
        print("New config file created !. \nPlease set wallpaper folder in config file.\nConfig File: ", path)
        with open(path, "w") as config_file:
            config.write(config_file)
        exit()

    def get_config(self, path):
        """
        Returns the config object
        """
        if not os.path.exists(path):
            self.create_config(path)

        config = configparser.ConfigParser()
        config.read(path)
        return config

    def get_setting(self, path, setting):
        """
        Print out a setting
        """
        config = self.get_config(path)
        value = config["Settings"][setting]
        return value

    def update_setting(self, path, setting, value):
        """
        Update a setting in config_file
        """

        config = self.get_config(path)
        config["Settings"][setting] = value
        with open(path, "w") as config_file:
            config.write(config_file)

    def exec_sh(self, command):
        """Executes shell code"""

        lin = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        (out1, err) = lin.communicate()

        out1 = str(out1, 'utf-8').splitlines(True)
        out1 = [s.replace("\n", "") for s in out1]

        return out1

    def is_day(self):
        """
        Return True if day: LMT < 16
        16 == 4PM, change this to suit your self.
        """

        import time
        if int(time.strftime("%H")) > 16:
            return False
        else:
            return False

    def info(self):
        """ Show the current values used in configuration file
        :returns: None

        """
        for i in self.get_config(self.config_file)["Settings"]:
            print("[{}]".format(i), ": ", self.get_setting(self.config_file, i))

    def current(self):
        """ Show the current values used in configuration file
        :returns: None

        """
        last_wallpaper = self.get_config(self.config_file)["Settings"]["last_wallpaper"]
        print(last_wallpaper)

    def search(self, shuff="2"):
        """
        build/create a bash command
        to search for images in folder as set in config file.
        images are filtered using grep with search and exclude option.
        The search term given as argument to script: filter for images with that in filename.
        The exclude term given as argument to script: exclude images with that in filename.
        From filtered images two are picked (shuf=2), in case last wallpaper == new.
        """

        wallpaper_dir = self.get_setting(self.config_file, "wallpaper_dir")

        if not os.path.exists:
            self.invalid_wall_dir()
            print("Wallpaper directory does not exist !.\nPlease set it in Config file: ", self.config_file)
            exit()
        if self.exec_sh("ls | wc -l") == '0':
            print("No wallpapers found in: \n", wallpaper_dir)
            exit()

        # initial command
        command = "find {} -type f | grep '.jpg\|.png\|.jpeg\|'".format(wallpaper_dir)

        # populate command for search query, exclude words
        if not self.args.wallpaper:
            if self.args.search:
                command += " | grep -i {}".format(self.args.search)
            if self.args.exclude:
                command += " | grep -v {}".format(self.args.exclude)
            command += " | shuf -n {}".format(shuff)

        wallpapers = self.exec_sh(command)
        return wallpapers

    def delete_cWall(self):
        """
        Delete the wallpaper that was set to "last_wallpaper" in the configuration file.
        """
        current_wallpaper = self.get_setting(self.config_file, "last_wallpaper")
        self.exec_sh("rm {}".format(current_wallpaper))
        self.update_setting(self.config_file, "last_wallpaper", "")
        print("attempting to delete: ", current_wallpaper)

    def gen_colour(self, wallpapers):
        """
        Run wal binary to generate colour scheme with wallpaper.
        """
        command = "wal -n --saturate 0.4 "

        if self.get_setting(self.config_file, "pywal") == "enabled" and self.get_setting(self.config_file, "pywal_random_theme") == "disabled":
            pywal_backend = "colorz"
            pywal_backend = self.get_setting(self.config_file, "pywal_backend")
            command += "-i {} --backend {} ".format(wallpapers, pywal_backend)

            self.exec_sh(command)

        elif self.get_setting(self.config_file, "pywal_random_theme") == "enabled":
            command += "--theme "
            if self.is_day():
                command += "random_light"
            else:
                command += "random_dark"
            print(command)
            self.exec_sh(command)

    def set(self):
        """
        Calls search method, it will try to return 2 images.
        Checks if the search method found wallpapers.

        Checks if last wallpaper == new.
        if are the same and the search method returned 2 images:
            it will use 2nd returned image as wallpaper.
        Prints names of both last wallpaper and new.
        """

        wallpapers = ""

        wallpapers = self.search()

        #self.exec_sh("dunstify -a system -i '/usr/share/icons/Arc/apps/48@2x/preferences-desktop-wallpaper.png' -t 6000 -r 9989 -u normal 'Wallpaper' 'Downloading random wallpaper: unsplash.com'")


        if len(wallpapers) == 0:
            self.invalid_wall_dir()
            return False

        # command = "nitrogen --set-scaled"
        #command = "feh --bg-scale"
        command = "feh --bg-fill"

        # check if last_wallpaper == newly selected
        if wallpapers[0] == self.get_setting(self.config_file, "last_wallpaper"):
            if len(wallpapers) <2:
                command += " {}".format(wallpapers[0])
                self.update_setting(self.config_file, "last_wallpaper", wallpapers[0])
                wallpapers = wallpapers[0]
            else:
                command += " {}".format(wallpapers[1])
                self.update_setting(self.config_file, "last_wallpaper", wallpapers[1])
                wallpapers = wallpapers[1]
        else:
            command += " {}".format(wallpapers[0])
            self.update_setting(self.config_file, "last_wallpaper", wallpapers[0])
            wallpapers = wallpapers[0]

        self.exec_sh("{}".format(command))
        self.gen_colour(wallpapers)

        # self.clear()
        # set a default last wallpaper to prevent error when new config is created
        try:
            last_wallpaper = self.last_wallpaper.rsplit("/", 1)[1]
        except IndexError as e:
            last_wallpaper = ""

        print("Last Wallpaper: ", last_wallpaper)
        print("\nWill set: ", wallpapers.rsplit("/", 1)[1])

    def clear(self):
        # Clear screen, terminal.
        os.system('clear')

if __name__ == "__main__":
    wall = wallpaper()
