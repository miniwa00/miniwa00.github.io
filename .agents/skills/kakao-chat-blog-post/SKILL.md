---
name: kakao-chat-blog-post
description: Use when the user gives a KakaoTalk counterpart or chat room name and asks to turn today's conversation into a blog post in this Jekyll repo.
---

# Kakao Chat Blog Post

This workflow turns a KakaoTalk room export into a public Jekyll post using only today's messages.

## Inputs

- A KakaoTalk counterpart name or chat room name from the user.
- Optional target date. If omitted, use today's date in Asia/Seoul.

## Workflow

1. Use Computer Use to open KakaoTalk, search the given name, enter the chat room, and export/download the conversation history.
2. Save exports under `var/kakao-chat-blog-post/`. This directory is intentionally ignored by git because it may contain private chat text.
3. Extract only the target day's messages:

   ```bash
   python3 tools/kakao_today_extract.py "<export-file>" --chat-name "<chat-room-name>"
   ```

   Use `--date YYYY-MM-DD` when the user requests a non-today date.
   KakaoTalk Mac text exports may be CSV files with `Date,User,Message` columns; the extractor supports that format.

4. Read only the extracted Markdown file from `var/kakao-chat-blog-post/` and write a post from that material. Do not use messages from other dates.
5. Create the final post in `_posts/` with this front matter shape:

   ```yaml
   ---
   title: "<short Korean title>"
   date: YYYY-MM-DD HH:MM:SS +0900
   categories: [Essay]
   tags: [kakao, conversation]
   math: true
   toc: true
   published: true
   author: Jongmin Kim
   comments: true
   ---
   ```

6. Run `bundle exec jekyll build` before publishing.
7. Before committing and pushing a post derived from private chat, show the generated title, file path, and a short summary, then get explicit approval.
8. After approval, commit with a Conventional Commit message such as `docs: 카카오톡 대화 기반 포스트 추가` and push.

## Writing Rules

- Use only the extracted target-day chat content as source material.
- Do not quote sensitive chat lines verbatim unless the user explicitly asks for direct quotations.
- Prefer a reflective Korean essay style consistent with existing `_posts`.
- Avoid exposing phone numbers, addresses, account identifiers, or private third-party details.
- If the extracted chat has too little substance for a post, tell the user and ask whether to create a short memo-style post instead.
