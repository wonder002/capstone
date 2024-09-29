from pydub import AudioSegment

class AudioProcessor:
    @staticmethod
    async def preprocess(input_path, output_path):
        # WAV 파일 로드
        audio = AudioSegment.from_wav(input_path)
        # 샘플 레이트를 16kHz로 변경 (Whisper 모델 요구사항)
        audio = audio.set_frame_rate(16000)
        # 처리된 오디오를 WAV 형식으로 저장
        audio.export(output_path, format="wav")