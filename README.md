# GGJ Card Maker

Generates a sweet html file that can be printed with a card for each jammer in a global game jam site.

![Screenshot](https://raw.github.com/technocake/ggj-participants-cards/master/screenshot.png)

#Setup

pip install requests
pip install requests-cache
pip install beautifulsoup4
pip install flask


# Usage
From CLI:
put jammers.csv in the folder and
run `python make_cards.py`

Web Interface:
you can also run a web interface for this. 
`python webinterface.py`

It will open the web-page in your browser automatically when ran.


#Input
  jammers.csv (downloaded from organizing site)
  put it in the same folder as this program.

  ![alt screenshot](https://raw.github.com/technocake/ggj-participants-cards/master/download-jammers.csv.png)

#Output
 jammers.html --> print it, impress.

See INSTALL.txt for details about config.

# Printing
![alt how to print](https://raw.github.com/technocake/ggj-participants-cards/master/print-in-chrome.png)

Ctrl+p in your browser. 
Chrome is recommended, as it lets you turn on the color backgrounds of the skills. By default browsers will strip background color from elements while printing. 

#Authors:
* Robin Garen Aaberg (technocake)
* Torstein Thune
* SnorreMD


 
# Classification
Btw, it classifies based on the ticked skillsets of the jammers into:

 * 2D
 * 3D
 * Programming
 * Sound
 * Other
 
