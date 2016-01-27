# GGJ Card Maker

Generates a sweet html file that can be printed with a card for each jammer in a global game jam site.
Each jammer is automatically classified and color-coded based on the chosen skillset on GGJ.org.

 * 2D (red)
 * 3D (dark red)
 * Programming (blue)
 * Sound (yellow)
 * Other (purple)

![Screenshot](https://raw.github.com/technocake/ggj-participants-cards/master/screenshot.png)

#Setup
In terminal run:
```terminal
git clone https://github.com/technocake/ggj-participants-cards
```
Then install dependencies:
```terminal
pip install requests
pip install requests-cache
pip install beautifulsoup4
pip install flask
```

# Usage

##Web Interface:
Start the webinterface: 
```python webinterface.py```
and upload jammers.csv

It will open the web-page in your browser automatically when ran.

##From CLI:
Alternatively one can run it as a standalone script. 

put jammers.csv in the folder and run 
```terminal
python make_cards.py
```

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
Btw, 
 
