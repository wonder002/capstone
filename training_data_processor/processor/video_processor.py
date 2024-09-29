import yt_dlp
import os
from ..utils.file_utils import FileUtils

class VideoProcessor:
    def __init__(self, output_dir):
        # 출력 디렉토리 설정
        self.output_dir = output_dir

    async def process(self, video_url, batch_dir):
        # 비디오 ID 추출
        video_id = video_url.split("v=")[1]
        # 비디오 출력 경로 설정 (배치 디렉토리 내부)
        output_path = os.path.join(batch_dir, video_id)
        os.makedirs(output_path, exist_ok=True)

        # yt-dlp 옵션 설정 (오디오 추출 및 WAV 변환)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        }
        # 비디오 다운로드 및 오디오 추출
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)

        # 메타데이터 준비
        metadata = {
            'title': info['title'],
            'description': info['description'],
            'upload_date': info['upload_date'],
        }
        # 메타데이터를 JSON 파일로 저장
        await FileUtils.save_json(metadata, os.path.join(output_path, f"{video_id}_metadata.json"))

        return video_id, output_path