---
title: "[Omoip] Bastion Host를 통해 RDS 인스턴스에 접근하는 방법"
date: 2024-08-16 17:00:00 +0900
categories: [AWS]
tags: [aws, rds, bastion-host, ssh-tunnel, dbeaver]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

RDS를 프라이빗 서브넷에 두면 외부에서 직접 접근할 수 없다. 하지만 Bastion Host와 SSH 터널링을 사용하면 RDS를 퍼블릭하게 열지 않고도 로컬 DBeaver에서 안전하게 접속할 수 있다.

## Bastion Host 생성

먼저 퍼블릭 서브넷에 EC2 인스턴스를 하나 만든다. 이 인스턴스가 Bastion Host 역할을 한다.

EC2를 만들 때는 다음 설정을 확인한다.

- 퍼블릭 서브넷 선택
- Public IP 자동 할당 활성화
- SSH 22번 포트를 내 IP에서만 허용
- 키 페어 생성 또는 기존 키 페어 선택

Bastion Host는 외부에서 들어갈 수 있는 입구 역할만 하므로, 작은 인스턴스 타입으로도 충분한 경우가 많다.

## SSH 터널링 설정

로컬 컴퓨터에서 다음 명령으로 SSH 터널을 연다.

```bash
ssh -i "your-key.pem" -L 3307:rds-endpoint:3306 ec2-user@bastion-host-public-ip
```

각 값의 의미는 다음과 같다.

- `your-key.pem`: Bastion Host 접속에 사용할 SSH 키
- `3307`: 로컬 컴퓨터에서 열 포트
- `rds-endpoint`: RDS 인스턴스 엔드포인트
- `3306`: RDS가 사용하는 포트, MySQL 기준
- `bastion-host-public-ip`: Bastion Host의 퍼블릭 IP

이 명령을 실행한 터미널은 닫지 않아야 한다. 세션이 살아 있는 동안 로컬의 `localhost:3307`로 들어온 트래픽이 Bastion Host를 거쳐 RDS로 전달된다.

## DBeaver 연결

DBeaver에서는 새 데이터베이스 연결을 만들고 Host와 Port를 다음처럼 설정한다.

```text
Host: localhost
Port: 3307
```

Database 이름, Username, Password는 RDS에 설정한 값을 입력한다. 이후 Test Connection을 실행해 연결을 확인한다.

## 보안 그룹 확인

RDS 보안 그룹은 Bastion Host에서 오는 트래픽을 허용해야 한다. 가능하면 Bastion Host의 보안 그룹을 source로 지정하는 방식이 좋다. 이렇게 하면 Bastion Host를 거치지 않는 외부 접근은 차단할 수 있다.

## 결론

Bastion Host를 통한 SSH 터널링은 RDS를 프라이빗 서브넷에 유지하면서도 로컬 개발 도구에서 접근할 수 있는 실용적인 방법이다. 핵심은 RDS를 직접 열지 않고, 접근 경로를 Bastion Host 하나로 좁히는 것이다.
