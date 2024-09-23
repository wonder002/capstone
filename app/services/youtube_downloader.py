from pytubefix import YouTube
from pytubefix.cli import on_progress


def download_video(youtube_url: str, download_path: str = "downloads/") -> str:
    yt = YouTube(youtube_url.strip(), on_progress_callback = on_progress)
    # 비디오 제목
    print(yt.title)

    # 저장될 파일 이름 = 유투브 비디오 ID
    video_id = yt.video_id
    filename = f"{video_id}.mp4"

    ys = yt.streams.get_highest_resolution()   

    ys.download(output_path= download_path, filename= filename)
    file_path = f"{download_path}/{filename}"

    return file_path