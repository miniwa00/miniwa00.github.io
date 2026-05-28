---
title: "[Noneo] React Native에서 dotenv가 동작하지 않을 때"
date: 2025-07-02 17:00:00 +0900
categories: [React Native]
tags: [react-native, expo, dotenv, firebase]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

React Native 프로젝트에서 Firebase 설정값을 `.env`에서 읽어오려 했는데 값이 비어 있는 문제가 생길 수 있다.

예를 들어 다음처럼 `process.env`를 직접 사용하면 기대와 다르게 환경변수가 들어오지 않을 때가 있다.

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

## react-native-dotenv 설치

이럴 때는 `react-native-dotenv`를 설치하고 Babel 설정에서 `.env`를 import할 수 있도록 잡아준다.

```bash
npm install react-native-dotenv --save-dev
```

## babel.config.js 설정

`babel.config.js`에 dotenv 플러그인을 추가한다.

```javascript
module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      [
        'module:react-native-dotenv',
        {
          moduleName: '@env',
          path: '.env',
          blacklist: null,
          whitelist: null,
          safe: false,
          allowUndefined: true,
        },
      ],
    ],
  };
};
```

Babel은 React Native 프로젝트에서 JavaScript와 TypeScript 코드가 앱에서 실행될 수 있는 형태로 변환되는 방식을 정한다. 여기서는 `@env`라는 모듈 이름으로 `.env` 값을 가져오도록 알려주는 역할을 한다.

## 결론

React Native에서는 Node.js처럼 `process.env`가 자연스럽게 동작한다고 가정하면 헷갈릴 수 있다. Expo나 React Native 프로젝트에서는 번들링 과정에서 환경변수를 주입하는 설정이 필요하고, 그 역할을 `react-native-dotenv`와 Babel 설정이 맡는다.
