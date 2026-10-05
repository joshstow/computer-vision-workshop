# Computer Vision Workshop

A hands-on workshop going from raw pixels (OpenCV) through real-time object detection (YOLO) to foundation models (SAM 2 & CLIP).

_by Josh Stow_

## Before the Workshop

**Please do this at home, before the day.** It downloads about 3 GB (Python packages and AI models) and takes 10–20 minutes. Venue wifi won't cope with everyone doing it at once.

You'll need:

- A laptop with a webcam (built-in or USB)
- [VS Code](https://code.visualstudio.com/) with the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) extensions
- [Git](https://git-scm.com/downloads) (optional: you can download the ZIP instead, see step 2)

> You **don't** need to install Python yourself: `uv` downloads the right version (3.12) automatically.

> **On Windows?** Work through the [Windows checklist](#windows-checklist) first. It fixes the most common install problems.

### 1. Install uv

[uv](https://docs.astral.sh/uv/) installs Python and all the workshop's packages for you, with the exact same versions on every laptop.

| macOS / Linux (Terminal) | Windows (PowerShell) |
|---|---|
| `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

On Windows, if that command is blocked (e.g. on a work laptop), try `winget install --id=astral-sh.uv -e` instead.

**Then close and reopen your terminal.** If you're using the terminal inside VS Code, quit VS Code completely and reopen it, so it picks up the new `uv` command. Check it worked:

```
uv --version
```

### 2. Download the workshop

```
git clone https://github.com/joshstow/computer-vision-workshop.git
cd computer-vision-workshop
```

No Git? On the GitHub page click **Code → Download ZIP**, unzip it, then `cd` into the folder in your terminal (it will be called `computer-vision-workshop-main`).

### 3. Install everything

```
uv sync
```

This one command downloads Python 3.12 if needed, creates a `.venv` folder inside the project, and installs every package at the exact versions in `uv.lock`. There's no need to activate anything or run `pip`.

### 4. Run the setup check

```
uv run python check_setup.py
```

This checks every library, downloads all the AI models, and tests your webcam. You want the last line to say:

```
All good - you're ready for the workshop!
```

Any line marked `[FAIL]` comes with a `->` hint on how to fix it. See also [Troubleshooting](#troubleshooting).

### 5. Select the kernel in VS Code

1. In VS Code, use **File → Open Folder…** and open the `computer-vision-workshop` folder itself (not the folder above it).
2. Open `01_opencv.ipynb`.
3. Click **Select Kernel** (top right) → **Python Environments** → **.venv (Python 3.12.x)**.
4. Run the first cell (Shift+Enter). If it prints numbers and shows a picture, you're done.

<details>
<summary><strong>Alternative: set up without uv (plain Python + pip)</strong></summary>

1. Install **Python 3.12** (not 3.13 or newer) from [python.org/downloads](https://www.python.org/downloads/). Scroll down to the 3.12.x releases.
   On Windows, **tick "Add python.exe to PATH"** in the installer.
2. In the `computer-vision-workshop` folder, create and activate a virtual environment, then install:

   **macOS / Linux**
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python check_setup.py
   ```

   **Windows (PowerShell)**
   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python check_setup.py
   ```

   If `Activate.ps1` gives an execution policy error, run
   `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` and try again.

> Always use `python -m pip`, never plain `pip`. Plain `pip` can belong to a different Python on your machine, which installs the packages somewhere your notebooks can't see them.

Then select the `.venv` kernel in VS Code as in step 5.

</details>

### Platform notes

#### Windows checklist

Most install problems happen on Windows. Do these **before** step 1:

- [ ] **Install the [Microsoft Visual C++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe).** PyTorch needs it. Without it you'll get `OSError: [WinError 126] ... error loading "...\torch\lib\c10.dll"`.
- [ ] **Put the workshop in a short folder outside OneDrive,** e.g. `C:\code\computer-vision-workshop`. Desktop and Documents are often synced by OneDrive, which locks files mid-install and tries to upload gigabytes of packages. Very long paths can also make installs fail.
- [ ] **Enable long paths** (needs admin, then restart): open PowerShell as Administrator and run
  `New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name LongPathsEnabled -Value 1 -PropertyType DWORD -Force`
- [ ] **Allow camera access:** Settings → Privacy & security → Camera → turn on *Camera access* **and** *Let desktop apps access your camera*.
- [ ] **Use PowerShell, not WSL.** OpenCV windows and webcams don't work from inside WSL.
- [ ] **Windows on ARM** (Snapdragon / Copilot+ laptops, Surface Pro X): PyTorch and OpenCV have no native ARM builds, so use the x64 version of Python, which runs under emulation and is slower. Replace step 3 with:
  ```powershell
  uv python install cpython-3.12-windows-x86_64-none
  uv sync --python cpython-3.12-windows-x86_64-none
  ```

#### macOS

- **Camera permission:** the first webcam cell triggers a permission prompt for VS Code. If you clicked *Don't Allow*, go to System Settings → Privacy & Security → Camera, turn VS Code on, and restart VS Code.
- **Intel Macs** (Apple menu → About This Mac says "Intel"): the PyTorch version used here no longer supports Intel Macs, so `uv sync` will fail. Please pair up with a neighbour for the workshop.
- If `git` asks you to install the Command Line Developer Tools, click *Install* and re-run the command afterwards.

#### Linux

- If importing OpenCV fails with `libGL.so.1: cannot open shared object file`, run `sudo apt install libgl1 libglib2.0-0`.
- If the webcam won't open, check your user is in the `video` group: `groups | grep video`.

---

## Workshop Notebooks

| # | Notebook | Topics |
|---|---|---|
| 01 | `01_opencv.ipynb` | Image matrices, colour spaces, edge detection, live webcam filters |
| 02 | `02_yolo.ipynb` | Real-time object detection & tracking, pose estimation, segmentation |
| 03 | `03_sam.ipynb` | SAM 2 auto-masks, CLIP zero-shot classification, YOLO + SAM 2 mega-pipeline |
| 04 | `04_advanced.ipynb` | Advanced video tracking, text-prompted segmentation & CLIP fine-tuning |

Work through them in order — each notebook builds on concepts from the previous one.

---

## Troubleshooting

- **`ModuleNotFoundError`** — Make sure your virtual environment is activated and you've selected the `.venv` kernel in VS Code. Re-run `pip install -r requirements.txt` if needed.
- **Webcam not opening** — Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` if you have multiple cameras.
- **Window won't close** — Press `q` while the OpenCV window is focused. If it's still stuck, restart the notebook kernel.
- **NumPy / torch build errors** — You're probably on the wrong Python version. Run `python --version` and make sure it says 3.12.x.
- **SAM 2 checkpoint download fails** — Check your internet connection. The checkpoint (~150 MB) downloads automatically the first time you run the SAM 2 setup cell in `03_sam.ipynb`.