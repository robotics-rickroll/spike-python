# Pybricks Development Setup in VS Code

This guide will help you set up Visual Studio Code for LEGO SPIKE Prime development using Pybricks, and install the Pybricks Runner extension for easy code deployment.

## Prerequisites
- LEGO SPIKE Prime or compatible hub
- USB or Bluetooth connection to your computer
- Python 3.x installed (for some tools)
- Visual Studio Code installed

## 1. Install Visual Studio Code
Download and install VS Code from [https://code.visualstudio.com/](https://code.visualstudio.com/).

## 2. Install Pybricks Runner Extension
Pybricks Runner makes it easy to run and upload MicroPython code to your LEGO hub.

### Steps:
1. Open VS Code
2. Go to the Extensions sidebar (Ctrl+Shift+X or Cmd+Shift+X)
3. Search for `pybricks-runner`
4. Click **Install** on the extension by Pybricks

Or install directly from the [Pybricks Runner Marketplace page](https://marketplace.visualstudio.com/items?itemName=AnandSingh.pybricks-runner).

## 3. Connect Your Hub
- Power on your SPIKE Prime hub
- Connect via USB or Bluetooth
- Make sure your hub is in update mode if required (see Pybricks docs)

## 4. Create or Open Your Project
- Place your `.py` files in the `pybricks/` folder
- Use the provided example files as templates

## 5. Run Your Code
- Open the Python file you want to run
- Click the Pybricks Runner button in the top right, or use the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`) and search for `Pybricks: Run`.
- Follow prompts to select your hub and deploy code

## 6. How to Run the Current Python File with Pybricks Runner (AnandSingh)

1. Open the `.py` file you want to run in VS Code (for example, `robot.py`).
2. Make sure your LEGO hub is powered on and connected via USB or Bluetooth.
3. In VS Code, look for the Pybricks Runner button in the top right of the editor window (it looks like a small LEGO brick).
4. Click the Pybricks Runner button to start uploading and running your code on the hub.
   - Alternatively, open the Command Palette (`Cmd+Shift+P` on Mac or `Ctrl+Shift+P` on Windows/Linux), type `Pybricks: Run`, and select it.
5. Follow the prompts to select your hub and confirm the upload.
6. Your code will be transferred and executed on the LEGO hub.

**Tip:**
- If you have multiple hubs connected, you will be prompted to select which one to use.
- Make sure your hub firmware is compatible with Pybricks.
- For more details, see the [Pybricks Runner extension page](https://marketplace.visualstudio.com/items?itemName=AnandSingh.pybricks-runner).

## 7. Troubleshooting
- Make sure your hub firmware is up to date
- If you have connection issues, try reconnecting USB/Bluetooth or restarting VS Code
- Check the Pybricks Runner extension documentation for more help

## Resources
- [Pybricks Documentation](https://docs.pybricks.com/)
- [Pybricks Runner Extension](https://marketplace.visualstudio.com/items?itemName=AnandSingh.pybricks-runner)
- [SPIKE Prime Getting Started](https://docs.pybricks.com/projects/spikeprime/en/latest/)

Happy coding with LEGO and Pybricks!