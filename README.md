## 가상환경

```bash
# venv 모듈을 이용해 venv 이름으로 가상환경 생성
python3 -m venv venv

# 가상환경 진입
source vnev/bin/activate

# pip 버전 업데이트
python -m pip install --upgrade pip

# 가상환경 비활성화
deactivate
```

## WAS 실행

```bash
cd app

uvicorn main:app --reload
```
