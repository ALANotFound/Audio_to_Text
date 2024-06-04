import os
import glob
import shutil

from Ifasr_new import start

"""
使用步骤:
    1.填入密钥
    2.填入你的音频文件根目录(支持深层目录搜索)
    3.运行代码

注:代码会在音频文件原地址处生成一个新目录,包含音频文件和转录文本
"""

# 1.密钥
appid = ""
secret_key = ""

# 2.目录
audioFile_root_dir_path = 'path/to/your/dir'  
# 例如: audioFile_root_dir_path = '/mntcephfs/lab_data/youjiajun/Tdata_降噪/test' 

def find_wav_files(root_dir):
    all_files = []
    audio_extensions = ['.wav', '.mp3', '.pcm', '.aac', '.opus', '.flac', '.ogg', '.m4a', '.amr', '.speex', '.lyb', '.ac3', '.ape', '.m4r', '.mp4', '.acc', '.wma']
    # 遍历根目录及其所有子文件夹
    for dirpath, dirnames, filenames in os.walk(root_dir): # 生成一个三元组，包含当前路径、该路径下的子目录列表以及文件名列表
        for filename in glob.glob(os.path.join(dirpath, f'*{audio_extensions}')):
            all_files.append(filename)
            print(f"已匹配到音频文件{filename}")
    return all_files

def dir_check(file_path):
    # 检查目录格式是否合规
    wav_files = [file for file in os.listdir(os.path.dirname(file_path)) if file.endswith('.wav')]
    txt_files = [file for file in os.listdir(os.path.dirname(file_path)) if file.endswith('.txt')]

    # 检查是否同时存在 .wav 和 .txt 文件
    if len(wav_files) == 1 and len(txt_files) == 1:
        print("该音频文件已处理过了,请删去转录文本再尝试运行")
        return -1
    else:
        return 1

def create_folder_from_file(file_path):

    # 从文件路径中提取文件名（包括后缀）
    file_name_with_extension = os.path.basename(file_path)
    
    # 分离文件名和后缀
    file_name, file_extension = os.path.splitext(file_name_with_extension)
    
    # 构建新的文件夹路径
    new_folder_path = os.path.join(os.path.dirname(file_path), file_name)
    
    os.makedirs(new_folder_path, exist_ok=True)

    # 构建文件移动的目标路径
    destination_file_path = os.path.join(new_folder_path, file_name + '.wav')
    
    
    # 将文件移动到新创建的文件夹中
    shutil.move(file_path, destination_file_path)

    output_file = os.path.join(new_folder_path, file_name + '.txt')

    return destination_file_path, output_file

if __name__ == "__main__":
    files = find_wav_files(audioFile_root_dir_path)
    for file in files:
        print(f"正在转录:{file}")
        if dir_check(file) == -1:
            continue
        else:
            new_file_path, transcription = create_folder_from_file(file)
            start(appid, secret_key, new_file_path, transcription)
