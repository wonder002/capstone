from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp

import logging

logger = logging.getLogger(__name__)

class YoutubeUtils:
    '''
    유튜브 다운로드 처리 관련 클래스
    '''

    staticmethod

    async def has_manual_subtitles(video_id, language):
        try:
            # 비디오의 자막 리스트를 가져옴
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # 모든 사용 가능한 자막 정보 로깅
            logger.info(f"비디오 {video_id}의 사용 가능한 자막:")
            for transcript in transcript_list:
                subtitle_type = '수동' if not transcript.is_generated else '자동'
                logger.info(f"  - 언어: {transcript.language}, 종류: {subtitle_type}")

            # 수동 자막 확인
            manual_transcript = next((t for t in transcript_list if not t.is_generated and t.language_code == language),
                                     None)
            if manual_transcript:
                logger.info(f"비디오 {video_id}에 수동 {language} 자막이 있습니다.")
                return True

            logger.info(f"비디오 {video_id}에 {language} 자막이 없습니다.")
            return False

        except Exception as e:
            logger.error(f"비디오 {video_id}의 자막 확인 중 오류 발생: {str(e)}")
            return False

    @staticmethod
    async def get_channel_videos(channel_url, limit=None):
        ydl_opts = {
            'extract_flat': True,
            'force_generic_extractor': True,
            'playlistend': limit
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(channel_url, download=False)
                if 'entries' not in result:
                    logger.error(f"채널에서 'entries'를 찾을 수 없습니다: {channel_url}")
                    return []

                video_urls = []
                for entry in result['entries']:
                    if 'id' in entry and 'url' not in entry:
                        # 'id'는 있지만 'url'이 없는 경우 URL 구성
                        video_urls.append(f"https://www.youtube.com/watch?v={entry['id']}")
                    elif 'url' in entry:
                        video_urls.append(entry['url'])
                    else:
                        logger.warning(f"'id' 또는 'url'이 없는 항목 건너뛰기: {entry}")

                if limit:
                    video_urls = video_urls[:limit]

                logger.info(f"채널에서 {len(video_urls)}개의 비디오를 찾았습니다: {channel_url}")
                return video_urls
            except Exception as e:
                logger.error(f"채널 {channel_url}에서 비디오 URL 추출 중 오류 발생: {str(e)}")
                return []

    