from pydub import AudioSegment
import os
AudioSegment.ffmpeg = "/opt/homebrew/Cellar/ffmpeg"
AudioSegment.ffprobe = "/opt/homebrew/Cellar/ffprobe"

def split_audio(file_path, output_dir, segment_length=10000):
    """
    음성 파일을 segment_length 밀리초 단위로 쪼갭니다.
    
    :param file_path: 쪼개고자 하는 음성 파일의 경로
    :param output_dir: 쪼개진 파일들이 저장될 디렉토리
    :param segment_length: 쪼개고자 하는 길이 (밀리초 단위, 기본값 10000ms = 10초)
    """
    audio = AudioSegment.from_file(file_path,format="m4a")
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i in range(0, len(audio), segment_length):
        segment = audio[i:i+segment_length]
        segment_path = os.path.join(output_dir, f"{file_name}_part{i//segment_length}.m4a")
        segment.export(segment_path, format="ipod")
        print(f"Saved {segment_path}")

# 사용 예시
input_file = "test_voice.m4a"
output_directory = "preprocess"

split_audio(input_file, output_directory)