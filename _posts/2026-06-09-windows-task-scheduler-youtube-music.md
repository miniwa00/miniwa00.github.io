---
title: "Windows 작업 스케줄러로 YouTube Music 자동 실행하기"
date: 2026-06-09 02:50:00 +0900
categories: [Devlog]
tags: [windows, automation, task-scheduler, youtube-music, vbs, nircmd]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

## 목표

Windows PC가 특정 시간에 자동으로 켜지고 자동 로그인된 뒤, 정해진 시간에 YouTube Music 앱을 실행하고 음악을 재생하도록 구성했다.

자동 부팅과 자동 로그인은 이미 설정되어 있었고, 남은 목표는 로그인 이후의 동작이었다.

- 특정 시간에만 YouTube Music 실행
- 실행 직후 시스템 볼륨을 30%로 설정
- YouTube Music 앱 로딩 후 스페이스바 입력으로 재생 시작
- 부팅 직후에는 앱이 자동 실행되지 않도록 정리

최종적으로는 Windows 작업 스케줄러에서 VBS 파일을 특정 시간에 실행하도록 등록했다.

## 최종 구성

VBS 스크립트는 다음 순서로 동작한다.

1. NirCmd로 Windows 마스터 볼륨을 30%로 설정한다.
2. Chrome PWA 형태로 설치된 YouTube Music 앱을 실행한다.
3. 앱 로딩을 위해 일정 시간 대기한다.
4. YouTube Music 창을 활성화한다.
5. 스페이스바 입력을 보내 재생을 시작한다.

최종 스크립트는 다음과 같다.

```vbs
Set WshShell = CreateObject("WScript.Shell")

' 1. NirCmd를 이용해 마스터 볼륨을 30%로 설정
WshShell.Run "C:\nircmd.exe setsysvolume 19660", 0, True
WScript.Sleep 500

' 2. YouTube Music PWA 앱 실행
WshShell.Run """C:\Program Files\Google\Chrome\Application\chrome_proxy.exe"" --profile-directory=Default --app-id=cinhimbnkkaeohfgghhklpknlkffjgod ""https://music.youtube.com/playlist?list=LM""", 0, False

' 3. 앱 로딩 대기
WScript.Sleep 8000

' 4. YouTube Music 창 활성화 후 재생
WshShell.AppActivate "YouTube Music"
WScript.Sleep 500
WshShell.SendKeys " "
```

## YouTube Music 앱 실행 방식

설치된 YouTube Music 앱은 Windows 네이티브 앱이 아니라 Chrome 기반 PWA였다. 그래서 실제 실행 대상은 다음 파일이었다.

```text
C:\Program Files\Google\Chrome\Application\chrome_proxy.exe
```

여기에 Chrome profile과 app id를 인수로 넘겨 YouTube Music 앱을 실행한다.

```text
--profile-directory=Default --app-id=<YouTube Music app id>
```

내 환경에서는 최종적으로 다음 앱 ID를 사용했다.

```text
cinhimbnkkaeohfgghhklpknlkffjgod
```

전체 실행 명령은 VBS 안에서 다음처럼 호출했다.

```vbs
WshShell.Run """C:\Program Files\Google\Chrome\Application\chrome_proxy.exe"" --profile-directory=Default --app-id=cinhimbnkkaeohfgghhklpknlkffjgod ""https://music.youtube.com/playlist?list=LM""", 0, False
```

여기서 `https://music.youtube.com/playlist?list=LM`은 YouTube Music의 좋아요 표시한 음악 목록이다.

## 자동 재생 처리

처음에는 URL에 `play=1` 같은 파라미터를 붙여 자동 재생을 시도했다.

```text
https://music.youtube.com/playlist?list=LM&play=1
```

하지만 YouTube Music은 브라우저와 PWA 정책상 페이지 진입만으로는 안정적으로 재생되지 않았다. 사용자의 명시적 조작 없이 미디어를 자동 재생하는 동작이 제한되기 때문이다.

그래서 앱을 실행한 뒤 일정 시간 기다리고, YouTube Music 창을 활성화한 다음 스페이스바 입력을 보내는 방식으로 처리했다.

```vbs
WScript.Sleep 8000

WshShell.AppActivate "YouTube Music"
WScript.Sleep 500
WshShell.SendKeys " "
```

`WScript.Sleep 8000`은 앱 로딩 대기 시간이다. PC 상태나 부팅 직후 부하에 따라 8초가 부족하면 10초나 12초로 늘릴 수 있다.

## 볼륨 30% 고정

자동 재생에서 중요한 문제 중 하나는 볼륨이었다. 부팅 직후 음악이 너무 크게 재생되지 않도록 마스터 볼륨을 30%로 고정하고 싶었다.

처음에는 VBS의 `SendKeys`로 볼륨 다운과 볼륨 업 키를 보내는 방식을 시도했다.

```vbs
WshShell.SendKeys chr(&hAF) ' Volume Down
WshShell.SendKeys chr(&hAE) ' Volume Up
```

하지만 이 방식은 안정적으로 동작하지 않았다. 특히 부팅 직후나 백그라운드 실행 상황에서는 미디어 키 입력이 무시될 수 있었다.

PowerShell을 통해 직접 볼륨을 제어하는 방식도 시도했지만, 이 환경에서는 기대한 대로 동작하지 않았다.

최종적으로는 NirCmd를 사용했다.

```vbs
WshShell.Run "C:\nircmd.exe setsysvolume 19660", 0, True
```

NirCmd의 `setsysvolume`은 0부터 65535 사이의 값을 사용한다. 65535가 100%이므로 30%는 대략 다음 값이다.

```text
65535 * 0.3 = 19660.5
```

따라서 30% 볼륨 설정에는 `19660`을 사용했다.

## 작업 스케줄러 등록

스크립트가 준비되면 Windows 작업 스케줄러에서 특정 시간에 실행되도록 등록한다.

작업 스케줄러에서 설정한 핵심 항목은 다음과 같다.

- 트리거: 원하는 시간
- 동작: 프로그램 시작
- 실행 대상: 작성한 `.vbs` 파일

여기서 중요한 점은 YouTube Music 앱 자체를 작업 스케줄러에 등록하는 것이 아니라, VBS 스크립트를 등록한다는 것이다.

앱 실행, 볼륨 설정, 로딩 대기, 스페이스바 입력을 모두 스크립트가 처리하기 때문이다.

## 부팅 직후 앱이 켜지는 문제

설정 중간에 부팅 직후 YouTube Music 앱이 갑자기 켜지는 문제가 있었다.

처음에는 VBS 스크립트나 작업 스케줄러가 원인인지 의심했지만, 실제 원인은 Windows 시작프로그램 폴더였다.

이전 테스트 과정에서 `shell:startup` 폴더에 YouTube Music 바로가기나 테스트용 실행 파일이 남아 있었고, 그 파일이 로그인 직후 앱을 실행하고 있었다.

확인 방법은 다음과 같다.

1. `Win + R`을 누른다.
2. `shell:startup`을 입력한다.
3. 폴더 안에 YouTube Music 바로가기, `.bat`, `.vbs` 파일이 남아 있는지 확인한다.
4. 작업 스케줄러로만 실행할 파일이라면 이 폴더에서는 제거한다.

이 정리를 마치면 부팅 직후에는 앱이 켜지지 않고, 작업 스케줄러가 지정한 시간에만 스크립트가 실행된다.

## 정리

최종 구조는 다음과 같다.

```text
Windows 자동 부팅
-> Windows 자동 로그인
-> 지정된 시간 도달
-> 작업 스케줄러가 VBS 실행
-> NirCmd로 볼륨 30% 설정
-> YouTube Music PWA 실행
-> 로딩 대기
-> 스페이스바 입력
-> 음악 재생
```

이번 설정에서 핵심은 스크립트 자체보다 실행 주체를 분리해서 이해하는 것이었다.

- 부팅 직후 실행되는 것은 시작프로그램 폴더가 담당한다.
- 특정 시간 실행은 작업 스케줄러가 담당한다.
- YouTube Music 실행과 재생 입력은 VBS가 담당한다.
- 안정적인 볼륨 제어는 NirCmd가 담당한다.

자동화 문제를 디버깅할 때는 "이 코드가 맞는가?"만 볼 것이 아니라, "누가 이 코드를 언제 실행하는가?"를 함께 확인해야 한다.
