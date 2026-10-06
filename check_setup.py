"""
Pre-workshop setup check.

Run this BEFORE the workshop, from the repo folder:

    uv run python check_setup.py          (if you installed with uv)
    python check_setup.py                 (if you activated a venv yourself)

It checks your Python version, imports every library the notebooks use,
downloads all model weights / datasets (~2 GB, so do it on good wifi!)
and tries to open your webcam.

Options:
    --no-downloads   skip the model / dataset downloads
    --no-camera      skip the webcam test
"""

import importlib
import importlib.metadata
import os
import platform
import sys

# Run from the repo folder so relative paths like "models/..." work
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Hide harmless Hugging Face warnings that look scary to beginners
os.environ.setdefault("TRANSFORMERS_VERBOSITY", "error")
os.environ.setdefault("HF_HUB_VERBOSITY", "error")

OK, FAIL, WARN = "[ OK ]", "[FAIL]", "[WARN]"  # plain ASCII so every terminal can print it
problems = []


def report(status, message, fix=None):
    print(f"  {status} {message}")
    if fix:
        print(f"         -> {fix}")
    if status == FAIL:
        problems.append(message)


# ---------------------------------------------------------------------------
def check_python():
    print("\n1. Python & system")
    v = sys.version_info
    machine = platform.machine().lower()
    print(f"  Python {platform.python_version()} on {platform.system()} {platform.release()} ({machine})")
    print(f"  Interpreter: {sys.executable}")

    if (v.major, v.minor) == (3, 12):
        report(OK, "Python 3.12")
    else:
        report(FAIL, f"Python {v.major}.{v.minor} - this workshop needs Python 3.12",
               "Use `uv run python check_setup.py`, or recreate your venv with Python 3.12 (see README)")

    if sys.prefix == sys.base_prefix:
        report(WARN, "Not running inside a virtual environment",
               "Packages may be going into your system Python. Use `uv run ...` or activate .venv first")

    if platform.system() == "Windows" and machine in ("arm64", "aarch64"):
        report(FAIL, "Windows on ARM: torch and OpenCV have no native wheels",
               "Use x64 Python instead: `uv python install cpython-3.12-windows-x86_64-none` (see README)")
    if platform.system() == "Darwin" and machine == "x86_64":
        report(FAIL, "Intel Mac: torch 2.10 doesn't support Intel Macs",
               "Pair up with a neighbour for the workshop (see README)")


# ---------------------------------------------------------------------------
LIBRARIES = [
    # (import name, friendly name)
    ("numpy", "NumPy"),
    ("cv2", "OpenCV"),
    ("matplotlib", "Matplotlib"),
    ("PIL", "Pillow"),
    ("torch", "PyTorch"),
    ("torchvision", "torchvision"),
    ("ultralytics", "Ultralytics (YOLO)"),
    ("sam2", "SAM 2 (Meta)"),
    ("lap", "lap (YOLO tracker)"),
    ("transformers", "Transformers (CLIP + Grounding DINO)"),
    ("datasets", "Datasets"),
    ("ipykernel", "ipykernel (VS Code notebooks)"),
]


def check_imports():
    print("\n2. Libraries")
    all_ok = True
    for module, name in LIBRARIES:
        try:
            mod = importlib.import_module(module)
            version = getattr(mod, "__version__", None) or importlib.metadata.version(module)
            report(OK, f"{name} {version}")
        except Exception as e:  # not just ImportError: torch raises OSError on Windows DLL problems
            all_ok = False
            fix = "Re-run `uv sync` (or `python -m pip install -r requirements.txt` inside your venv)"
            if "WinError 126" in str(e) or "DLL" in str(e):
                fix = ("Install the Microsoft Visual C++ Redistributable (x64): "
                       "https://aka.ms/vs/17/release/vc_redist.x64.exe then restart")
            report(FAIL, f"{name}: {type(e).__name__}: {e}", fix)

    if all_ok:
        import torch
        x = torch.rand(3, 3) @ torch.rand(3, 3)
        report(OK, f"PyTorch can run maths ({'CUDA GPU' if torch.cuda.is_available() else 'CPU'})")
    return all_ok


# ---------------------------------------------------------------------------
def check_downloads():
    print("\n3. Model weights & datasets (first run downloads ~2 GB)")

    def attempt(name, fn):
        print(f"  ...  {name}", flush=True)
        try:
            fn()
            report(OK, name)
        except Exception as e:
            report(FAIL, f"{name}: {type(e).__name__}: {e}",
                   "Check your internet connection (or proxy / firewall) and re-run this script")

    from ultralytics import YOLO
    for weights in ["yolov8n.pt", "yolov8n-pose.pt", "yolov8n-seg.pt"]:
        attempt(f"YOLO weights models/{weights}", lambda w=weights: YOLO(f"models/{w}"))

    def sam2():
        # Same checkpoint and config as notebooks 03 and 04
        import urllib.request
        from sam2.build_sam import build_sam2
        checkpoint = "models/sam2.1_hiera_small.pt"
        if not os.path.exists(checkpoint):
            os.makedirs("models", exist_ok=True)
            # Download to a temp name first so a dropped connection never leaves a broken file behind
            urllib.request.urlretrieve(
                "https://dl.fbaipublicfiles.com/segment_anything_2/092824/sam2.1_hiera_small.pt",
                checkpoint + ".part")
            os.replace(checkpoint + ".part", checkpoint)
        build_sam2("configs/sam2.1/sam2.1_hiera_s.yaml", checkpoint, device="cpu")

    attempt("SAM 2.1 small checkpoint models/sam2.1_hiera_small.pt", sam2)

    from transformers import (AutoModelForZeroShotObjectDetection, AutoProcessor,
                              CLIPModel, CLIPProcessor)

    def clip():
        CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    def gdino():
        AutoModelForZeroShotObjectDetection.from_pretrained("IDEA-Research/grounding-dino-tiny")
        AutoProcessor.from_pretrained("IDEA-Research/grounding-dino-tiny")

    def beans():
        from datasets import load_dataset
        load_dataset("AI-Lab-Makerere/beans")

    attempt("CLIP (openai/clip-vit-base-patch32)", clip)
    attempt("Grounding DINO (IDEA-Research/grounding-dino-tiny)", gdino)
    attempt("Beans dataset (AI-Lab-Makerere/beans)", beans)


# ---------------------------------------------------------------------------
def check_camera():
    print("\n4. Webcam")
    from workshop import close_camera, open_camera

    try:
        cap = open_camera()
    except RuntimeError as e:
        report(FAIL, str(e))
        return

    ok, frame = cap.read()
    close_camera(cap)
    if ok:
        report(OK, f"Webcam works ({frame.shape[1]}x{frame.shape[0]})")
    else:
        report(FAIL, "Webcam opened but returned no frames",
               "Close other apps using the camera (Zoom, Teams...) and try again")


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Computer Vision Workshop - setup check")
    check_python()
    imports_ok = check_imports()
    if imports_ok and "--no-downloads" not in sys.argv:
        check_downloads()
    if imports_ok and "--no-camera" not in sys.argv:
        check_camera()

    print()
    if problems:
        print(f"{len(problems)} problem(s) found - see the -> hints above, or the README Troubleshooting section.")
        sys.exit(1)
    print("All good - you're ready for the workshop!")
