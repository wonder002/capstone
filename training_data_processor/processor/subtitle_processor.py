import logging
from youtube_transcript_api import YouTubeTranscriptApi
import aiofiles

logger = logging.getLogger(__name__)

class SubtitleProcessor:
    @staticmethod
    async def download_subtitle(video_id, output_path, language='ko'):
        try:
            # 지정된 언어의 자막 가져오기
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
            # 자막을 파일로 저장
            async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
                for entry in transcript:
                    await f.write(f"{entry['start']:.2f}\t{entry['duration']:.2f}\t{entry['text']}\n")
            logger.info(f"자막 다운로드 성공 (비디오 ID: {video_id})")
            return True
        except Exception as e:
            logger.error(f"자막 다운로드 중 오류 발생 (비디오 ID: {video_id}): {str(e)}")
            return False