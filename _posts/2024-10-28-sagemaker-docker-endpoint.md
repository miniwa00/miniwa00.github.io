---
title: "Docker Image를 SageMaker Endpoint로 배포하기"
date: 2024-10-28 17:00:00 +0900
categories: [AWS]
tags: [aws, sagemaker, docker, ecr, endpoint]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

SageMaker에서 직접 만든 Docker Image를 Endpoint로 배포하려면 ECR에 올린 이미지, SageMaker 모델, 엔드포인트 구성, 엔드포인트를 순서대로 연결해야 한다.

## 모델 생성

먼저 Custom Container로 사용할 Docker Image를 만들고 ECR에 push한다. 이후 SageMaker 콘솔에서 `추론 > 모델`로 이동해 모델 생성을 시작한다.

모델 생성 화면에서는 ECR 이미지 URI를 입력하고, SageMaker가 사용할 IAM 역할을 선택한다. 이 IAM 역할에는 SageMaker가 ECR 이미지를 읽고 필요한 네트워크 리소스에 접근할 수 있는 권한이 있어야 한다.

## 네트워크 설정

모델을 만들 때 VPC, 서브넷, 보안 그룹을 선택한다. 이때 선택한 서브넷의 네트워크 조건이 중요하다. 기록 당시에는 선택된 서브넷의 퍼블릭 IPv4 주소 자동 할당이 켜져 있어야 엔드포인트 생성 문제가 해결됐다.

네트워크 설정은 SageMaker 배포에서 자주 놓치기 쉬운 부분이다. 이미지와 모델 설정이 맞더라도 VPC, 서브넷, 보안 그룹, 라우팅 조건이 맞지 않으면 엔드포인트 생성 단계에서 실패할 수 있다.

## 엔드포인트 구성 생성

모델을 만든 뒤에는 `추론 > 엔드포인트 구성`으로 이동해 엔드포인트 구성을 만든다. 여기서 엔드포인트 구성 이름을 입력하고, 프로덕션 변형을 생성한다.

프로덕션 변형에서는 앞에서 만든 모델을 선택하고, 원하는 인스턴스 유형을 지정한다. 이 설정이 실제 endpoint가 어떤 모델을 어떤 인스턴스에서 serving할지 결정한다.

## 엔드포인트 생성

마지막으로 `추론 > 엔드포인트`로 이동해 엔드포인트를 생성한다. 엔드포인트 이름을 입력하고 앞에서 만든 엔드포인트 구성을 연결하면 SageMaker가 실제 serving endpoint를 준비한다.

```text
Docker Image
-> ECR
-> SageMaker Model
-> Endpoint Configuration
-> Endpoint
```

## 결론

Docker Image를 SageMaker Endpoint로 배포하는 과정은 단순히 이미지를 올리는 것으로 끝나지 않는다. 이미지 URI, IAM 역할, VPC 네트워크 설정, 엔드포인트 구성, 인스턴스 타입이 모두 이어져야 한다. 문제가 생기면 Docker보다 SageMaker 리소스 연결과 네트워크 조건을 먼저 확인하는 것이 좋다.
