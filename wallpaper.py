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

CONFIG:
On initial launch it will create a configuration file at "~/.config/wallpaper.ini". Please set your wallpaper directory under "wallpaper_dir".

Example:

[Settings]
wallpaper_dir = /home/myUserName/Pictures/walls/_/


Wallpaper File Naming Convention:
My wallpapers have "_night", "_day" or both "_day_night", "bright", "dark", etc in their filename. This way this script can filter them. 
few examples:

Example 1: sunset_dark_night_painting.jpg
Example 2: alena-aenami-darknight_night_forest_dark_night_moon_painting.jpg

CRONTAB:
I have set it to change wallpaper every 10 minutes. Please refer to crontab manual/wiki.

An example of using it with crontab:
*/10 * * * * export "$HOME=/home/yuki"; export DISPLAY=":0.0"; /home/myUserName/my_scripts/bin/wallpaper.py --time; 




Built for linux OS. It uses find, ls, grep and other programs. Uses $HOME and forward slash. Feel free to port to other OS.
Dependencies:               NOTES:
            python3
            nitrogen        wallpaper utility
            argparse        python package. It maybe available with python standard install.
            configparser    python package. It maybe available with python standard install.


"""

    

class wallpaper():
    def __init__(self):
        self.home_dir = self.exec_sh("echo $HOME")[0]
        self.argparse_init()
        self.config_file = "{}/.config/wallpaper.ini".format(self.home_dir)
        self.last_wallpaper = self.get_setting(self.config_file, "last_wallpaper")

        # Check if wallpaper Dir specified
        if self.args.dir:
            self.update_setting(self.config_file, "wallpaper_dir", self.args.dir)


        if self.args.time:
            print("Will set wallpaper based on time !")
            if self.is_day():
                self.args.search = "day"
            else:
                self.args.search = "night"
       
        self.set()


    def argparse_init(self):
        # Argument management
        arg_parser = argparse.ArgumentParser(description="Set desktop wallpaper. Set wallpaper by either specifying a specific an image, select an image randomly from a directory or select an image randomly from a filtered list of images from a directory.")

        arg_parser.add_argument("-d", "--dir", action="store", help="Path of folder that contain wallpapers.")

        arg_parser.add_argument("-w", "--wall", action="store", help="File path of wallpaper.")

        arg_parser.add_argument("-t", "--time", action="store_true", help="Use time of day to pick Wallpaper")
        
        arg_parser.add_argument("-s", "--search", action="store", help="Filter images with keywords in file name. Use comma to seperate keywords.")

        arg_parser.add_argument("-e", "--exclude", action="store", help="Filter images for images without specified keywords in file name. Use comma to seperate keywords.")
        self.args = arg_parser.parse_args()

    def invalid_wall_dir(self):
        print("No wallpaper found in: {}, \n --> Please set the Wallpaper directory variable in the config file.\n --> Config file:  ~/.config/wallpaper.ini".format(self.get_setting(self.config_file, "wallpaper_dir")))
        exit()


    def create_config(self, path):
        config = configparser.ConfigParser()
        config['Settings'] = {"wallpaper_dir": "{}".format(self.home_dir+"/Pictures/"), "last_wallpaper": ""}
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
        Update a setting
        """

        config = self.get_config(path)
        config["Settings"][setting] = value
        with open(path, "w") as config_file:
            config.write(config_file)


    def exec_sh(self, command):
        """Executes bash code"""

        lin=subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
        (out1, err)=lin.communicate()
        out1 = str(out1, 'utf-8').splitlines(True)
        out1 = [s.replace("\n", "") for s in out1]
        return out1

    def is_day(self):
        """
        Return True if day: LMT < 16
        16 == 4PM, personal touch
        """

        import time
        if int(time.strftime("%H")) > 16:
            return False
        else:
            return False 

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
        if not self.args.wall:
            if self.args.search:
                command += " | grep {}".format(self.args.search)
            if self.args.exclude:
                command += " | grep -v {}".format(self.args.exclude)
            command += " | shuf -n {}".format(shuff)
        
        wallpapers = self.exec_sh(command)
        return wallpapers

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

        if self.args.wall:
            wallpapers = self.args.wall
            self.exec_sh("nitrogen --set-scaled {}".format(wallpapers))
            return
        else:
            wallpapers = self.search()

        if len(wallpapers) == 0:
            self.invalid_wall_dir()
            return False

        command = "nitrogen --set-scaled"

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

        self.clear()
        print("Last Wallpaper: {}".format(self.last_wallpaper.rsplit("/", 1)[1]))
        print("\nWill set: ", wallpapers.rsplit("/", 1)[1])


    def clear(self):
        # Clear screen, terminal.
        os.system('clear')
    

        
if __name__ == "__main__":
    wall = wallpaper()
