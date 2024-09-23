## 기술 스택

- fastapi
- pytube (pytubefix)
- python-ffmpeg
- Wisper

## 사용법

### 가상환경 설정

```bash
# venv 모듈을 이용해 venv 이름으로 가상환경 생성
python3 -m venv venv

# 가상환경 진입
source vnev/bin/activate

# pip 버전 업데이트 (필요시)
python -m pip install --upgrade pip

# 패키지 설치
pip install -r requirements.txt
```

### ffmpeg 설치

Wisper 를 이용하기 위해 비디오(mp4) 를 오디오 (mp3) 로 변환해야 합니다.
비디오 파일이나 오디오 파일을 처리할 때 내부적으로 ffmpeg 실행파일을 필요로 하기 때문에 ffmpeg 가 설치되어 있어야 로컬에서 프로젝트의 기능이 정상적으로 동작합니다.

```bash
brew install ffmpeg
```

### 애플리케이션 실행

프로젝트 루트 디렉토리에서 명령어를 입력합니다.

```bash
uvicorn app.main:app --reload
```
