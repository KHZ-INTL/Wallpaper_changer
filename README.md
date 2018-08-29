# Wallpaper_changer
A python script that sets the wallpaper from randomly selected images, from defined folder. Also able to search for specific wallpaper. It can filter for images that have or should'nt have words, keyword in image file name, utilising the grep program. 

Also able to set wallpapers based on time. If Local time &lt; 4PM, wallpaper is selected from: with "day" in filename. Appropriately for night. It was developed to be run periodically with crontab, --time flag comes handy sometimes. 


The application does not run run continuously in the background, this is on purpose so that it does not use ram and resources. For it to change wallpapers automatically it needs to be setup with crontab. Please see my example below. 

#### Configuration:
On initial launch it will create a configuration file at "~/.config/wallpaper.ini". Please set your wallpaper directory under "wallpaper_dir".
Example:

[Settings]
wallpaper_dir = /home/myUserName/Pictures/walls/_/





#### Wallpaper File Naming Convention:
My wallpapers have "_night", "_day" or both "_day_night", "bright", "dark", etc in their filename. This way this script can filter them. 
few examples:

Example 1: sunset_dark_night_painting.jpg
Example 2: alena-aenami-darknight_night_forest_dark_night_moon_painting.jpg

#### CRONTAB:
I have set it to change wallpaper every 10 minutes. Please refer to crontab manual/wiki.

An example of using it with crontab:
*/10 * * * * export "$HOME=/home/MyUserName"; export DISPLAY=":0.0"; /home/myUserName/my_scripts/bin/wallpaper.py --time; 


#### Arguments

##### Search for wallpapers: -s --search:
`wallpaper.py --search="sunset"`

##### Exclude images: -e --exclude:
`wallpaper.py --search="sunset" --exclude="painting"`

##### Wallpaper Directory: -d --dir:
`wallpaper.py --dir="/home/myUserName/Pictures/walls/unfiltered/"`

##### Set a specific wallpaper: -w --wall:
`wallpaper.py -w /home/myUserName/Pictures/walls/unfiltered/2.jpg"`

##### Set wallpaper based on time: -t --time:
`wallpaper.py --time`


Built for linux OS. It uses find, ls, grep and other programs. Uses $HOME and forward slash. Feel free to port to other OS.
##### Dependencies:               NOTES:
            python3
            nitrogen        wallpaper utility
            argparse        python package. It maybe available with python standard install.
            configparser    python package. It maybe available with python standard install.

#### LICENSE
GPL v3.0
