---
title: "ECS Fargate + GitHub Action 자동 배포"
date: 2024-08-14 18:00:00 +/-TTTT
categories: [AWS]
tags: [aws, docker, ecs, github action]
math: true
toc: true
published: true
author: Jongmin Kim
---

## **ECS**

- 태스크 정의 json 파일 다운로드
    - 좌측 태스크 정의 클릭
        
        ![image](/assets/img/photos/ECSGitHubAction/1.png)
        
    - 존재하는 태스크 정의 패밀리 클릭
        
        ![image](/assets/img/photos/ECSGitHubAction/2.png)
        
    - 최신 태스크 정의 클릭
        
        ![image](/assets/img/photos/ECSGitHubAction/3.png)
        
    - JSON 탭에서 JSON 다운로드 클릭
        
        ![image](/assets/img/photos/ECSGitHubAction/4.png)
        
    - 다운받은 json 파일을 애플리케이션 루트 디렉토리에 위치
        
        ![image](/assets/img/photos/ECSGitHubAction/5.png)
        

---

## **GitHub Action**

- GitHub Action에서 ‘Deploy to Amazon ECS’ workflow 선택
    
    ![image](/assets/img/photos/ECSGitHubAction/6.png)
    
- Settings의 Secrets and variables에서 AWS_ACCESS_KEY_ID와 AWS_SECRET_ACCESS_KEY를 Repository secrets에 등록
    
    ![image](/assets/img/photos/ECSGitHubAction/7.png)
    
- .github/workflows/aws.yml 파일을 아래 코드로 수정
    
    ```jsx
    name: Deploy to Amazon ECS
    
    on:
      push:
        branches: [ "develop-deploy" ]
    
    env:
      AWS_REGION: ap-northeast-2
      ECR_REPOSITORY: githubsalt-ecr
      ECS_SERVICE: githubsalt-backend
      ECS_CLUSTER: githubsalt-ecs
      ECS_TASK_DEFINITION: githubsalt-backend-revision2.json
      CONTAINER_NAME: githubsalt-container
      
    jobs:
      deploy:
        name: Deploy
        runs-on: ubuntu-latest
        environment: production
    
        steps:
          - name: Checkout
            uses: actions/checkout@v4
    
          - name: Set up JDK 17
            uses: actions/setup-java@v3
            with:
              java-version: '17'
              distribution: 'adopt'
    
          - name: Grant execute permission for gradlew
            run: chmod +x gradlew
    
          - name: build with gradle
            run: ./gradlew clean build -x test
    
          - name: Configure AWS credentials
            uses: aws-actions/configure-aws-credentials@v1
            with:
              aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
              aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
              aws-region: ${{ env.AWS_REGION }}
    
          - name: Login to Amazon ECR
            id: login-ecr
            uses: aws-actions/amazon-ecr-login@v1
    
          - name: Build, tag, and push image to Amazon ECR
            id: build-image
            env:
              ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
              IMAGE_TAG: ${{ github.sha }}
            run: |
              docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
              docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
              echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT
    
          - name: Fill in the new image ID in the Amazon ECS task definition
            id: task-def
            uses: aws-actions/amazon-ecs-render-task-definition@v1
            with:
              task-definition: ${{ env.ECS_TASK_DEFINITION }}
              container-name: ${{ env.CONTAINER_NAME }}
              image: ${{ steps.build-image.outputs.image }}
    
          - name: Deploy Amazon ECS task definition
            uses: aws-actions/amazon-ecs-deploy-task-definition@v1
            with:
              task-definition: ${{ steps.task-def.outputs.task-definition }}
              service: ${{ env.ECS_SERVICE }}
              cluster: ${{ env.ECS_CLUSTER }}
              wait-for-service-stability: true
    ```
    
- 커밋 후 workflow가 작동하는 것을 확인
    
    ![image](/assets/img/photos/ECSGitHubAction/workflow.png)
    

---

## **ECS**

- (수정) action workflow가 끝나면 자동으로 배포되게 수정
    
    ![image](/assets/img/photos/ECSGitHubAction/8.png)
    

---

- 태스크 정의에 최신 개정이 추가됐는지 확인
    
    ![image](/assets/img/photos/ECSGitHubAction/9.png)
    
    ![image](/assets/img/photos/ECSGitHubAction/10.png)
    
- 개정된 태스크 정의를 바탕으로 서비스에 새로운 태스크를 띄우기
    - 서비스로 접속
        
        ![image](/assets/img/photos/ECSGitHubAction/11.png)
        
    - 우측의 서비스 업데이트 클릭
        - ‘새 배포 강제 적용’에 체크
        - 원하는 태스크 정의 개정 버전을 선택
        - 태스크를 없애고 싶으면 원하는 태스크를 0으로 설정
            
            ![image](/assets/img/photos/ECSGitHubAction/12.png)