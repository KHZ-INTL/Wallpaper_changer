# Wallpaper_changer
A python script that sets the wallpaper from randomly selected images, from a defined folder. Also able to search for a specific wallpaper and set it when you need to. It can filter for images that have or shouldn't have words, keyword in image file name, utilising the grep program. 

Also able to set wallpapers based on time, using --time option. If Local time &lt; 4PM, wallpaper is selected from: with "day" in filename. Appropriately for night. It was developed to be run periodically with crontab. 

##### System Resources
The application does not run run continuously in the background, this is on purpose so that it does not use ram and resources. For it to change wallpapers automatically it needs to be setup with crontab. Please see crontab section below. 

##### CRONTAB
I have set it to change wallpaper every 10 minutes. Please refer to a crontab manual/wiki, <a href="https://www.tutorialspoint.com/unix_commands/crontab.htm" target="_blank">TutorialPoint.com</a> have a simple guide on crontab.


An example:

`*/10 * * * * export "$HOME=/home/MyUserName"; export DISPLAY=":0.0"; /home/myUserName/my_scripts/bin/wallpaper.py --time;` 

#### Configuration:
On initial launch it will create a configuration file at "~/.config/wallpaper.ini". Please set your wallpaper directory under "wallpaper_dir". Please delete the configuration file when there is an update to the script.

Example:

`[Settings]`

`wallpaper_dir = /home/myUserName/Pictures/walls/_/`


#### Wallpaper File Naming Convention:
My wallpapers have "_night", "_day" or both "_day_night", "bright", "dark", etc in their filename. As result this script can filter them when used with the --time or --search option. It is not a requirement and you don't have to follow this naming convention. However, it is recommended.
few examples:

+ Example 1: sunset_dark_night_painting.jpg

+ Example 2: alena-aenami-darknight_night_forest_dark_night_moon_painting.jpg

#### Wal Colour scheme Generation
If PyWal is enabled; `wallpaper.py --pywal enabled`, then the selected wallppaer will be passed as an argument when calling wal for colour shcme generation. Also, you can change pywal's backend for colour scheme generation by using the `--pywal_backend` argument. You must install the additional backend if not available, they are available in python package repositories, use PIP. Furthermore, you can use random wal colour schemes using the `--pywal_random` argument.


#### Arguments

##### Search for a wallpaper: -s --search:
`wallpaper.py --search="sunset"`

##### Exclude images with x in filename: -e --exclude:
`wallpaper.py --search="sunset" --exclude="painting"`

##### Wallpaper Directory: -d --dir:
`wallpaper.py --dir="/home/myUserName/Pictures/walls/unfiltered/"`

##### Set a specific wallpaper: -w --wall:
`wallpaper.py --wall /home/myUserName/Pictures/walls/unfiltered/2.jpg"`

##### Set wallpaper based on time: -t --time:
`wallpaper.py --time`

##### Delete currently set wallpaper: -D --delete:
`wallpaper.py --delete`

##### Show information/configuartion values: -i --info:
`wallpaper.py --info`

##### Generate colour scheme using Wal-pywal: -p --pywal:
`wallpaper.py --pywal enabled`

##### Set Wal-pywal backend: -b --pywal_backend:
`wallpaper.py --pywal_backend colorz`
optional backends:
+ haishoku
+ wal
+ colorz
+ schemer2
+ colorthief


##### Dependencies:               NOTES:
+ Built for linux OS. It uses find, ls, grep and other programs. Uses $HOME and forward slash. Feel free to port to other OS.


| Dependencies  | Notes |
| ------------- | ------------- |
| python3 |  |
| feh  |  wallpaper utility |
| argparse | python package. It maybe available with python standard install. |
| configparser | python package. It maybe available with python standard install. |


#### LICENSE
GPL v3.0
