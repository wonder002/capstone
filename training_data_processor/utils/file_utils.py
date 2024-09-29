import os
import zipfile
import aiofiles
import json

class FileUtils:
    @staticmethod
    async def create_zip_batch(batch_dir, video_ids, output_dir):
        """
        주어진 비디오 ID 목록에 해당하는 디렉토리들을 압축 파일로 생성하는 메서드.

        Args:
            batch_dir (str): 생성된 ZIP 파일을 저장할 배치 디렉토리 경로.
            video_ids (list): 압축할 비디오 ID 목록.
            output_dir (str): 비디오 파일들이 저장된 디렉토리 경로.

        Returns:
            str: 생성된 ZIP 파일의 경로.
        """

        # batch 디렉토리에 있는 파일 개수를 기반으로 새 zip 파일 경로를 지정함.
        zip_path = os.path.join(batch_dir, f"batch_{len(os.listdir(batch_dir)) + 1}.zip")

        # zip 파일을 생성하고, 'w' 모드로 열어 비디오 파일들을 추가함.
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for video_id in video_ids:
                # 각 비디오 ID에 해당하는 디렉토리 경로를 설정함.
                video_dir = os.path.join(output_dir, video_id)

                # 비디오 디렉토리 내의 모든 파일을 탐색함.
                for root, _, files in os.walk(video_dir):
                    for file in files:
                        # 파일의 전체 경로를 구함.
                        file_path = os.path.join(root, file)

                        # 압축 파일 안에서 파일이 저장될 상대 경로를 설정함.
                        arcname = os.path.relpath(file_path, output_dir)

                        # zip 파일에 해당 파일을 추가함.
                        zipf.write(file_path, arcname)

        # 생성된 zip 파일의 경로를 반환함.
        return zip_path

    @staticmethod
    def create_batch_directory(output_dir, batch_number):
        # 배치 번호에 따른 새 디렉토리 생성
        batch_dir = os.path.join(output_dir, f"batch_{batch_number}")
        os.makedirs(batch_dir, exist_ok=True)
        return batch_dir

    @staticmethod
    async def save_json(data, filepath):
        """
        주어진 데이터를 비동기 방식으로 JSON 파일로 저장하는 메서드.

        Args:
            data (dict): JSON으로 저장할 데이터.
            filepath (str): 저장할 파일의 경로.
        """

        # aiofiles를 사용하여 비동기적으로 파일을 엶.
        async with aiofiles.open(filepath, "w", encoding="utf-8") as f:
            # 데이터를 JSON 형식으로 변환하여 파일에 씀.
            await f.write(json.dumps(data, ensure_ascii=False, indent=4))