---
title: "Expo prebuild 이후 APK 설치 오류 정리"
date: 2025-01-25 17:00:00 +0900
categories: [React Native]
tags: [expo, eas, android, apk, troubleshooting]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

Expo 앱을 Android APK로 빌드하는 과정에서 빌드는 성공했지만 설치 후 앱이 바로 종료되는 문제가 있었다. 처음에는 EAS 빌드 명령으로 preview 프로필을 사용했다.

```bash
eas build -p android --profile preview
```

## expo doctor부터 확인

빌드 오류를 만났을 때는 먼저 `expo doctor` 또는 `npx expo-doctor`로 프로젝트 상태를 확인하는 편이 좋다.

당시 확인된 이슈는 크게 두 가지였다.

1. non-CNG 프로젝트에서 app config fields가 동기화되지 않을 수 있다는 경고
2. React Native Directory package metadata 검증 경고

두 번째 경고는 `dotenv`, `firebase`, `uuid` 같은 패키지가 React Native Directory에 포함되지 않아 발생한 것이었다. 프로젝트에 직접적인 문제가 아니라면 설정으로 경고를 줄일 수 있다.

```json
{
  "expo": {
    "doctor": {
      "reactNativeDirectoryCheck": {
        "listUnknownPackages": false
      }
    }
  }
}
```

이 설정을 `package.json`에 추가한 뒤 `npx expo-doctor`가 통과하는지 다시 확인했다.

## splashscreen_logo 오류

다시 빌드했을 때 splash screen 이미지 관련 오류가 발생했다. 이 경우 `app.config.js`에 splash 설정을 명시해 이미지 경로를 잡아준다.

```javascript
splash: {
  image: './assets/images/splashscreen_logo.png',
  resizeMode: 'contain',
  backgroundColor: '#ffffff',
},
android: {
  splash: {
    mdpi: './assets/images/splashscreen_logo.png',
    hdpi: './assets/images/splashscreen_logo.png',
    xhdpi: './assets/images/splashscreen_logo.png',
    xxhdpi: './assets/images/splashscreen_logo.png',
    xxxhdpi: './assets/images/splashscreen_logo.png',
  },
},
```

## 빌드는 성공하지만 앱이 바로 종료되는 경우

APK를 다운로드하고 설치하는 데까지는 성공했지만 앱 실행 직후 종료되는 문제가 남았다. 가능한 원인 중 하나로 Android SDK version mismatch를 의심했다.

```javascript
ext {
  buildToolsVersion = findProperty('android.buildToolsVersion') ?: '35.0.0'
  minSdkVersion = Integer.parseInt(findProperty('android.minSdkVersion') ?: '24')
  compileSdkVersion = Integer.parseInt(findProperty('android.compileSdkVersion') ?: '35')
  targetSdkVersion = Integer.parseInt(findProperty('android.targetSdkVersion') ?: '35')
  kotlinVersion = findProperty('android.kotlinVersion') ?: '1.9.24'
  ndkVersion = '26.1.10909125'
}
```

기존에는 `compileSdkVersion`과 `targetSdkVersion`이 서로 달랐고, 이를 35로 통일해 보았다. 다만 이 조치만으로는 문제가 해결되지 않았다.

## 결론

Expo APK 문제는 빌드 단계, 설정 검증 단계, 설치 후 런타임 단계가 서로 다르다. `expo doctor`가 통과하더라도 APK가 바로 종료될 수 있고, 이때는 Android 네이티브 설정과 런타임 로그를 함께 봐야 한다. 기록상 핵심은 먼저 프로젝트 상태를 정리하고, splash asset과 SDK version mismatch 같은 명시적인 설정 문제를 하나씩 제거하는 흐름이었다.
