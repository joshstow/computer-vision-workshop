# Computer Vision Workshop

A hands-on workshop going from raw pixels (OpenCV) through real-time object detection (YOLO) to foundation models (SAM 2 & CLIP).

## Prerequisites

- A webcam (built-in or USB)
- [VS Code](https://code.visualstudio.com/) with the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extensions installed
- Git

---

## Environment Setup

> **Important:** This workshop requires **Python 3.12**. Newer versions (3.13/3.14) do not yet have compatible binary packages for all dependencies.

### 1. Get Python 3.12

Choose **one** of the options below — whichever suits your setup.

<details>
<summary><strong>Option A: Install Python 3.12 directly</strong> (simplest)</summary>

Download and install the latest Python 3.12 release from the official site:

**https://www.python.org/downloads/**

Scroll down to the **3.12.x** releases and download the installer for your OS.

- **macOS** — Download the `.pkg` installer and run it.
- **Windows** — Download the `.exe` installer. **Check "Add Python to PATH"** during installation.
- **Linux** — Use your package manager (e.g. `sudo apt install python3.12 python3.12-venv`) or download from the site.

After installation, verify:

```bash
python3.12 --version
# Should output: Python 3.12.x
```

> **Note:** On macOS/Linux the command may be `python3.12` rather than `python`. On Windows it is usually `python` or `py -3.12`.

</details>

<details>
<summary><strong>Option B: Use pyenv</strong> (manage multiple Python versions side-by-side)</summary>

[pyenv](https://github.com/pyenv/pyenv) lets you install and switch between multiple Python versions easily.

#### macOS

```bash
brew install pyenv
```

Then add pyenv to your shell config (`~/.zshrc`):

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

#### Linux (Ubuntu/Debian)

Install build dependencies first:

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses-dev \
  libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev tk-dev
```

Then install pyenv:

```bash
curl https://pyenv.run | bash
```

Add pyenv to your shell config (`~/.bashrc` or `~/.zshrc`):

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
```

#### Windows

On Windows, use [pyenv-win](https://github.com/pyenv-win/pyenv-win). Open **PowerShell** and run:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

Then **restart your terminal** for the changes to take effect.

#### Install & activate Python 3.12

```bash
pyenv install 3.12
```

If that shows an error, list available versions and pick the latest 3.12.x:

```bash
pyenv install --list | grep "3.12"
```

Then pin 3.12 to this project directory (won't affect the rest of your system):

```bash
pyenv local 3.12
```

</details>

Verify you have the right version before continuing:

```bash
python --version
# Should output: Python 3.12.x
```

> On macOS/Linux you may need to use `python3` or `python3.12` instead of `python` — use whichever command shows 3.12.x. The same applies to `pip` (`pip3` / `pip3.12`).

---

### 2. Clone the Repository

```bash
git clone https://github.com/joshstow/computer-vision-workshop.git
cd computer-vision-workshop
```

---

### 3. Create and Activate a Virtual Environment

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> If you get an execution policy error on Windows, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs everything needed for all three notebooks (OpenCV, YOLO, SAM 2, CLIP, etc.).

---

### 5. Select the Kernel in VS Code

1. Open the `computer-vision-workshop` folder in VS Code.
2. Open any notebook (e.g. `01_opencv.ipynb`).
3. Click the **kernel picker** in the top-right corner of the notebook.
4. Select **`.venv (Python 3.12.x)`** from the list.

You're ready to go!

---

## Workshop Notebooks

| # | Notebook | Topics |
|---|---|---|
| 01 | `01_opencv.ipynb` | Image matrices, colour spaces, edge detection, live webcam filters |
| 02 | `02_yolo.ipynb` | Real-time object detection & tracking, pose estimation, segmentation |
| 03 | `03_sam.ipynb` | SAM 2 auto-masks, CLIP zero-shot classification, YOLO + SAM 2 mega-pipeline |

Work through them in order — each notebook builds on concepts from the previous one.

---

## Troubleshooting

- **`ModuleNotFoundError`** — Make sure your virtual environment is activated and you've selected the `.venv` kernel in VS Code. Re-run `pip install -r requirements.txt` if needed.
- **Webcam not opening** — Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` if you have multiple cameras.
- **Window won't close** — Press `q` while the OpenCV window is focused. If it's still stuck, restart the notebook kernel.
- **NumPy / torch build errors** — You're probably on the wrong Python version. Run `python --version` and make sure it says 3.12.x.
- **SAM 2 checkpoint download fails** — Check your internet connection. The checkpoint (~150 MB) downloads automatically the first time you run the SAM 2 setup cell in `03_sam.ipynb`.