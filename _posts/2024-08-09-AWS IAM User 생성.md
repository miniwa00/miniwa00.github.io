---
title: "AWS IAM User 생성"
date: 2024-08-09 17:00:00 +/-TTTT
categories: [AWS]
tags: [aws, iam]
math: true
toc: true
published: true
author: Jongmin Kim
---

### 처음에는 AWS Organization에 사용자를 추가하면 되는 줄 알았음
### **AWS Organization**
- **목적** 
  - 여러 aws 계정(루트, iam 포함)을 조직에 통합하고 중앙에서 관리할 수 있는 계정 관리 서비스. 계정 관리 및 통합 결제 기능을 지원하며, 기업의 예산, 보안 및 규정 준수 요구 사항 준수에 도움을 줄 수 있음. 조직 관리자로써 기존 계정 초대 또한 가능함.  
- **기능**
  -  모든 멤버 계정에 대한 통합 결제
      - 통합 결제에서 관리 계정은 조직에 속한 멤버 계저의 결제 정보, 계정 정보 및 계정 활동에 엑세스할 수도 있음.
  - 계정의 계층적 그룹화
      - 계정을 조직 단위(OU)로 그룹화하고 OU마다 다른 엑세스 정책을 연결할 수 있음.
  - 회사에서 필요한 권한이 다른 각 팀에 OU를 부여하고 결제를 통합적으로 관리하기에 적절함.
  - 각 계정은 독립적으로 각자의 활동을 할 수 있음.
    ![image](/photos/IAM/1.png){: width="700" height="400" }

---

### **AWS Identity and Access Management (IAM)**

- **목적**: AWS IAM은 개별 AWS 계정 내에서 사용자, 그룹, 역할 및 권한을 관리하는 데 사용됨. 이는 주로 보안 관점에서 AWS 리소스에 대한 접근 제어를 제공하는 데 중점을 .
- **기능**:
    - **사용자 및 그룹 관리**: AWS 계정 내에서 IAM 사용자를 생성하고 이들을 그룹화하여 관리할 수 있습니다.
    - **역할(Role) 관리**: 특정 작업을 수행할 수 있는 권한을 정의한 역할을 생성하고, 이를 IAM 사용자나 AWS 서비스에 부여할 수 있습니다.
    - **정책 관리**: JSON 기반의 정책을 사용하여 사용자, 그룹, 역할에 대한 구체적인 권한을 정의할 수 있습니다. 이를 통해 AWS 리소스에 대한 접근을 세밀하게 제어할 수 있습니다.
    - **연합(Federation)**: 외부의 사용자 디렉토리(예: Active Directory)와 연동하여 인증 및 권한을 관리할 수 있습니다.

### AWS Organization과 IAM의 차이

- **핵심 차이점**
    - **관리 범위**: AWS Organization은 여러 AWS 계정을 관리하는 데 중점을 두는 반면, IAM은 단일 AWS 계정 내에서 사용자 및 권한을 관리하는 데 중점을 둡니다.
    - **정책 적용**: Organization에서는 SCP를 통해 전체 계정에 대한 정책을 관리하고, IAM에서는 개별 사용자나 역할에 대해 상세한 권한을 부여합니다.

### IAM 사용자 등록 방법

1. 서비스에서 IAM 검색 후 접속
   ![image](/photos/IAM/2.png){: width="700" height="400" }
2. 좌측 사이드바에서 사용자 클릭 후 접속
   ![image](/photos/IAM/3.png){: width="700" height="400" }
3. 우측의 사용자 생성 클릭 후 사용자 세부 정보 지정
   ![image](/photos/IAM/4.png){: width="700" height="400" }
   - 이때 Identity Center에서 사용자 지정 - 권장을 누르게 되면 Identity Center에서 사용자를 생성하도록 안내함
   ![image](/photos/IAM/5.png){: width="700" height="150" }
   - Identity Center에서 생성된 사용자는 이메일로 전송된 access portal 링크를 통해서만 AWS 콘솔에 접근할 수 있음 (기존 로그인 방식으로는 접근 불가)
   - 기존 로그인 방식으로 IAM 유저 로그인을 하고 싶다면 위의 절차로 진행해야함.
4. 그룹이 있다면 그룹에 사용자를 추가하고 없다면 그룹을 생성해 줌
   ![image](/photos/IAM/6.png){: width="700" height="400" }
   - 그룹 생성 탭에서는 아래와 같이 그룹에 할당할 권한을 설정할 수 있음
   ![image](/photos/IAM/7.png){: width="700" height="400" }
5. 검토 및 생성을 진행함
   ![image](/photos/IAM/8.png){: width="700" height="400" }
6. csv 파일에는 최초 접속을 위한 아이디와 비밀번호가 담겨 있음 (이때가 비밀번호를 확인할 수 있는 유일한 시간이니 csv를 꼭 잘 저장해 놓자)
   ![image](/photos/IAM/9.png){: width="700" height="400" }
7. 이후 로그인을 위해서는 root 계정의 ID 12자리 수를 넣고 사용자 이름, 최초 암호를 입력하면 암호 재설정 이후 정상적으로 콘솔에 접근이 가능함.