---
title: "CatVTON 로컬 테스트"
date: 2024-10-11 17:00:00 +0900
categories: [AI]
tags: [catvton, virtual-try-on, python, cuda]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

## CatVTON을 선택한 이유

CatVTON은 가상 피팅 테스트를 위해 살펴본 모델 중 비교적 최신 업데이트가 반영된 모델이었다. 기록 당시 모델 업데이트가 활발했고, 1024x768 해상도 기준으로 8GB VRAM 이하에서도 동작할 수 있다는 설명이 있어 로컬 테스트 후보로 적합해 보였다.

또 하나의 장점은 masking AI가 함께 구성되어 있어 localized된 형태로 다루기 쉽다는 점이었다. 가상 피팅에서는 옷 영역을 얼마나 안정적으로 분리하고 합성하느냐가 중요하기 때문에, masking 흐름까지 함께 확인할 수 있는 모델이라는 점이 선택 이유가 됐다.

## 로컬 인퍼런스 준비

먼저 CatVTON repository를 clone한다.

```bash
git clone https://github.com/Zheng-Chong/CatVTON.git
```

이후 conda 환경을 만들고 필요한 패키지를 설치한다.

```bash
conda create -n catvton python=3.9
conda activate catvton
cd catvton
pip install -r requirements.txt
```

## Torch와 CUDA 확인

로컬에서 GPU 인퍼런스를 하려면 PyTorch가 CUDA를 제대로 인식하는지 확인해야 한다.

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

여기서 `torch.cuda.is_available()`가 `True`를 출력하면 CUDA가 정상적으로 연결된 것이다. 결과가 다르다면 설치된 torch 버전과 로컬 CUDA toolkit 버전이 맞는지 다시 확인해야 한다.

## 데이터 준비

인퍼런스 전에 입력 이미지와 의류 이미지, masking에 필요한 데이터를 준비해야 한다. CatVTON은 모델 실행 자체보다 입력 데이터의 형태와 경로를 맞추는 작업이 더 중요할 수 있다. 로컬 테스트에서는 먼저 작은 샘플로 전체 파이프라인이 동작하는지 확인한 뒤, 해상도와 배치 크기를 늘리는 편이 안정적이다.

## 결론

CatVTON 로컬 테스트의 핵심은 모델을 바로 크게 돌리는 것이 아니라, 환경과 입력 데이터를 먼저 작게 검증하는 것이다. CUDA 인식, dependency 설치, 샘플 데이터 구조가 맞아야 이후 masking과 try-on 결과를 의미 있게 비교할 수 있다.
