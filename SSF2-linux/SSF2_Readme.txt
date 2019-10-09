
Linux Users:

Before you can run SSF2, you may need to add the "data" folder as a Trusted Location in your Flash Player Settings. See below:

1) Launch SSF2 by running the "SSF2" executable file provided. If the loading screen gets stuck, proceed to Step 2. Otherwise you're already good to go.

2) Right-click the SSF2 game window and choose "Global Settings" from the context menu. It should take you to a Adobe Flash Player preferences window (if so, proceed to the next step). If it takes you to a website instead of this window, you may need to install the Adobe Flash plugin first. To do this, go to the Software & Updates application in your OS, and in the "Other Software" tab check the box next to "Canonical Partners" and close out. Once you've done this, go to your terminal and run:

sudo apt update
sudo apt install adobe-flashplugin

This should enable the Preference window when you repeat Step 2 from the beginning.

See below for more:

https://askubuntu.com/questions/765508/how-do-i-install-adobe-flashplayer-in-ubuntu-16-04

3) Click the "Advanced" tab. (If you don't see "Advanced" look for "Global Security Settings" instead)

4) Click the "Trusted Location Settings" button listed under the Developer Tools section. (It's possible you are already there from the previous step)

5) Click "Add Folder" (or "Edit Locations->Add Location"), and browse to the directory containing the SSF2 executable. Choose the "data" folder to add it to the list, and close each menu to confirm changes. (Note: Add only the first data folder "{APP_DIR}/data", NOT "{APP_DIR}/data/data")

6) Close and launch the game again. (Note: You must repeat the above steps if you ever move the game files to another directory)

Once you've done the above, simply run the "SSF2" executable file provided with the download. Enjoy!


(If you have issues with the launcher, you can also rename the "run" file in the data folder to "run.swf", and drag it into your internet browser. Be sure to have the latest Flash Player installed: https://get.adobe.com/flashplayer/ )

*** SmashNNAI debugging guide ***
TCP port: 2802

Game doesn't load once it reaches 100%
- Game is not connected to port, port most likely not opened. Close the game, open the port and start the game again