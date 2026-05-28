---
title: "[Noneo] React Native Firebase 설정 추가하기"
date: 2025-07-08 17:00:00 +0900
categories: [React Native]
tags: [react-native, firebase, firestore, auth]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

React Native 프로젝트에서 Firebase를 사용하려면 Firebase 프로젝트 생성 이후 앱 코드와 네이티브 설정을 함께 연결해야 한다.

## 패키지 설치

먼저 필요한 Firebase 관련 패키지를 설치한다.

```bash
npm install @react-native-firebase/firestore
npm install @react-native-firebase/app
npm install @react-native-firebase/auth
```

Firestore, Firebase 앱 초기화, Firebase Auth를 각각 사용하기 위한 모듈이다.

## Firebase 프로젝트 설정

Firebase 콘솔에서 프로젝트를 만들고 Android 앱을 등록한 뒤 `google-services.json`을 다운로드한다. 이 파일은 Android 프로젝트의 `android/app` 안에 넣는다.

이후 Firebase 프로젝트 설정에서 아래 값들을 확인한다.

```text
FIREBASE_API_KEY
FIREBASE_AUTH_DOMAIN
FIREBASE_PROJECT_ID
FIREBASE_STORAGE_BUCKET
FIREBASE_MESSAGING_SENDER_ID
FIREBASE_APP_ID
```

이 값들은 `.env`에 추가해두고 앱 코드에서 읽어오도록 한다.

## Firebase config 작성

`config/firebase.ts` 파일을 만들고 Firebase 앱을 초기화한다.

```typescript
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: process.env.FIREBASE_AUTH_DOMAIN,
  projectId: process.env.FIREBASE_PROJECT_ID,
  storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.FIREBASE_APP_ID,
};

if (!firebaseConfig.apiKey) {
  console.warn('Firebase 설정값이 없습니다. .env 파일을 확인해주세요.');
}

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
```

`.env`를 React Native에서 읽어오려면 `react-native-dotenv` 같은 설정이 추가로 필요할 수 있다.

## 결론

Firebase 설정은 콘솔에서 값을 확인하는 일과 앱 코드에서 초기화하는 일이 함께 맞아야 한다. 특히 React Native에서는 네이티브 쪽 파일인 `google-services.json`과 JavaScript 쪽 config가 모두 연결되어야 하므로, 둘 중 하나만 맞춰서는 동작하지 않을 수 있다.
