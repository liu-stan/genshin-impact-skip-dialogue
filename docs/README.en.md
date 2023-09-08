# genshin-impact-skip-dialogue
genshin-impact-skip-dialogue is a tool designed to skip dialogue and story scenes in the Genshin Impact game. This tool automates the process of clicking through dialogue, choosing dialogue options, and pick up items. It relies on image recognition using opencv-python. Note that it does not support dialogue acceleration.

## Configuration Options

pause shortcut keys `pause` , `alt+p`

```yaml
# Tasks pause shortcut keys
tasks_pause: alt+p
```

## Installation and Usage 

### Using Pre-built Releases
Download and extract the tool from [releases](https://github.com/liu-stan/genshin-impact-skip-dialogue/releases). Run `gs_skip.exe` as an administrator.


### Running from Source Code


1. Clone the project repository to your local computer and download the source code:


```
git clone https://github.com/liu-stan/genshin-impact-skip-dialogue.git
cd genshin-impact-skip-dialogue
```

2. Create a Python virtual environment, activate it, and install dependencies:

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

```
3. Run the tool (requires administrator privileges):
```
python gs_skip.py
```

4. Optionally, you can use pyinstaller to package the tool. Copy the `images` folder and `config.yaml` to the `dist` folder, and then run `gs_skip.exe` as an administrator.

```
pyinstaller --onefile gs_skip.py
```