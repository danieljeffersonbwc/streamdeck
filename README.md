🎮 ConsoleDeck
ConsoleDeck is a simple graphical interface that allows you to configure up to 9 buttons to launch websites or executable files with a click.  
Ideal for creating your own customizable macro deck or personal launcher.
---
✅ Requirements
A Windows PC
Python 3.11 or higher
Internet connection (only for the initial setup)
---
🐍 Step 1 – Install Python
Go to 👉 https://www.python.org/downloads/
Download the latest version of Python 3
During installation, check the box ✅ "Add Python to PATH"
Click Install Now
---
📦 Step 2 – Install required libraries
Open the Start menu
Type `cmd` and press Enter
In the terminal window, paste the following command:
```bash
pip install pygame pyperclip pyserial
```
If you get an error like `'pip' is not recognized`, try restarting your PC.
---
▶️ Step 3 – Run ConsoleDeck
Download all project files into a folder (e.g., Desktop)
Open that folder in the terminal (`cmd`)
Start the app with this command:
```bash
python main.py --gui
```
If everything is set up correctly, a graphical window will open.
---
⚙️ Features
Click one of the 9 buttons to assign an action
Choose between:
a website URL (e.g. `https://youtube.com`)
a `.exe` file on your PC
or no action
Modify the fields directly inside the app
Use the "Browse" button to select `.exe` files
Save your changes only when you're ready
Supports volume control, mute toggle, and media play/pause via serial
Settings are stored in a local file called `config.json`.
---
❓ Troubleshooting
🟡 Nothing happens when I click a button?  
Make sure you launched the app using: `python main.py --gui`
🔗 Can I use YouTube or other links?  
Yes, any valid `https://` link will work.
🧩 Can I assign programs like `.exe` files?  
Yes! Use the “Browse” button to pick an executable file.
💾 It says 'pip' is not recognized  
Restart your computer or reinstall Python and ensure "Add Python to PATH" is selected during setup.
---
🧼 How to uninstall
You can delete the project folder at any time
To uninstall Python, go to Apps & Features in Windows
