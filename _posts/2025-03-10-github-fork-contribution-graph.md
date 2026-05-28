---
title: "Fork한 GitHub 레포지토리 커밋은 잔디에 반영될까"
date: 2025-03-10 17:00:00 +0900
categories: [Git]
tags: [github, fork, contribution, git]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

GitHub에서 fork한 레포지토리에 커밋을 남겼다고 해서 그 커밋이 항상 내 Contributions Graph, 흔히 말하는 잔디에 반영되는 것은 아니다.

잔디에 반영되려면 보통 몇 가지 조건을 만족해야 한다.

1. 내가 소유하거나 협력자로 참여 중인 레포지토리에서 발생한 활동이어야 한다.
2. 커밋이 해당 레포지토리의 default branch, 보통 `main`이나 `master`에 포함되어야 한다.
3. public 레포지토리 활동이어야 한다. private 레포지토리 활동은 별도 설정을 켜야 표시된다.

## Fork 커밋이 반영되지 않는 이유

Fork는 원본 레포지토리의 복제본으로 취급된다. 내가 fork한 저장소에서 작업하더라도 그 활동이 원본 프로젝트의 기본 브랜치에 포함되지 않으면 GitHub가 의미 있는 기여로 집계하지 않을 수 있다.

그래서 fork에서 열심히 커밋했는데 잔디가 비어 보이는 일이 생긴다. 커밋이 사라진 것은 아니지만, Contributions Graph의 집계 조건을 만족하지 못한 것이다.

## 반영되게 하는 방법

가장 확실한 방법은 fork가 아니라 내 소유의 새 레포지토리로 옮기는 것이다.

```bash
git clone <forked-repo-url>
git remote remove origin
git remote add origin <your-new-repo-url>
git push -u origin main
```

원본 프로젝트에 기여하려는 목적이라면 Pull Request를 열고, 그 PR이 원본 레포지토리의 default branch에 merge되도록 하는 것이 좋다. 또는 원본 레포지토리의 collaborator로 추가되면 해당 저장소에서 남긴 커밋이 잔디에 반영될 수 있다.

## 결론

Fork에서의 커밋은 작업 기록으로는 남지만, GitHub 잔디에는 자동으로 반영되지 않을 수 있다. 잔디까지 남기고 싶다면 내 소유 레포지토리에서 작업하거나, 원본 저장소에 PR을 보내 merge되는 흐름을 타야 한다.
