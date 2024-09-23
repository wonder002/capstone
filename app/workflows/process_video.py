from app.services.youtube_downloader import download_video

# 비디오에서 텍스트 처리 과정을 담당하는 메서드
def process_video(youtube_url: str) -> dict:
    video_path = download_video(youtube_url)
    
    return {
        "video_path": video_path,
    }