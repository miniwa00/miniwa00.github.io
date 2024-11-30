---
title: "Spring Boot 도커 이미지 ECS 수동 배포"
date: 2024-08-14 17:00:00 +/-TTTT
categories: [AWS]
tags: [aws, docker, ecs]
math: true
toc: true
published: true
author: Jongmin Kim
---

<a href="https://velog.io/@ekxk1234/ECS-체험기" target="_blank" title="ECS 체험기">참고: @ekxk1234 - ECS 체험기</a>

---


## **Application Setting**

- Spring Boot 실행을 위한 Java 설치
    - jdk 17 설치
        
        `brew install openjdk@17` 
        
    - 환경변수 설정
        
        `echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc` 
        
        `source ~/.zshrc` 
        
    - Java 설치 확인
        
        `java --version` 
        
- 만약 Application을 한번도 빌드한 적이 없다면 Jar 파일이 없을 것임. 따라서 앱을 한 번 빌드해 줘야 함.
    - `./gradlew clean build`
    - 빌드 이후에는 `./build/libs/` 안에 SNAPSHOT.jar 파일을 확인할 수 있음
    - `java -jar ./build/libs/project-name-SNAPSHOT.jar` 로 application 작동 확인
- Dockerfile 작성
    - `vi Dockerfile`
        
        ```jsx
        FROM openjdk:17-jdk-alpine3.13
        ARG JAR_FILE=./build/libs/project-name-SNAPSHOT.jar
        COPY ${JAR_FILE} app.jar
        ENTRYPOINT ["java","-jar","/app.jar"]
        ```
        
- Build Docker Image
    - `docker build -t githubsalt-ecr .`
    - 애플 실리콘의 경우 `docker build --platform linux/amd64 -t githubsalt-ecr .`
- Test Docker container running
    - `docker run -t githubsalt-ecr .`

---

## **VPC Setting**

- VPC 생성
    - 작은 규모에서 권장되는 CIDR 블록인 24블록 사용
    - NAT 게이트웨이는 생성하는 즉시 시간당 0.045$ 씩 과금이 발생하기 때문에 프라이빗 서브넷에 있는 리소스들이 외부 API 호출을 필요로 하는 순간에 켜줄 예
        
        ![image](/assets/img/photos/SpringBootECS/1.png)
        
- 보안 그룹 연결
    - Spring Boot Application이 사용하는 8080 포트랑 MySQL이 사용하는 3306 포트를 인바운드 규칙에 추가해줌
    - VPC ID가 이전에 생성한 VPC의 ID와 동일한지 확인
        
        ![image](/assets/img/photos/SpringBootECS/2.png)
        

---

## **ECR**

- 리포지토리 생성
    - 리포지토리 이름을 입력해줌
        
        ![image](/assets/img/photos/SpringBootECS/3.png)
        
- Push Docker image
    - 우측 푸시 명령 보기를 클릭
        
        ![image](/assets/img/photos/SpringBootECS/4.png)
        
    - 화면에 나온 명령어를 그대로 입력
        - 단 1번 명령어는 아래 명령어로 바꿔 입력 (aws cli가 설치돼있고 access key가 있다는 가정 하에 진행)
            
            ```jsx
            aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 565393031158.dkr.ecr.ap-northeast-2.amazonaws.com/githubsalt-ecr 
            ```
            
        
        ![image](/assets/img/photos/SpringBootECS/5.png)
        

---

## **ECS**

- 클러스터 생성
    - 우측 클러스터 생성 클릭
        
        ![image](/assets/img/photos/SpringBootECS/6.png)
        
    - 클러스터 정보 입력해서 클러스터 생성
        
        ![image](/assets/img/photos/SpringBootECS/cluster.png)
        
        - **AWS Fargate 설명**
            - **장점**
                - **서버 관리 불필요**: Fargate를 사용하면 EC2 인스턴스를 직접 관리할 필요가 없습니다. AWS가 인프라를 관리하므로, 운영 체제 업데이트, 패치, 스케일링 등 서버 관리 작업에서 벗어날 수 있습니다.
                - **자동 스케일링**: Fargate는 자동으로 필요한 리소스를 프로비저닝하고, 컨테이너의 수요에 따라 스케일링을 처리합니다. 이는 사용자가 직접 스케일링을 설정할 필요 없이 사용량에 따라 유연하게 대처할 수 있게 합니다.
                - **비용 최적화**: Fargate에서는 사용한 리소스에 대해서만 비용을 지불하므로, EC2와 비교했을 때 불필요한 리소스를 예약하거나 과도하게 프로비저닝할 필요가 없습니다. 이는 비용 절감에 도움이 됩니다.
                - **보안 강화**: 각 Fargate 작업은 자체 가상 네트워크 인터페이스와 보안 그룹을 가지며, 격리된 환경에서 실행됩니다. 이로 인해 작업 간의 보안 경계가 강화됩니다.
                - **단순성**: Fargate는 설정이 간단하며, 클러스터와 작업을 신속하게 설정하고 배포할 수 있습니다. 인프라 관리에 대한 복잡성을 줄이고 애플리케이션 코드에 집중할 수 있습니다.
            - **단점**
                - **비용**: 작은 규모의 애플리케이션이나 간헐적으로 사용되는 애플리케이션의 경우 비용이 절감될 수 있지만, 대규모로 지속적으로 실행되는 애플리케이션의 경우 EC2 인스턴스를 사용하는 것보다 비용이 더 많이 들 수 있습니다.
                - **제한된 커스터마이징**: EC2 인스턴스를 직접 관리하는 것과 달리, Fargate에서는 커널 수준의 설정이나 특정 하드웨어 요구 사항(예: GPU 지원) 등에 대한 제어가 제한됩니다. 복잡한 커스터마이징이 필요한 경우 EC2 기반의 ECS를 선택하는 것이 더 나을 수 있습니다.
                - **리소스 제한**: Fargate에는 제공하는 리소스(예: CPU, 메모리)에 제한이 있습니다. 이러한 제한 때문에 대규모의 고성능 애플리케이션에는 적합하지 않을 수 있습니다.
                - **네트워크 설정**: Fargate는 기본적으로 AWS VPC 내에서 실행되며, 이를 벗어난 복잡한 네트워크 설정이나 외부 통신 설정은 제한적일 수 있습니다.
            - **결론**
                - Fargate는 서버리스 환경에서 컨테이너를 쉽게 실행하고 관리할 수 있게 해주므로, 간단한 배포, 관리 편의성, 보안, 유연성을 원하는 경우에 적합합니다.
                - 그러나 대규모 애플리케이션을 장기적으로 실행하거나, 고도의 커스터마이징이 필요한 경우 EC2 기반의 ECS를 고려하는 것이 더 적합할 수 있습니다. 상황에 맞는 선택이 중요합니다.
- 태스크 정의 생성
    - 좌측 태스크 정의 클릭
        
        ![image](/assets/img/photos/SpringBootECS/7.png)
        
    - 새 태스크 정의 생성
        - 시작 유형은 AWS Fargate 선택
        - 태스크 크기는 최소 규모에 가까운 1 vCPU, 2GB 메모리로 설정
            - 이때 ‘태스크 크기’는 해당 태스크 정의를 따르는 모든 컨테이너들이 사용할 수 있는 리소스의 총량이다.
            
            ![image](/assets/img/photos/SpringBootECS/8.png)
            
        - 이미지 URI에는 ECR에 업로드한 이미지의 URI를 입력
            - **ECR에서 이미지 URI**
                
                ![image](/assets/img/photos/SpringBootECS/ecr.png)
                
        - 컨테이너 포트를 매핑
            - 8080: Spring Boot 포트
            - 3306: MySQL 포트
            
            ![image](/assets/img/photos/SpringBootECS/9.png)
            
        - 리소스 할당 제한이란?
            - 컨테이너 내에서 할당하고자 하는 리소스의 양
            - 태스크 전체의 리소스가 1 vCPU / 2GB 메모리이니 이를 초과할 수 없다.
- 클러스터 내 서비스 생성
    - 클러스터 안에서 우측 생성 클릭
        
        ![image](/assets/img/photos/SpringBootECS/10.png)
        
    - 생성할 서비스 구성
        - 아까 생성한 태스크 패밀리와 개정 버전을 선택
            
            ![image](/assets/img/photos/SpringBootECS/11.png)
            
        - 네트워킹 설정에서 사용할 VPC, 서브넷, 보안그룹을 선택
            - VPC를 생성할 때 NAT Gateway를 만들지 않았기 때문에 Public Subnet만 열어주면 된다.
            
            ![image](/assets/img/photos/SpringBootECS/12.png)
            
- 생성된 서비스 & 태스크 확인
    - 메인 화면
        
        ![image](/assets/img/photos/SpringBootECS/13.png)
        
    - 태스크
        
        ![image](/assets/img/photos/SpringBootECS/14.png)
        
    - 퍼블릭 IP:포트로 접근했을 때
        
        ![image](/assets/img/photos/SpringBootECS/15.png)
