---
title: "[Noneo] Expo 관련 커맨드 정리"
date: 2025-07-16 17:00:00 +0900
categories: [React Native]
tags: [expo, react-native, android, ios]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

Expo는 React Native 앱을 빠르게 만들고 빌드할 수 있게 도와주는 도구다. 기본 Managed Workflow에서는 `android`와 `ios` 네이티브 폴더가 없고, Expo가 많은 설정을 대신 관리한다.

## 프로젝트 시작

새 Expo 앱은 다음처럼 만들 수 있다.

```bash
npx create-expo-app@latest 앱이름 --template blank
```

자주 쓰는 템플릿은 다음과 같다.

- `blank`: 추가 라이브러리나 설정 없이 새 프로젝트 시작
- `blank-typescript`: TypeScript가 사전 설정된 템플릿
- `tabs-typescript`: 탭 네비게이션 구조가 포함된 TypeScript 템플릿
- `expo-dev-client`: Firebase나 커스텀 네이티브 코드처럼 네이티브 모듈이 필요한 앱에 적합한 템플릿

## Managed Workflow에서 Bare Workflow로 변환

네이티브 설정이 필요하면 `prebuild`를 실행한다.

```bash
npx expo prebuild
```

이 명령은 Expo 프로젝트를 Managed Workflow에서 Bare Workflow에 가까운 형태로 바꾸며, `android`와 `ios` 폴더를 생성한다. `app.json`이나 `app.config.js`에 새로운 플러그인을 추가했을 때도 다시 실행해야 할 수 있다.

기존 네이티브 파일을 정리하고 새로 만들려면 다음 명령을 사용한다.

```bash
npx expo prebuild --clean
```

특정 플랫폼만 대상으로 삼을 수도 있다.

```bash
npx expo prebuild --platform android
```

## prebuild 오류를 만났을 때

`npx expo prebuild`가 동작하지 않으면 Node.js 버전과 의존성 충돌을 먼저 확인한다. Expo는 특정 LTS 버전의 Node.js와 더 잘 맞는 경우가 많다.

```bash
rm -rf node_modules package-lock.json
npm install
npm cache clean --force
```

iOS에서 `pod install` 오류가 나면 Ruby와 Xcode 경로 문제일 수 있다.

```bash
brew install ruby --update
sudo xcode-select --switch /Applications/Xcode.app
```

필요하면 `ios` 폴더에서 직접 `pod install --repo-update`를 실행한다.

## Android 릴리스 APK 생성

Android 릴리스 APK는 다음 명령으로 만들 수 있다.

```bash
cd android
./gradlew assembleRelease
```

생성된 APK는 보통 아래 경로에 생긴다.

```text
android/app/build/outputs/apk/release/app-release.apk
```

## 결론

Expo에서는 어디까지 Expo가 관리하고, 어디부터 네이티브 프로젝트를 직접 다룰지 구분하는 것이 중요하다. 단순 앱은 Managed Workflow로 충분하지만, Firebase나 네이티브 모듈이 들어오면 `prebuild` 이후의 Android/iOS 설정까지 함께 이해해야 한다.
