class Config:
    def __init__(self):
        # 기본 설정값 초기화
        self.OUTPUT_DIR = "dataset"  # 처리된 데이터를 저장할 기본 디렉토리
        self.VIDEO_NUM = 50
        self.BATCH_SIZE = 100  # 한 배치에 처리할 비디오 수
        self.MAX_CONCURRENT_DOWNLOADS = 5  # 동시에 처리할 수 있는 최대 다운로드 수
        self.SUBTITLE_LANGUAGE = 'en'  # 자막 언어 설정 (한국어)

        # 채널 URL은 초기화 시점에 설정하지 않음
        self.CHANNEL_URL = None

    def set_channel_url(self, url):
        # 채널 URL을 설정하는 메서드
        self.CHANNEL_URL = url