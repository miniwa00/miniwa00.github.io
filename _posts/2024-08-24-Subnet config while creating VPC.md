---
title: "VPC 생성 시 서브넷 설정"
date: 2024-08-23 17:00:00 +/-TTTT
categories: [AWS]
tags: [aws, vpc, network, subnet]
math: true
toc: true
published: true
author: Jongmin Kim
---

### **VPC 안에서의 서브넷이란?**

VPC 내에서 특정 범위의 IP 주소를 사용하는 논리적인 네트워크 분할

- VPC(Virtual Private Cloud)
    - 기본적으로 인터넷과 격리된 AWS의 가상 네트워크
- 서브넷
    - 이 VPC 내에서 개별적으로 격리된 네트워크 세그먼트

---

### **서브넷은 특정 IP 주소 범위를 가짐**

예시: `10.0.1.0/24` 

- `10.0.1.0` : 서브넷의 시작 주소
- `/24` : 서브넷 마스크가 24비트 길이임을 의미
    - 서브넷 마스크는 `255.255.255.0` 이다.
    - 처음 세 옥텟(8비트씩 총 3세트)이 네트워크 부분이고, 나머지 8비트는 호스트 부분이다.
    - 네트워크 부분이 `10.0.1` 로 고정되며, 나머지 8비트는 자유롭게 설정할 수 있다.
- IP 주소 개수 계산
    - `/24` 에서는 8비트가 호스트 부분으로 사용되므로 256(2^8)가지의 값을 가질 수 있다.
    - **하지만 서브넷의 첫 번째 주소(`10.0.1.0`)는 네트워크 식별자로, 마지막 주소(`10.0.1.255`)는 브로드캐스트 주소로 예약되어 있다.**
    - **따라서 실제 사용할 수 있는 IP 주소는 254개(`10.0.1.1` ~`10.0.1.254`)이다.**
- 시작 주소(`10.0.1.0`)의 역할
    - 시작 주소(=네트워크 주소)는 해당 서브넷 전체를 나타내며, 네트워크 내의 개별 장치(EC2 인스턴스 등)를 식별하지 않는다.
    - 이 네트워크 주소는 주로 라우팅 테이블에서 서브넷을 식별하는데 사용된다.
- 호스트 부분(`/24`)의 역할
    - 호스트 부분은 서브넷 내에서 유일한 IP 주소를 가지도록 각 장치에 할당된다.
    - 즉 총 254개의 장치에 연결될 수 있다.
        - VPC 안의 서브넷에 연결될 수 있는 장치들
            - EC2 인스턴스
            - RDS 인스턴스
            - Lambda 함수
            - ECS
            - …
    - 적절한 호스트 부분의 선택
        - 큰 서비스일수록 더 많은 장치(호스트)가 서브넷 내에 존재할 수 있기 때문에 호스트 부분이 크게 할당되어야 한다.
            - **/24 서브넷 (`255.255.255.0`)**
                - 호스트 비트: 8비트
                - 최대 호스트 수: `2^8 - 2 = 254` (네트워크 및 브로드캐스트 주소 제외)
            - **/20 서브넷 (`255.255.240.0`)**
                - 호스트 비트: 12비트
                - 최대 호스트 수: `2^12 - 2 = 4094`
            - **/16 서브넷 (`255.255.0.0`)**
                - 호스트 비트: 16비트
                - 최대 호스트 수: `2^16 - 2 = 65,534`
        - 개발 단계나 작은 서비스는 `/26` 이나 `/28` 과 같은 작은 서브넷이 적합할 수 있음.

---

### **퍼블릭 서브넷과 프라이빗 서브넷**

- 퍼블릭 서브넷
    - 인터넷 게이트웨이(IGW)를 통해 인터넷과 직접적으로 연결될 수 있는 서브넷
    - 퍼블릭 서브넷에 있는 리소스들은 인터넷에 접근할 수 있고, 인터넷으로 나가는 트래픽을 허용할 수 있다.
    - **퍼블릭 서브넷에 배치된 리소스는 퍼블릭 IP 주소나 Elastic IP 주소를 할당받아 인터넷과 직접적으로 통신할 수 있다.**
    - 웹 서버, 로드 밸런서 등 외부와의 통신이 필요한 리소스들이 배치된다.
        - 예를 들어, 웹 애플리케이션의 프론트엔드 서버는 퍼블릭 서브넷에 배치되어야 사용자가 인터넷을 통해 접속할 수 있다.
- 프라이빗 서브넷
    - 인터넷과 직접적으로 연결되지 않은 서브넷
    - 프라이빗 서브넷에 있는 리소스들은 인터넷과의 직접적인 연결이 차단되며, 보안을 강화하기 위해 외부에서 접근이 필요 없는 리소스들을 배치하는데 사용된다.
    - 프라이빗 서브넷은 라우팅 테이블에 인터넷 게이트웨이에 대한 경로가 없다.
        
        ![image](/assets/img/photos/VPCSubnet/1.png)
        
    - 프라이빗 서브넷에 배치된 리소스는 프라이빗 IP 주소만을 가지며, 외부 인터넷으로부터 직접적인 접속이 불가하다.
        - 프라이빗 서브넷에 있는 리소스가 인터넷에 접근해야 하는 경우, NAT 게이트웨이나 NAT 인스턴스를 통해 가능하며, 이는 퍼블릭 서브넷에 위치하게 된다.
    - 데이터베이스 서버, 내부 애플리케이션 서버 등 보안이 중요한 리소스들이 배치된다.
        - RDS, 백엔드 서버 등
- 궁금증들
    1. 백엔드 서버의 Swagger 독스를 보고 싶다면 퍼블릭 서브넷을 써야하나?
        - 경우에 따라 다름
        - 퍼블릭 서브넷 사용
            - 백엔드 서버가 퍼블릭 서브넷에 있다면 인터넷을 통해 직접 접근할 수 있다.
            - 따라서 Swagger Docs를 인터넷에서 접근할 수 있도록 하려면 퍼블릭 서브넷에 배치하는 것이 필요
            - 이는 개발이나 테스트 환경에서 빠르게 접근하고자 할 때 유용하다.
        - 프라이빗 서브넷 사용
            - 백엔드 서버가 프라이빗 서브넷에 있다면 인터넷에서 직접 접근할 수 없다.
            - 이때 리버스 프록시를 통해 Swagger만 인터넷에 노출시킬 수 있다.                
    2. DBeaver를 통해 내 컴퓨터에서 DB를 보고 싶다면 퍼블릭 서브넷을 써야하나?
        - 프라이빗 서브넷에 두는 것이 일반적이며, 퍼블릭 서브넷에 두지 않는 것이 좋다.
        - RDS를 프라이빗 서브넷에 두고 Bastion Host를 통한 SSH 터널링으로도 DBeaver에서 DB에 접근할 수 있다.
            
---

### **비용**

- 퍼블릭 서브넷에서 igw 통해 인터넷 접근 VS 프라이빗 서브넷에서 nat gateway를 통해 인터넷 접근
    - **NAT 게이트웨이를 사용하는 경우가 일반적으로 더 비싸다.**
    - 인터넷 게이트웨이(IGW)
        - 인터넷 게이트웨이를 사용하는 것은 별도의 비용이 발생하지 않는다.
        - 인터넷 게이트웨이 자체는 무료로 제공되며, 퍼블릭 서브넷에서 외부와의 통신에 대해 데이터 전송 비용만 발생한다.
        - 사용 시 비용
            - **인바운드 트래픽**: 무료
            - **아웃바운드 트래픽**: 표준 데이터 전송 요금이 부과된다.
    - NAT 게이트웨이
        - NAT 게이트웨이는 사용 시간과 처리된 데이터 양에 따라 요금이 부과된다.
            - 시간당 요금: NAT 게이트웨이가 활성화된 시간에 대한 비용
            - 데이터 처리 요금: NAT 게이트웨이를 통해 전송되는 데이터에 대해서도 GB당 요금 부과
        - 사용 시 비용
            - **시간당 비용**: `us-east-1` 리전에서 NAT 게이트웨이 사용 시 시간당 $0.045의 요금이 부과.
            - **데이터 처리 비용**: GB당 $0.045 정도의 요금이 추가로 부과.
- 한 VPC 안의 ECS에서 실행중인 프론트엔드 서버와 백엔드 서버 간의 통신
    - **이는 프라이빗 서브넷 간의 통신으로 간주된다.**
    - 프라이빗 서브넷 간의 통신
        - 같은 VPC 내에서, 특히 프라이빗 서브넷 간의 통신은 AWS 내부 네트워크를 통해 이루어진다.
        - 이 통신은 일반적으로 라우팅 테이블을 통해 관리되며, IGW나 NAT 게이트웨이를 거치지 않는다.
        - 이 통신은 외부 인터넷을 거치지 않기 때문에 네트워크 트래픽이 AWS 네트워크 내에서만 이동하며, 보안적으로도 우수하다.
    - 비용이 발생하지 않음
        - **같은 VPC 내의 서브넷 간 통신에서는 데이터 전송에 대한 추가 비용이 발생하지 않는다.**

---

### **Lambda를 VPC 안에 위치시키는 게 나을까?**

- 람다를 퍼블릭 서브넷에 배치하는 것이 가능한가?
    
    Lambda 함수는 퍼블릭 서브넷에 배치하기는 힘들다.
    
    1. **인터넷 접근성**:
        - **Lambda 함수가 퍼블릭 서브넷에 배치되더라도, Lambda 함수 자체는 퍼블릭 IP를 할당받지 않으므로, 인터넷 게이트웨이를 통해 직접 인터넷에 접근할 수 없습니다.**
        - Lambda가 인터넷에 접근해야 한다면, 퍼블릭 서브넷 대신 **프라이빗 서브넷에 NAT 게이트웨이**를 사용하거나, **퍼블릭 서브넷에 NAT 인스턴스**를 설정하여 인터넷에 접근할 수 있도록 해야 합니다.
    2. **VPC와 서브넷 선택**:
        - Lambda 함수가 VPC에 연결되면, 지정된 서브넷 내의 네트워크 리소스에 접근할 수 있습니다. 퍼블릭 서브넷에 연결된 Lambda 함수는 해당 서브넷 내의 리소스에 접근할 수 있지만, 외부 인터넷에 직접적으로 접근하려면 NAT 게이트웨이나 NAT 인스턴스가 필요합니다.
    3. **보안 고려사항**:
        - Lambda 함수를 퍼블릭 서브넷에 배치하는 것은 일반적으로 **권장되지 않습니다**. Lambda 함수가 외부 인터넷과 상호작용해야 하는 경우, NAT 게이트웨이와 프라이빗 서브넷을 사용하는 것이 일반적인 패턴입니다. 이렇게 하면 Lambda 함수는 VPC 내의 리소스에 접근하면서도 외부 인터넷에 대한 안전한 접근을 보장할 수 있습니다.
- VPC 밖의 람다가 ECS 안의 서비스에 접근할 때 발생하는 비용
    
    1. **Lambda 호출 비용**
    
    - **Lambda 호출 비용**: Lambda 함수 호출 시, 요청에 따라 호출 비용이 발생합니다. AWS Lambda는 호출 횟수와 함수 실행 시간을 기준으로 요금을 부과합니다.
        - **요청당 비용**: 1백만 건의 요청당 $0.20가 부과됩니다.
        - **함수 실행 시간 비용**: 함수가 실행된 시간(GB-초)에 따라 요금이 부과됩니다. 실행 시간과 메모리 크기에 따라 비용이 다릅니다.
    - **데이터 전송 비용**: Lambda가 호출된 후 반환되는 데이터 양에 따라 추가 비용이 발생할 수 있습니다. 그러나 Lambda 함수가 VPC 밖에 있다면, 이 데이터 전송에 대한 비용은 크게 신경 쓰지 않아도 됩니다.
    
    2. **데이터 전송 비용**
    
    - **인터넷 데이터 전송 비용**: VPC 내의 ECS 인스턴스에서 인터넷을 통해 Lambda 함수를 호출할 때, AWS는 아웃바운드 트래픽에 대해 요금을 부과할 수 있습니다.
        - **아웃바운드 데이터 전송 비용**: VPC 내에서 Lambda 함수로 전송되는 데이터(인터넷을 통해 나가는 트래픽)에 대해 비용이 부과됩니다. 이 비용은 GB당 약 $0.09(첫 10TB까지)입니다.
    - **인바운드 데이터 전송 비용**: Lambda 함수가 응답으로 ECS 인스턴스에 데이터를 반환할 때, 일반적으로 인바운드 트래픽(인터넷에서 들어오는 트래픽)에 대해서는 비용이 발생하지 않습니다.
    
    3. **NAT 게이트웨이 비용 (ECS가 프라이빗 서브넷에 있을 경우)**
    
    - 만약 ECS 인스턴스가 프라이빗 서브넷에 있고, NAT 게이트웨이를 통해 Lambda 함수를 호출하는 경우, NAT 게이트웨이를 사용하는 데 추가 비용이 발생할 수 있습니다.
        - **NAT 게이트웨이 비용**: 시간당 요금(예: $0.045/시간)과 데이터 처리 요금(예: GB당 $0.045)이 부과됩니다.
- VPC 밖의 람다에서 S3로의 데이터 저장
    
    Lambda 함수가 VPC 밖에서 실행되고, 이 Lambda 함수가 `boto3`를 사용하여 S3 버킷에 이미지를 저장하는 경우, **아웃바운드 트래픽에 대한 비용은 발생하지 않습니다**.
    
    이유:
    
    - **Lambda와 S3는 AWS의 글로벌 인프라 내에서 상호작용**: Lambda 함수가 VPC 밖에 있다면, 기본적으로 AWS의 공용 네트워크에서 실행됩니다. 이 경우 Lambda 함수와 S3 간의 통신은 AWS 내부 네트워크에서 이루어지며, 이 내부 트래픽에 대해 데이터 전송 비용은 부과되지 않습니다.
    - **S3에 데이터를 업로드하는 비용**: S3에 데이터를 업로드하는 데는 데이터 전송 비용이 발생하지 않습니다. S3로의 데이터 전송(업로드)은 무료입니다. 단, S3에서 데이터를 다운로드하거나 S3에서 외부로 데이터를 전송할 때는 데이터 전송 비용이 발생할 수 있습니다.
    
    비용 발생 여부:
    
    - **Lambda 실행 비용**: Lambda 함수를 호출하고 실행하는 데 대한 비용(요청 수 및 실행 시간에 따라)이 발생합니다.
    - **S3 스토리지 비용**: S3에 이미지를 저장할 때, 저장 용량에 따라 스토리지 비용이 발생합니다.
    - **데이터 업로드 비용**: Lambda 함수에서 S3로 데이터를 업로드하는 과정에서는 추가적인 아웃바운드 데이터 전송 비용이 발생하지 않습니다.