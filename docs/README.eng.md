# HIVAU-70k

HIVAU-70k, a large-scale benchmark for hierarchical video anomaly understanding across any granularity.

> This repository extracts and organizes **only the code for generating the HIVAU-70k benchmark based on UCF-Crime and XD-Violence** from the [HolmesVAU official repository](https://github.com/pipixin321/HolmesVAU). For model training, inference code, and the full framework, please refer to the original repo.

---

## 📌 Overview

This repository provides the method to build a video anomaly detection benchmark based on the approach proposed in HolmesVAU’s **HIVAU-70k**, using the following two public datasets:

* [UCF-Crime](https://www.crcv.ucf.edu/projects/real-world/)
* [XD-Violence](https://roc-ng.github.io/XD-Violence/)

---

## 🗂 Folder Structure

Organize your video data in the following structure:

```bash
├── HIVAU-70k
    └── src
        └── videos
            ├── ucf-crime
            │   └── videos
            │       ├── train
            │       └── test
            │   └── clips
            │       ├── train
            │       └── test
            │   └── events
            │       ├── train
            │       └── test
            └── xd-violence
                └── videos
                    ├── train
                    └── test
                └── clips
                    ├── train
                    └── test
                └── events
                    ├── train
                    └── test
```

Each `train/` and `test/` folder should contain the video files themselves (e.g., `.mp4`).

---

## ⚙️ Environment Setup

```bash
conda create -n hivau python=3.9 -y
conda activate hivau
pip install -r requirements.txt
```

---

## 🔧 How to Run

### 1. Data Download

There are three main ways to download the data. Choose one of the following:

* **Using Hugging Face**
  The datasets here are already preprocessed. You can skip the “3. Clip Splitting & Validation” step.

  ```bash
  git lfs install
  git clone https://huggingface.co/datasets/backseollgi/HIVAU-70k_UCF-Crime
  git clone https://huggingface.co/datasets/backseollgi/HIVAU-70k_XD-Violence
  ```

---

* **Manual Download**
  For stability, download the UCF-Crime and XD-Violence videos directly from their **official websites**.

---

* **Automated Script**
  Create the download directories and run the `.sh` scripts to attempt automatic download:

  ```bash
  mkdir -p src/videos/ucf-crime/videos
  mkdir -p src/videos/xd-violence/videos

  # Download and extract datasets
  bash ucf-crime.sh
  bash xd-violence.sh
  bash data_unzip.sh
  ```

  ⚠ **Note:** The `ucf-crime.sh` script may fail in some environments due to blocked requests or expired URLs. If it fails, please download manually from the [UCF-Crime website](https://www.crcv.ucf.edu/projects/real-world/).

---

### 2. Folder Organization

Arrange your files according to the structure shown above. If you used the terminal scripts, no further reorganization is needed.

---

### 3. Clip Splitting & Check

Run the following scripts to split videos into clips and validate the data:

```bash
cd src

# 1. Split videos (default: 12 threads)
python split_video.py
# (Optional: change number of threads)
python split_video.py --n_thread 4

# 2. Validate clips
python check_video.py
```

> 💡 This process can take several hours, depending on the number and length of videos.

---

## 📎 References

* This code is based on the **HIVAU-70k** benchmark structure proposed in the [HolmesVAU paper](https://arxiv.org/abs/2412.06171).
* For the full HolmesVAU functionality (model training, inference, etc.), please refer to the original repository:
  🔗 [https://github.com/pipixin321/HolmesVAU](https://github.com/pipixin321/HolmesVAU)

---

## 📜 License

* This code leverages public code and datasets (UCF-Crime, XD-Violence) and is intended solely for benchmark construction.
* Please adhere to the original code’s license and the datasets’ copyrights.
