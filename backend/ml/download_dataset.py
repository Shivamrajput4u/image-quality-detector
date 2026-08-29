"""One-time dataset setup: pulls the MVTec AD 'bottle' category from Kaggle.

Requires a free Kaggle account + API token: create one at
https://www.kaggle.com/settings -> API -> Create New Token, then place the
downloaded kaggle.json at ~/.kaggle/kaggle.json.

MVTec AD is hosted on Kaggle as individual per-image files rather than one
archive per category, so there's no way to fetch just "bottle" through the
API directly — this downloads the full ~5GB dataset once, keeps only the
category we need, and deletes the rest.

Usage (from backend/):
    python -m ml.download_dataset
"""

from __future__ import annotations

import shutil
from pathlib import Path

CATEGORY = "bottle"
DATASET = "ipythonx/mvtec-ad"

RAW_DIR = Path(__file__).resolve().parent / "_mvtec_raw"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "mvtec"


def main() -> None:
    import kaggle  # imported lazily — only needed for this one-time setup step

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {DATASET} (full dataset, ~5GB) to {RAW_DIR} ...")
    kaggle.api.dataset_download_files(DATASET, path=str(RAW_DIR), unzip=True)

    source = RAW_DIR / CATEGORY
    target = DATA_DIR / CATEGORY
    if target.exists():
        shutil.rmtree(target)
    shutil.move(str(source), str(target))

    shutil.rmtree(RAW_DIR)
    print(f"Kept only '{CATEGORY}' at {target}, removed the other 14 categories.")


if __name__ == "__main__":
    main()
