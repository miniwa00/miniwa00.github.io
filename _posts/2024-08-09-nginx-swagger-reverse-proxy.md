---
title: "NGINX로 Swagger만 외부에 노출하기"
date: 2024-08-09 17:00:00 +0900
categories: [AWS]
tags: [nginx, swagger, reverse-proxy, vpc, security]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

백엔드 서버를 프라이빗 서브넷에 두면 인터넷에서 직접 접근할 수 없다. 이 구조는 보안에는 좋지만, 개발이나 협업 과정에서 Swagger 문서만 외부에서 보고 싶을 때 불편할 수 있다.

이때 리버스 프록시를 사용하면 Swagger 경로만 제한적으로 외부에 노출할 수 있다.

## 리버스 프록시란

리버스 프록시는 클라이언트 요청을 받아 백엔드 서버로 전달하고, 백엔드 서버의 응답을 다시 클라이언트에게 전달하는 중간 서버다. NGINX나 Apache가 대표적인 리버스 프록시로 사용된다.

리버스 프록시는 보안, 로드 밸런싱, 캐싱, SSL 종료 같은 목적으로 자주 쓰인다.

## Swagger만 노출하는 구조

백엔드 서버는 프라이빗 서브넷에 그대로 두고, 퍼블릭 서브넷에 NGINX 서버를 배치한다. 외부 사용자는 NGINX에만 접근하고, NGINX는 특정 경로만 프라이빗 백엔드 서버로 전달한다.

예를 들어 `/swagger/` 경로만 백엔드로 프록시하도록 설정할 수 있다.

```nginx
server {
    listen 80;

    server_name your-public-domain.com;

    location /swagger/ {
        proxy_pass http://private-backend-server-ip/swagger/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 보안 그룹 설정

NGINX 서버의 보안 그룹에는 외부에서 필요한 포트만 열어둔다. 일반적으로 HTTP 80 또는 HTTPS 443만 허용한다.

백엔드 서버의 보안 그룹은 더 중요하다. 백엔드는 외부 전체가 아니라 NGINX 서버에서 오는 요청만 허용해야 한다. 그래야 Swagger 문서 접근은 가능하지만 백엔드 서버 자체는 인터넷에 직접 노출되지 않는다.

## 장점과 주의점

이 구조의 장점은 백엔드 서버를 프라이빗 서브넷에 유지하면서도 필요한 문서만 제한적으로 공개할 수 있다는 점이다. 또한 NGINX에서 IP 제한, 인증, HTTPS 설정을 추가하면 Swagger 접근도 더 세밀하게 제어할 수 있다.

다만 리버스 프록시 서버를 별도로 운영해야 하므로 인프라 복잡성은 증가한다. 프록시 서버가 중간에 들어가기 때문에 성능과 장애 지점도 함께 고려해야 한다.

## 결론

Swagger를 보기 위해 백엔드 서버 전체를 퍼블릭 서브넷에 둘 필요는 없다. NGINX 리버스 프록시를 사용하면 프라이빗 백엔드 구조를 유지하면서도 Swagger 같은 특정 경로만 외부에 노출할 수 있다.
