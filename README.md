# HIVAU-70k
HIVAU-70k, a large-scale benchmark for hierarchical video anomaly understanding across any granularity.


> 이 레포는 [HolmesVAU 공식 레포지토리](https://github.com/pipixin321/HolmesVAU)의 벤치마크 구축 방식 중, **UCF-Crime과 XD-Violence 기반의 HIVAU-70k 벤치마크 생성 코드만 분리**하여 정리한 것입니다.
> 모델 학습, 추론 코드 및 전체 프레임워크는 반드시 원본 레포를 참조해 주세요.

---

## 📌 개요

이 저장소는 HolmesVAU에서 제안한 **HIVAU-70k** 벤치마크 구축 방식을 참고하여,
다음 두 공개 데이터셋을 기반으로 영상 이상 탐지 벤치마크를 구축하는 방법을 제공합니다:

* [UCF-Crime](https://www.crcv.ucf.edu/projects/real-world/)
* [XD-Violence](https://roc-ng.github.io/XD-Violence/)

---

## 🗂 폴더 구조

아래와 같은 구조로 비디오 데이터를 정리해야 합니다:

```
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

각 `train/`, `test/` 폴더에는 영상 파일들이 직접 위치해야 합니다 (`.mp4` 등).

---

## ⚙️ 환경 세팅

```bash
conda create -n hivau python=3.9 -y
conda activate hivau
pip install -r requirements.txt
```

## 🔧 실행 방법

### 1. 데이터 다운로드

* **Huggingface 이용**
해당 레포는 전처리까지 완료된 데이터입니다. 3. 영상 분할 및 검증 -> 생략 가능
```bash
git lfs install
git clone https://huggingface.co/datasets/backseollgi/HIVAU-70k_XD-Violence
git clone https://huggingface.co/datasets/backseollgi/HIVAU-70k_XD-Violence
```
---
* **직접 다운로드**
  `UCF-Crime`과 `XD-Violence` 비디오는 각각 **공식 홈페이지**에서 수동으로 다운로드하는 것이 가장 안정적입니다.
---
* **터미널 스크립트 실행**
  아래 명령어로 다운로드 디렉터리를 만들고 `.sh` 스크립트를 실행해 자동 다운로드를 시도할 수 있습니다:

```bash
mkdir -p src/videos/ucf-crime/videos
mkdir -p src/videos/xd-violence/videos

# 데이터셋 다운로드 및 압축 해제
bash ucf-crime.sh
bash xd-violence.sh
bash data_unzip.sh

```

⚠ **주의:**
`ucf-crime.sh`는 **일부 환경에서 요청이 차단되거나 URL이 만료**되어 **실행이 실패할 수 있습니다**.
이 경우, [UCF-Crime](https://www.crcv.ucf.edu/projects/real-world/)에서 수동 다운로드를 진행해 주세요.

---

### 2. 폴더 정리

위에 명시한 폴더 구조에 따라 파일들을 정리합니다.
터미널 명령어로 다운받으셨다면 따로 파일을 정리하지 않아도 됩니다.

### 3. 영상 분할 및 검증

아래 스크립트를 실행하여 클립 단위로 영상을 분할하고, 데이터가 올바른지 확인합니다:

```bash
cd src
### 1.
# 영상 분할 (디폴트 스레드 12)
python split_video.py
# (옵션 변경 가능)
python split_video.py --n_thread 4

### 2.
python check_video.py
```

> 💡 이 과정은 수 시간 정도 소요될 수 있습니다. (영상 수와 길이에 따라 다름)

---

## 📎 참고

* 본 코드는 [HolmesVAU 논문](https://arxiv.org/abs/2412.06171)에서 제안된 **HIVAU-70k** 벤치마크 구조에 기반합니다.
* HolmesVAU 전체 기능 (모델 학습, 추론 등)이 필요할 경우, 반드시 원본 레포를 참조하세요:
  🔗 [https://github.com/pipixin321/HolmesVAU](https://github.com/pipixin321/HolmesVAU)

---

## 📜 라이선스 및 고지

* 본 코드의 기반은 공개된 코드 및 데이터셋(UCF-Crime, XD-Violence)을 활용한 것으로, 벤치마크 구축 목적에 한해 사용됩니다.
* 원본 코드의 라이선스와 데이터셋 저작권을 준수하여 사용해 주세요.

---

원하시면 위 README에 들어갈 이미지나 예시 결과도 함께 구성해 드릴 수 있습니다. 필요하시면 말씀 주세요!
