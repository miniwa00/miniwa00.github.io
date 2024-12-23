---
title: "fzf 사용법 및 튜토리얼"
date: 2024-12-23 14:00:00 +/-TTTT
categories: [Tool]
tags: [macOS, CLI Tool, fzf, iterm, zsh, neovim, brew]
math: true
toc: true
published: true
author: Jongmin Kim
comments: true
---

fzf는 터미널에서 사용할 수 있는 경량화되고 빠른 명령줄 인터페이스 기반의 파일 및 텍스트 검색 도구이다. 

---
### 설치
- fzf 설치
```
brew install fzf
```
- fd 설치: fzf는 내부적으로 find 명령어를 사용하는데 이를 fd로 대체하여 성능을 향상시킨다.
```
brew install fd
```
- fzf-git 설치: fzf에 강력하게 호환되는 git 관련 도구
```
cd ## 홈 디렉토리로 이동
git clone https://github.com/junegunn/fzf-git.sh.git
```

---
### fzf 세팅을 위한 zshrc 파일
- zshrc 파일을 열고 plugins에 fzf를 추가한 후 아래 부분도 파일의 하단에 추가한다.


```
...

# plugins
plugins=(
    ... 
	fzf
)

...

# ---- FZF Start ----

# Set up fzf key bindings and fuzzy completion
eval "$(fzf --zsh)"

# -- setup fzf theme --
fg="#CBE0F0"
bg="#011628"
bg_highlight="#143652"
purple="#B388FF"
blue="#06BCE4"
cyan="#2CF9ED"

export FZF_DEFAULT_OPTS="--color=fg:${fg},bg:${bg},hl:${purple},fg+:${fg},bg+:${bg_highlight},hl+:${purple},info:${blue},prompt:${cyan},pointer:${cyan},marker:${cyan},spinner:${cyan},header:${cyan}"

# -- Set up fzf-git --
source ~/fzf-git.sh/fzf-git.sh

# -- Use fd instead of fzf --
export FZF_DEFAULT_COMMAND="fd --hidden --strip-cwd-prefix --exclude .git"
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# Use fd (https://github.com/sharkdp/fd) for listing path candidates.
# - The first argument to the function ($1) is the base path to start traversal
# - See the source code (completion.{bash,zsh}) for the details.
_fzf_compgen_path() {
  fd --hidden --exclude .git . "$1"
}

# Use fd to generate the list for directory completion
_fzf_compgen_dir() {
  fd --type=d --hidden --exclude .git . "$1"
}

# ---- FZF End ---- 
```

---
### fzf and fzf-git Examples
- fzf Examples
![image](/assets/img/photos/fzftutorial/1.png)  
<br>
- fzf-git Examples
![image](/assets/img/photos/fzftutorial/2.png)
