---
title: "masking Lambda 생성"
date: 2024-08-22 17:00:00 +/-TTTT
categories: [AWS]
tags: [aws, docker, ecr, ecs, lambda]
math: true
toc: true
published: true
author: Jongmin Kim
---

<a href="https://velog.io/@ironkey/AWS-Lambda를-Docker로-구축하기" target="_blank" title="ECS 체험기">참고: @ironkey - AWS Lambda를 Docker로 구축하기</a>

---

### **Lambda를 Docker로 구축하는 이유**

1. 서비스에 필요한 리소스 용량이 커져도 구축 가능하다.
    - Lambda의 기본 제한 용량은 250MB입니다. 이는 tensorflow와 같은 고용량 라이브러리르 포함하는 경우 문제를 발생시킵니다.
    - Docker를 이용하면 최대 10GB의 컨테이너 이미지까지 배포할 수 있어 해당 문제점을 극복할 수 있습니다.
2. 이미지 단위로 관리가 용이하다
    - Docker가 가지고 있는 일반적인 장점입니다.
    - github로 소스의 버전을 관리하듯 Docker Image로 서비스를 버전관리 할 수 있습니다.

---

### **repository 분리**

1. 기존 CatVTON 리포지토리에서 preprocess_agnostic_mask.py와 참조 폴더들을 분리
    
    ![image](/assets/img/photos/maskingLambdaDocker/1.png)
    
2. agnostic_mask.py를 **“유저 이미지 입력 → 5개의 masking 결과 반환”** 형태로 수정
    
    ```jsx
    for cloth_type in ["upper", "lower", "overall", "inner", "outer"]:
        get_mask(
            image=img,
            cloth_type=cloth_type,
            username=username,
            start_timestamp=start_timestamp,
        )
    ```
    
3. 생성된 5개의 masking 이미지들을 s3 버킷에 저장
    - 유저 이름 아래에 생성된 시간별로 저장하여 추후에 이전의 마스킹을 불러오는 경우에도 대응가능하도록 작성
    
    ```jsx
    s3 = boto3.client(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    
    def save_and_upload_s3(mask, username, cloth_type, start_timestamp):
    
        output_dir = "/tmp/mask_results"
        os.makedirs(output_dir, exist_ok=True)
    
        # timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        new_image_name = f"{username}_{start_timestamp}_{cloth_type}.png"
        mask.save(os.path.join(output_dir, new_image_name))
    
        filename = os.path.join(output_dir, new_image_name)
        bucket_name = "githubsalt-bucket"
        object_name = f"{username}/{start_timestamp}/{cloth_type}.png"
    
        s3.upload_file(filename, bucket_name, object_name)
    ```
    
4. Lambda에서 호출 가능한 handler 작성
    - input으로 username과 base64로 인코딩된 이미지를 받음
    - return으로 "Hello, {username}"이라는 문자열 반환
    
    ```jsx
    def handler(event, context):
        start = time.time()
        start_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    
        body = event["body-json"]
    
        username = body["username"]
        img = body["img"]
    
        for cloth_type in ["upper", "lower", "overall", "inner", "outer"]:
            get_mask(
                image=img,
                cloth_type=cloth_type,
                username=username,
                start_timestamp=start_timestamp,
            )
    
        result = f"Hello, {username}"
    
        print("Time taken: ", time.time() - start)
    
        return {"statusCode": 200, "body": json.dumps(result)}
    ```
    

---

### **Dockerfile 작성**

- **Dockerfile**
    
    ```docker
    FROM amazon/aws-lambda-python:3.9
    
    # Lambda 작업 디렉토리로 설정 (기본적으로 /var/task)
    WORKDIR /var/task
    
    # pip 업그레이드
    RUN /var/lang/bin/python3.9 -m pip install --upgrade pip
    
    # 필요한 시스템 패키지 설치 (OpenGL 라이브러리 포함)
    RUN yum install -y \
        mesa-libGL \
        mesa-libGL-devel \
        libXtst \
        libXrender \
        libXext
    
    # 로컬 디렉토리의 모든 파일을 Lambda 작업 디렉토리로 복사
    COPY . /var/task
    
    # 필요한 Python 패키지 설치
    RUN pip install -r requirements.txt
    
    # CMD 설정 (핸들러 함수 위치)
    CMD ["agnostic_mask.handler"]
    ```
    
    1. `FROM amazon/aws-lambda-python:3.9` 
        - 베이스 이미지로 Python 3.9 환경을 제공하는 AWS Lambda 기본 이미지를 사용
    2. `WORKDIR /var/task` 
        - Docker 컨테이너 내의 작업 디렉토리를 `/var/task` 로 설정
    3. `RUN /var/lang/bin/python3.9 -m pip install --upgrade pip` 
        - pip를 최신 버전으로 업그레이드
    4. `RUN yum install -y ~` 
        - OpenGL 라이브러리(`mesa-libGL`, `mesa-libGL-devel`)와 X11 라이브러리(`libXtst`, `libXrender`, `libXext`)를 설치
        - maksing된 이미지를 저장하는데 꼭 필요한 라이브러리
    5. `COPY . /var/task` 
        - 로컬 머신의 현재 디렉토리에 있는 모든 파일을 컨테이너 내의 `/var/task` 디렉토리로 복사
    6. `RUN pip install -r requirements.txt` 
        - `requirements.txt` 파일에 명시된 모든 Python 패키지를 설치
    7. `CMD ["agnostic_mask.handler"]`
        - Docker 컨테이너가 실행될 때 기본적으로 실행될 명령을 설정
        - 이 명렁은 Lambda 함수가 실행될 때 호출될 함수로, `agnostic_mask.py` 파일 내의 `handler` 함수를 지정

---

### **이미지 빌드 및 ECR에 푸시**

![image](/assets/img/photos/maskingLambdaDocker/2.png)

---

### **Lambda 함수 생성**

1. 우측 함수 생성 클릭
    
    ![image](/assets/img/photos/maskingLambdaDocker/3.png)
    
2. **컨테이너 이미지** 옵션 선택, 이름 입력
    
    ![image](/assets/img/photos/maskingLambdaDocker/4.png)
    
3. **이미지 찾아보기** 클릭 후 이미지 선택
    
    ![image](/assets/img/photos/maskingLambdaDocker/5.png)
    
4. 생성된 함수 확인
    
    ![image](/assets/img/photos/maskingLambdaDocker/6.png)
    

---

### **함수 로컬 테스트 & 클라우드 테스트**

1. 기존에 빌드된 Docker 이미지를 사용
2. 터미널에서 직접 Docker 컨테이너를 run
    - 로컬의 9000번 포트를 컨테이너의 8080 포트에 매핑
    
    ```jsx
    docker run --rm -p 9000:8080 masking-ecr
    ```
    
3. Postman에서 Lambda의 엔드포인트로 post 요청 전송
    - 엔드포인트: [`http://localhost:9000/2015-03-31/functions/function/invocations`](http://localhost:9000/2015-03-31/functions/function/invocations)
    - header와 body에 적절한 값(테스트 이벤트 json과 동일한 형식)을 넣어서 요청을 전송하고 결과를 확인
    
    ![image](/assets/img/photos/maskingLambdaDocker/7.png)
    

### **Troubleshooting**

1. 함수 실행 3초만에 timeout 발생
    - 최초에는 제한 시간이 3초로 설정돼있음.
    - 이 값을 예상되는 함수 실행 시간만큼 늘려줘야 함.
    
    ![image](/assets/img/photos/maskingLambdaDocker/8.png)
    
    ![image](/assets/img/photos/maskingLambdaDocker/9.png)
    
2. 실행 중 `Unable to import module 'agnostic_mask': No module named 'model'` 에러 발생
    
    ![image](/assets/img/photos/maskingLambdaDocker/10.png)
    
    - Lambda는 `/var/task` 안에 있는 파일들만 실행할 수 있음
    - 그러나 최초에 Dockerfile을 작성할 때는 workdir을 `/app` 으로 두고 거기 안에 모든 파일들을 복사하도록 함. 그리고 실행에 필요한 `agnostic_mask.py` 만 `/var/task` 로 옮겼음.
    - 따라서 `agnostic_mask.py` 실행에 필요한 모듈들을 적절히 가져오지 못했던 것임.
    
    → workdir 자체를 `/var/task` 로 설정하고 모든 파일들을 그곳으로 복사하여 문제를 해결함.
    
3. 테스트 이벤트 작성 실수
    - 테스트 이벤트도 post 요청 형식과 동일하게 header와 body를 담아줘야 함.
    - agnostic_mask.py의 handler에서 처리하는 방식과 대응되는 body여야 함.
    
    ```python
    def handler(event, context):
        start = time.time()
        start_timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    
        body = event["body-json"]
    
        username = body["username"]
        img = body["img"]
    
        for cloth_type in ["upper", "lower", "overall", "inner", "outer"]:
            get_mask(
                image=img,
                cloth_type=cloth_type,
                username=username,
                start_timestamp=start_timestamp,
            )
    
        result = f"Hello, {username}"
    
        print("Time taken: ", time.time() - start)
    
        return {"statusCode": 200, "body": json.dumps(result)}
    ```
    
    ```python
    {
      "body-json": {
        "username": "jongmin",
        "img": "/9j/4AAQSkZJRgABAQEBLAEsAA..."
      },
      "headers": {
        "Content-Type": "application/json"
      }
    }
    ```
    
4. 실행 중 용량 부족 발생
    - 마찬가지로 `/tmp` 의 용량을 적절히 늘려주면 됨
    
    ![image](/assets/img/photos/maskingLambdaDocker/11.png)
    
5. 실행 중 Read-only 이슈 발생
    
    ![image](/assets/img/photos/maskingLambdaDocker/12.png)
    
    - Lambda는 `/tmp` 를 제외한 모든 디렉토리는 Read-only
    - 그러나 `agnostic_mask.py` 에서 cache를 저장하는 부분과 masking 결과물을 저장하는 부분이 동일한 디렉토리에 저장하게끔 되어 있어 에러가 발생
    
    → 따라서 모든 파일 쓰기는 `/tmp` 아래에서 이루어지도록 코드를 수정함.
    
6. Lambda가 .env에서 환경변수를 직접 읽어오지 못함.
    
    ![image](/assets/img/photos/maskingLambdaDocker/13.png)
    
    - AWS access key가 담긴 `.env`를 Docker Image에 직접 포함시켜서 함수를 실행해봤지만 환경변수를 읽어오지 못하는 문제가 발생
    - 또한 AWS_ACCESS_KEY_ID라는 키를 그대로 써도 반영이 안되는(IAM 역할로 추가하라는) 문구가 뜸.
    
    → 따라서 이름에서 AWS를 떼고 환경 변수로 지정하여 함수에서 사용하도록 함. 
    
    ![image.png](/assets/img/photos/maskingLambdaDocker/14.png)