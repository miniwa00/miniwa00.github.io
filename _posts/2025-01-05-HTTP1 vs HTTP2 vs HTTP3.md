---
title: "HTTP 1 Vs HTTP 2 Vs HTTP 3"
date: 2025-01-05 15:00:00 +/-TTTT
categories: [Network]
tags: [http]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

> YouTube에서 ByteByteGo 채널의 'HTTP 1 Vs HTTP 2 Vs HTTP 3!' 비디오를 보고 내용을 정리했습니다.  
> 아래에 첨부된 사진들은 해당 비디오에서 발췌된 것임을 밝힙니다.  
> **영상 링크: <a href="https://youtu.be/UMwQjFzTQXw?si=HcBXt7ul1-_VqxeY" target="_blank" title="ByteByteGo - HTTP 1 Vs HTTP 2 Vs HTTP 3!">ByteByteGo - HTTP 1 Vs HTTP 2 Vs HTTP 3!</a>**

### HTTP란?
- HTTP(Hypertext Transfer Protocol)는 브라우저와 웹 서버가 소통하는 방법. 처음에는 하이퍼텍스트 문서(링크가 포함된 문서)를 전송하기 위해 설계되었지만, 지금은 이미지, 동영상, API, 파일 전송 등 다양한 웹 서비스를 지원함.

---

### HTTP 버전의 발전 과정
- HTTP 0.9 (1991):
  - 아주 단순했으며 GET 요청만 지원.
  - HTML 파일만 전송 가능, 헤더나 상태 코드 없음.
  <p style="text-align: center;"><img src="https://miniwa00.github.io/assets/img/photos/http/1.png" alt="Description of image" width=400 height=100></p>
<br> 

- HTTP 1.0 (1996):
  - 헤더, 상태 코드, POST/HEAD 메서드 추가.
  - 요청마다 새로운 연결(TCP 핸드셰이크)이 필요해 비효율적.
    1. TCP Handshake: TCP SYN, TCP SYN+ACK, TCP ACK
    2. Certificate Check: 서버로부터 Certification을 받는 과정
    3 . Key Exchange: 클라이언트와 서버간의 데이터를 암호화하기 위한 session key 생성 및 교환
    4. Data Transmission: 암호화된 데이터를 주고받음
  <p style="text-align: center;"><img src="/assets/img/photos/http/2.png" alt="Description of image" width=200 height=300></p>
<br>

- HTTP 1.1 (1997):  
  - **지속적 연결(Persistent Connections)** : 요청마다 연결을 끊지 않음.
  <p style="text-align: center;"><img src="/assets/img/photos/http/3.png" alt="Description of image" width=400 height=250></p>

  - **파이프라이닝(Pipelining)** : 한 연결에서 여러 요청을 연속적으로 보낼 수 있게 함.
  <p style="text-align: center;"><img src="/assets/img/photos/http/4.png" alt="Description of image" width=400 height=250></p>

  - **청크 전송 인코딩** : 비디오와 같은 큰 응답을 작은 단위로 나눠 전송 → 페이지 로드 속도 개선.
  <p style="text-align: center;"><img src="/assets/img/photos/http/5.png" alt="Description of image" width=400 height=150></p>

  - **캐싱 및 조건부 요청** : 불필요한 데이터 전송을 줄여 성능 향상.
    - 헤더에 Cache-Control이나 If-Modified-Since 등을 포함시켜 캐싱 구현
  <p style="text-align: center;"><img src="/assets/img/photos/http/6.png" alt="Description of image" width=400 height=200></p>

  - 하지만 **Head-of-Line Blocking 문제**가 여전히 존재.
  <p style="text-align: center;"><img src="/assets/img/photos/http/7.png" alt="Description of image" width=400 height=400></p>

    - Head-of-Line Blocking이란? 
      - 여러 요청이 동일한 연결이나 큐를 공유할 때, 앞선 요청 중 하나가 지연되거나 블록될 경우 뒤에 있는 다른 요청들이 그 요청이 처리되기를 기다리게되는 문제.
        1. 클라이언트가 여러 요청을 순차적으로 서버에 보냄 → 서버는 요청들을 처리하여 응답
        2. 빨간 화살표로 표시된 요청이 처리 시간이 길어지면서 지연 발생 → 그 결과, 이후의 요청들이 대기 상태에 들어감
   - 발생 이유
     - HTTP/1.1의 Pipelining은 요청을 직렬로 보내는 방식이라 앞선 요청이 블로킹되면 뒤의 요청도 대기한다.
   - 해결 트릭
     - **Domain Sharding**
       - 도메인 샤딩은 웹 브라우저의 병렬 HTTP 요청 수 제한을 우회하기 위해 여러 도메인(서브도메인 포함)을 활용하여 자원을 분산하는 기법
       - 작동 원리
         - HTTP/1.1에서는 일반적으로 한 도메인당 병렬 연결 수가 6개로 제한
         - 도메인 샤딩은 자원(이미지, CSS, JS 파일)을 여러 도메인에 분산 배치하여 병렬 요청 수를 늘림
         - 브라우저는 각각의 도메인에 대해 독립적으로 병렬 연결을 열기 때문에 요청이 분산되고 처리 속도가 빨라짐
       - 한계
         - 추가적인 DNS 조회로 인해 초기 로딩 시간이 약간 증가할 수 있음
     - **Asset Bundling**
       - 에셋 번들링은 여러 개의 파일을 하나의 파일로 묶어 요청 수를 줄이는 기법
       - Webpack, Vite, Parcel과 같은 번들링 도구를 사용하여 여러 JS 모듈을 하나의 파일로 번들링
       - HTTP 요청 수가 감소하여 네트워크 병목이 줄어듦 
       - 한계
         - 너무 큰 번들 파일은 브라우저 초기 렌더링 시간을 늘릴 수 있음
<br>

- HTTP 2 (2015):
  - 특징
    - **Single TCP Connection**
      - HTTP/2에서는 여러 요청과 응답이 하나의 TCP 연결에서 처리됨
      - 요청과 응답은 각각 **Strema**이라는 단위로 구분됨
        - Streamd은 HTTP/2 프로토콜의 논리적 채널로 각 요청/응답이 독립적으로 전송됨
    <p style="text-align: center;"><img src="/assets/img/photos/http/8.png" alt="Description of HTTP image" width=400 height=200></p>

    - **Binary Framing Layer**
      - HTTP/2는 데이터를 플레인 텍스트로 전송하는 HTTP/1.1과 다르게 데이터를 Binary Frame 형식으로 전송함
      - 요청/응답은 프레임으로 나뉘며, 각 프레임에는 Stream ID가 포함되어 어떤 요청/응답에 속하는지 식별함
    - **Multiflexing**
      - 요청/응답이 병렬로 처리됨
      - Stream ID를 통해 각각의 요청/응답이 독립적으로 전송되므로, 특정 요청의 지연이 다른 요청에 영향을 미치지 않음
      - **이는 HTTP/1.1에서 발생했던 Head-of-Line Blocking 문제를 해결함**
    - **Server Push**
      - 요청하지 않은 리소스를 미리 클라이언트에 전달.
    <p style="text-align: center;"><img src="/assets/img/photos/http/9.png" alt="Description of HTTP image" width=400 height=300></p>

    - **스트림 우선순위**
      - 중요 리소스를 먼저 로드하도록 설정 가능.
    - **헤더 압축**
      - HPACK이라는 알고리즘을 사용해 HTTP 헤더 크기를 줄여 성능을 최적화
  - 한계
    - **Retransmission(TCP 기반 패킷 재전송) 문제**
      1. 서버로 전송된 요청 중 일부 데이터(패킷)가 손실
      2. TCP는 신뢰성을 보장하기 위해 손실된 패킷을 다시 전송
      3. 이 과정에서 해당 연결의 모든 요청 처리가 지연될 수 있음
      <p style="text-align: center;"><img src="/assets/img/photos/http/10.png" alt="Description of HTTP image" width=300 height=300></p>
<br>

- HTTP 3 (2022):
    - TCP 대신 **QUIC(큐익)**을 사용하며 UDP 기반으로 설계 → 더 빠르고 안정적인 연결 제공.
    - 지연 시간 감소: QUIC과 TLS 핸드셰이크를 통합해 연결 설정 속도 향상.
    - 제로 라운드 트립 타임(0-RTT): 클라이언트가 서버와 과거에 연결된 적 있다면 초기 핸드셰이크 없이 데이터 전송 시작 가능.
    - 네트워크 변경(예: Wi-Fi → LTE)에도 연결 유지 → 모바일 환경에 적합.

---

### 추가 탐구 주제

1. HTTP/QUIC이란? QUIC이 웹 성능을 어떻게 개선하는지 살펴보기
2. TLS와 보안: HTTP 프로토콜에서 보안 핸드셰이크의 중요성
3. HTTP 3 채택의 과제: HTTP 3의 확산이 더딘 이유