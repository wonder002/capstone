import asyncio
import os
import logging
from training_data_processor.utils.youtube_utils import YoutubeUtils
from training_data_processor.utils.file_utils import FileUtils
from training_data_processor.processor.video_processor import VideoProcessor
from training_data_processor.processor.audio_processor import AudioProcessor
from training_data_processor.processor.subtitle_processor import SubtitleProcessor

logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self, config):
        # 설정 초기화
        self.config = config
        # 비디오 처리를 위한 비동기 큐 생성
        self.video_queue = asyncio.Queue()
        # 동시 다운로드 제한을 위한 세마포어 생성
        self.semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_DOWNLOADS)
        # 현재 배치의 비디오 ID 목록
        self.current_batch = []
        # 비디오 프로세서 초기화
        self.video_processor = VideoProcessor(self.config.OUTPUT_DIR)
        # 현재 배치 번호
        self.current_batch_number = 1
        self.total_videos=0
        self.processed_videos = 0

    async def process_video(self, video_url):
        # 세마포어를 사용하여 동시 처리 제한
        async with self.semaphore:
            try:

                # 비디오 ID 추출
                video_id = video_url.split("v=")[1]

                # 수동 자막 존재 여부 확인
                self.processed_videos += 1
                has_manual_subs = await YoutubeUtils.has_manual_subtitles(video_id, self.config.SUBTITLE_LANGUAGE)

                if not has_manual_subs:
                    logger.info(f"[{self.processed_videos}/{self.total_videos}] 건너뛰기 {video_url}: 수동 자막 없음")
                    return

                # 현재 배치 디렉토리 생성
                batch_dir = FileUtils.create_batch_directory(self.config.OUTPUT_DIR, self.current_batch_number)

                # 비디오 처리 (다운로드 및 오디오 추출)
                video_id, output_path = await self.video_processor.process(video_url, batch_dir)

                # 자막 다운로드
                await SubtitleProcessor.download_subtitle(
                    video_id,
                    os.path.join(output_path, f"{video_id}.txt"),
                    self.config.SUBTITLE_LANGUAGE
                )

                # 오디오 전처리
                await AudioProcessor.preprocess(
                    os.path.join(output_path, f"{video_id}.wav"),
                    os.path.join(output_path, f"{video_id}_processed.wav")
                )

                # 현재 배치에 비디오 ID 추가
                self.current_batch.append(video_id)
                # 배치 크기 도달 시 새 배치 시작
                if len(self.current_batch) >= self.config.BATCH_SIZE:
                    logger.info(f"배치 {self.current_batch_number} 완료. 새 배치 시작.")
                    self.current_batch = []
                    self.current_batch_number += 1

                logger.info(f"[{self.processed_videos}/{self.total_videos}] 처리 완료: {video_url}")
            except Exception as e:
                logger.error(f"[{self.processed_videos}/{self.total_videos}] 비디오 처리 중 오류 발생 {video_url}: {str(e)}")

    async def run(self):
        # 채널의 비디오 URL 가져오기
        video_urls = await YoutubeUtils.get_channel_videos(self.config.CHANNEL_URL, self.config.VIDEO_NUM)
        self.total_videos = len(video_urls)
        logger.info(f"총 {self.total_videos}개의 비디오 URL을 가져왔습니다.")

        # 비디오 URL을 큐에 추가
        for url in video_urls:
            await self.video_queue.put(url)

        # 모든 비디오 처리
        tasks = []
        while not self.video_queue.empty():
            video_url = await self.video_queue.get()
            task = asyncio.create_task(self.process_video(video_url))
            tasks.append(task)
        await asyncio.gather(*tasks)

        logger.info("모든 비디오 처리 완료.")