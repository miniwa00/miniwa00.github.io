---
title: "[CES 2025] 젠슨 황 NVIDIA CEO 기조연설 직관 후기 (2)"
date: 2025-01-07 17:00:00 +/-TTTT
categories: [Essay]
tags: [ces2025, keynote, nvidia, grace blackwell, rtx, ai, gpu, nvidia digits, cosmos]
math: true
toc: true
published: true
author: Jongmin Kim
---

### **세 번째 주제 - Grace Blackwell NVLink 기반 슈퍼칩**

<center><img src="/assets/img/photos/jenson/8.jpg" alt="Description of image" width=400></center>

- **Grace Blackwell 슈퍼칩**  
젠슨 황은 Blackwell GPU를 기반으로 하는 새로운 슈퍼칩과 그 시스템을 소개했습니다. Grace Blackwell 슈퍼칩은 두 개의 고성능 Blackwell Tensor 코어 GPU와 하나의 Grace CPU를 통합하여 구성됩니다. 
> Grace CPU는 Nvidia가 자체적으로 데이터센터용 프로세서로 대규모 AI 및 고성능 컴퓨팅(HPC) 워크로드를 처리하기 위해 설계되었습니다. 최대 144개의 Arm Neoverse V2 코어를 탑재하여 복잡한 연산 작업을 효율적으로 처리할 수 있습니다.
특히 NVLink-C2C(Chip-to-Chip) 인터커넥트를 통해 각 구성 요소간에 900GB/s의 양방향 대역폭을 제공합니다. 

- **GB200 NVL72 시스템**  
Grace Blackwell 슈퍼칩을 기반으로 한 GB200 NVL72는 36개의 Grace CPU와 72개의 Blackwell GPU를 랙 스케일 디자인으로 연결한 시스템입니다.  
이 시스템은 1조 개의 매개변수를 가진 LLM의 실시간 추론을 기존 대비 30배 빠르게 수행할 수 있습니다. 

---

### **네 번째 주제 - Projects DIGITS**

<center><img src="/assets/img/photos/jenson/11.jpg" alt="Description of image" width=400></center>

- **개인용 AI 슈퍼컴퓨터, Project DIGITS**  
이어서 젠슨 황은 GB10 그레이스 블랙웰 슈퍼칩을 탑재한 Projects DIGITS를 공개했습니다. 이는 개인용 AI 슈퍼컴퓨터로, AI 연구자, 데이터 과학자, 학생들에게 고성능 컴퓨팅 환경을 제공합니다.  
  1. GB10 Grace Blackwell 슈퍼칩 탑재, 초당 천 조번의 연산 처리 가능
  2. 128GB 통합 메모리
  3. 최대 4TB NVMe SSD 지원
  4. 소프트웨어 지원:  
      a. NVIDIA NeMo 프레임워크: 모델 미세 조정 및 학습 최적화  
      b. NVIDIA RAPIDS: 데이터 과학 워크플로우 가속화  
      c. NVIDA NGC 카탈로그: 사전 학습된 모델과 오케스트레이션 도구 제공  

Project DIGITS는 개인 연구자나 학생들도 고성능 AI 슈퍼컴퓨터를 데스크톱 환경에서 활용할 수 있게 한다는 점에서 큰 의미를 지닙니다. 이는 AI 연구와 기술의 민주화에 크게 기여한다고 볼 수 있습니다. 물론 상대적으로 저렴해진 RTX 50 시리즈의 가격도 이런 흐름에 일조합니다.  

<center><img src="/assets/img/photos/jenson/12.jpg" alt="Description of image" width=400></center>

위 사진은 데스크톱 환경에 세팅된 DIGITS의 모습입니다.

---

### **다섯 번째 주제 - Physical AI를 위한 플랫폼, Cosmos**

<center><img src="/assets/img/photos/jenson/9.jpg" alt="Description of image" width=400></center>

- **Cosmos**  
  연설 막바지에 젠슨 황은 Physical AI 개발을 위한 새로운 플랫폼인 Cosmos를 소개했습니다. Cosmos는 로봇과 자율주행 차량 등 물리적 세계와 상호작용하는 AI 시스템을 가속화하기 위해 설계되었습니다. Cosmos에서는 물리 기반 합성 데이터를 생성하여 로봇이 현실 세계의 다양한 시나리오를 학습하고 테스트할 수 있도록 지원합니다.  
  <br>
  Cosmos는 World Foundation Model를 통해 물리적 환경의 모델링을 기반으로 로봇이 주변 세계를 이해하도록 돕습니다. Autoregression Model, Diffusion Model 등 다양한 베이스 모델을 사용하여 물리 환경 모델링을 지원합니다. 또한 엔비디아의 디지털 트윈 플랫폼인 Omniverse와 결합하여 다양한 시나리오에 대한 시뮬레이션과 테스트를 수행할 수 있습니다.  

젠슨 황은 "로보틱스를 위한 챗GPT 순간이 다가오고 있다"며 Cosmos가 Physical AI를 대중화하고 **모든 개발자가 일반 로보틱스를 활용할 수 있도록 지원**한다고 강조했습니다.

---

### **느낀 점**

엔비디아는 Agentic AI를 넘어 이미 Physical AI 시대를 바라보고 있었습니다. 이는 AI가 단지 소프트웨어로서만 존재하는 것이 아닌, 인간과 실제로 유기적으로 상호작용하는 개체로서의 존재 의미를 갖는다는 것입니다. 즉 공상과학 영화에서 쉽게 볼 수 있는 모습과 동일한 세상이 머지 않았음을 알 수 있습니다. 이런 상황에서 개인은 어떤 준비를 해야 할까요? 이런 세상에서 필요한 역량은 무엇이고, 어떤 마인드셋이 필요할까요? 이렇듯 젠슨 황의 기조연설은 많은 학생, 개발자, 연구자들에게 있어 엄청난 기회인 동시에 변화하는 세상에 대한 강한 경종입니다. 
