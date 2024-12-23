---
title: "SFAW 전시회 회고"
date: 2024-03-30 17:00:00 +/-TTTT
categories: [Essay]
tags: [sfaw, listening, customer success, customer satisfaction]
math: true
toc: true
published: true
author: Jongmin Kim
---

## 관람객들을 감동시키는 방법

저는 2024년 3월에 SFAW 전시회에서 인턴쉽을 진행했던 회사의 플랫폼과 서비스를 소개하면서 많은 관람객들과 소통할 수 있는 기회를 가졌습니다. 그 과정에서 깨달은 점과 향후 개선해야 할 사항들에 대해 공유하고자 합니다.😊

---
### 고객 응대 타임라인

- **고객 응대 초기**:
	- 설명을 시작한지 얼마 되지 않았을 때에는 관람객에게 숨 쉴 틈을 주지 않고 제가 해야 할 말만 계속 늘어놓았습니다. 말이 너무 빠르고 내용이 정립되지 않아서 관람객 입장에서 상당히 부담스러웠을 것입니다. 또한 몸이 불안하게 너무 좌우로 흔들린다는 피드백을 받았습니다.
<br><br>
- **익숙해진 후**: 
    - 동료의 조언을 받아들여 말을 천천히 하고자 노력했습니다. 또한 설명해야 할 레퍼토리가 대강 정립되어 데모 애플리케이션에 대해 말하는 것 자체에는 큰 어려움은 없었습니다. 그러나 여전히 '이 데모가 어떻게 돌아가고, 이것들을 플랫폼에서 할 수 있다!'만 강조했기 때문에, 관람객 입장에서는 공감이 잘 되지 않았을 수도 있습니다.
<br>
    - **대화가 잘 통했던 고객**
      1. 그러나 몇몇 관람객은 티키타카가 잘 됐고, 그런 관람객의 특징은 일단 우리가 데모에서 풀어낸 솔루션이 자신들의 고민거리와 직결되어 있었습니다. 특정한 공간에서의 복장, 행동, 현상 디텍션과 관련된 고민이 있는 관람객들과는 이야기가 잘 통했습니다. 이런 관람객들은 대체로 라벨링부터 큐레이트, 모델로 이어지는 이전 회사 플랫폼 전반에 대한 호기심을 강하게 보였고, CAL(Custom Auto Label)을 활용한 라벨링 비용의 절감, 모델 배포 후 약점과 추가적인 요청에 대해서도 빠른 대응이 가능하다는 점에 크게 감동했습니다. 
      2. 그 다음으로 이야기가 잘 통했던 관람객들은 어떤 공정에서 부품들의 불량을 탐지하는 과정에서의 디텍션과 관련된 고민을 가지고 있었습니다. 이 경우에는 PCB 프로젝트가 매우 주요하게 먹혔습니다. PCB 프로젝트를 통해서 다양한 부품들에 대해서 높은 정확도로 디텍션이 가능하다는 것에 놀라워 했고, 기존의 룰베이스 방식과 비교해 비전 AI도 성능이 많이 좋아졌다고 평가했습니다. 또한 이것도 마찬가지로 다양한 시나리오와 관람객의 요청에 빠른 대응이 가능하다는 부분에 크게 감동했습니다. 이 말은 다르게 표현하면 실제 use-case에 대해 관람객들을 설득 가능하고 그것이 관람객들이 감동하는 포인트라는 것입니다. 따라서 미리 예측 가능한 모든 use-case에 대해 테넌트에 세팅을 했으면 지금보다 훨씬 더 많은 관람객들에게 플랫폼 내부까지 시연할 수 있었을 것으로 생각합니다.
<br>
    - **중요한 감동 포인트**:
    	1. CAL을 활용한 라벨링 비용 절감은 관람객이 라벨링 시 발생하는 인건비와 오랜 소요 시간 등에 대해 깊은 고민을 하고 있음을 알 수 있습니다.
    	2. 적은 데이터 수량임에도 높은 precision & recall을 보여준 것은, mAP라는 다소 복잡한 평가지표보다 대부분이 이해하고 있는 정밀도와 재현율을 기반으로 모델의 우수함을 설명했을 때 놀라워하는 반응이 많았습니다.
    	3. 모델 재학습의 용이성과 빠른 대응 가능성은, 데모용 모델을 제작할 때 소요된 MLOps 시간이 8시간 이내임을 강조함으로써 실제로 어떻게 가능한지를 플랫폼을 시연하면서 설명했을 때 주요하게 감동했습니다.
    	4. 관람객들은 순전히 '라벨링 이후 모델 학습'이라는 컨텍스트로 이해했습니다. 이는 큐레이트의 유용한 기능까지 설명하기에는 살짝 아쉬웠습니다. 제가 당시에 설명을 할 때는 결국 관람객이 묻고 싶은 것은 '얼마나 빠르고 정확한가?'라고 생각했습니다. 따라서 큐레이트의 좋은 기능들도 어떻게 간략하고 압축적으로 설명할 수 있을지 고민해야 합니다. 라벨링 후 학습이 가능하다는 맥락에서 갑자기 what to label이나 scatter view를 설명하기에 굉장히 애매하다는 의미입니다.
<br><br>
- **설명이 상당히 익숙해졌을 때**:
	- 가장 먼저 회사에 대해 들어봤는지, ML에 대한 이해도가 높은지를 물어봤습니다. 제 생각에 회사를 아는지에 대한 질문은 크게 의미가 없었습니다. 어차피 대부분 모르고 있습니다. ML에 대한 이해도는 대체로 조금 있는 수준이었습니다. 제가 하는 말을 전혀 이해하지는 못할 정도는 아니었습니다. 따라서 모델에 대한 자세한 정보, 비전 AI의 주요 담론 등에 대해서 딥하게 설명하기보다는 MLOps에 대해 개괄적으로 설명해 주었고, 비전 AI의 특성, 객체 검출 등의 기본적인 내용을 궁금해 하실 때만 답을 드렸습니다. 그 이후 조직 내부에서 비전 AI로 해결하고자 하는 문제가 있는지 물어보았습니다. 만약 풀고자 하는 문제가 데모에서 하는 것과 비슷하다면 위와 같이 이야기가 잘 통했고, 그것이 아니어도 관람객의 이야기를 들으면서 우리가 생각할 때 가능하다고 판단되는 것들과 관람객들의 이야기를 잘 융합하고자 했습니다. 간혹 관람객의 고민이 잘 와닿지 않거나 이해가 안 되는 경우가 있었는데 그랬을 때 마찬가지로 관람객들도 별 만족 없이 돌아갔던 것 같습니다.
<br>
    - **가장 중요한 것은 관람객의 고민을 듣는 것입니다**. 그것을 통해 이러한 문제가 현장에서 발생하고 있음을 깨닫는 것이 중요합니다. 생각보다 많은 관람객들이 문제를 안고 있었고 그 중 대다수는 현재 우리의 기술로도 쉽게 풀 수 있다고 판단이 들었습니다. 그때는 자신 있게 충분히 해결 가능한 문제라고 말을 해주는 것도 관람객을 만족시키는 좋은 행동이라고 생각합니다. 다만 아쉬웠던 것은 좋은 경험의 관람객에게 명함을 많이 전달하지 못한 것입니다. 무조건 많이 뿌려야 합니다!
<br>
    - **초점을 Gradio가 아닌 OpenCV에 두어야 관람객의 경험이 훨씬 좋아진다는 것을 느꼈습니다**. Gradio는 그냥 솔루션의 한 예라는 것으로 간략하게 설명하고 OpenCV에서 어떻게 실제로 디텍션이 되는지를 강조하는 것이 중요할 것 같습니다. 관람객은 디텍션만으로도 매우매우매우 신기해합니다! 화룡점정으로 '사실 이런 디텍션은 다른 회사도 다 하지만, 이 결과물을 위한 공수가 매우 많이 든다. 그러나 우리의 플랫폼을 사용하면 이런 것에 사용되는 모델 쯤이야 엄청 빨리 만들 수 있다!'를 강조해야 합니다. 뭐, 중대재해 이런 배경은 필요 없다는 생각이 듭니다. 결국 Gradio는.. 왼손은 거들 뿐 전략.. 무릎을 굽힌 것은 추진력을 얻기 위한 전략.. 인터랙티브하고 액티브함을 무기로 한 관람객 유입용 사탕입니다!
<br>