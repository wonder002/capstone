import asyncio
import logging
from .config.config import Config
from .processor.batch_processor import BatchProcessor

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main(channel_url):
    # 설정 객체 생성
    config = Config()

    # 채널 URL 설정
    config.set_channel_url(channel_url)
    logger.info(f"처리할 YouTube 채널 URL: {channel_url}")

    # 배치 프로세서 초기화
    processor = BatchProcessor(config)

    # 처리 시작
    logger.info("YouTube 채널 처리 시작")
    await processor.run()
    logger.info("YouTube 채널 처리 완료")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        logger.error("사용법: python main2.py <YouTube 채널 URL>")
        sys.exit(1)

    channel_url = sys.argv[1]
    asyncio.run(main(channel_url))
