# Computer Vision Workshop

A hands-on workshop going from raw pixels (OpenCV) through real-time object detection (YOLO) to foundation models (SAM 2 & CLIP).

_by Josh Stow_

## Prerequisites

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
   export SAM2_BUILD_CUDA=0
   python -m pip install -r requirements.txt
   python check_setup.py
   ```

   **Windows (PowerShell)**
   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   $env:SAM2_BUILD_CUDA = "0"
   python -m pip install -r requirements.txt
   python check_setup.py
   ```

   `SAM2_BUILD_CUDA=0` tells SAM 2's installer to skip compiling an optional GPU extension that the workshop doesn't need.

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

Run `uv run python check_setup.py` first: it pinpoints most problems. Then find your error below.

### Installing

| You see… | Fix |
|---|---|
| `uv: command not found` / `'uv' is not recognized` | Close and reopen your terminal. If you're in VS Code's terminal, quit VS Code completely and reopen it. |
| `OSError: [WinError 126]` or `DLL load failed` when importing torch | Install the [Visual C++ Redistributable (x64)](https://aka.ms/vs/17/release/vc_redist.x64.exe) and restart. |
| `Could not install packages due to an OSError` / `No such file or directory` on Windows | Path too long or inside OneDrive. Move the folder to e.g. `C:\code\` and enable long paths (see the [Windows checklist](#windows-checklist)). |
| `No matching distribution found for torch` / errors building NumPy or torch | Wrong Python version. Use `uv sync` (it picks 3.12 for you), or check `python --version` says 3.12.x. |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`. |
| `SSL: CERTIFICATE_VERIFY_FAILED` or downloads time out | A work or venue network is blocking downloads. Try home wifi or a phone hotspot. |
| Something's still broken | Delete the `.venv` folder and run `uv sync` again. |

### Running the notebooks

| You see… | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'cv2'` (or `ultralytics`, `torch`…) | VS Code is using the wrong Python. Click the kernel name (top right) and choose **.venv (Python 3.12.x)**. To check, run `import sys; print(sys.executable)` in a cell: the path should contain `.venv`. |
| `.venv` isn't in the kernel list | Make sure you opened the `computer-vision-workshop` folder itself. Then press Ctrl/Cmd+Shift+P → **Developer: Reload Window**, and look under **Select Another Kernel → Python Environments**. |
| `RuntimeError: Could not open webcam` | Check camera permissions ([Windows](#windows-checklist) / [macOS](#macos)) and close Zoom/Teams. If a previous webcam cell crashed, restart the kernel (it still holds the camera). Got two cameras? Set `CAMERA_INDEX = 1` in `workshop.py`. |
| The cell is running but no window appears | The OpenCV window probably opened *behind* VS Code. Look for a Python icon in the taskbar or Dock, or use Alt+Tab / Cmd+Tab. |
| Pressing `q` does nothing | Click the OpenCV window first: it needs keyboard focus, not VS Code. If it's still stuck, press **Interrupt** on the notebook toolbar, or **Restart** the kernel. |
| "The kernel crashed" during SAM 2 / Grounding DINO / CLIP | Your laptop ran out of memory. Close other apps (especially browsers), restart the kernel, and re-run from the top of the notebook. |
