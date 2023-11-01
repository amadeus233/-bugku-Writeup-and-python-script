import math
import numpy as np
import wave
import pylab
from tqdm import tqdm


# 摩斯电码字典
morse_dict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z',
    '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
    '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0',
    '.-.-.-': '.', '---...': ':', '--..--': ',', '-.-.-.': ';', '..--..': '?',
    '-...-': '=', '.----.': '\'', '-..-.': '/', '-.-.--': '!', '-....-': '-',
    '..--.-': '_', '.-..-.': '"', '-.--.': '(', '-.--.-': ')', '...-..-': '$',
    '.-...': '&', '.--.-.': '@'
}

# 打开音频文件
audio = wave.open('music.wav', 'rb')  # 使用音频文件名打开音频文件

# 读取音频信息
params = audio.getparams()
print("音频信息：", params)
n_channels, _, sample_rate, n_frames = params[:4]

# 设置图形分辨率
pylab.figure(dpi=200, figsize=(1000000 / n_frames * 50, 2))

# 读取频谱信息
str_wave_data = audio.readframes(n_frames)
audio.close()

# 将频谱信息转为数组
wave_data = np.frombuffer(str_wave_data, dtype=np.short).T

# 计算平均频率
wave_avg = int(sum([abs(x / 10) for x in wave_data]) / len(wave_data)) * 10
print("平均频率：", wave_avg)

# 绘制摩斯电码图像
morse_block_sum = 0  # 待划分的数据
morse_block_length = 0  # 待划分的数据长度
morse_arr = []
time_arr = []
pbar = tqdm(wave_data, desc="绘制摩斯电码图像")
for i in pbar:
    # 高于平均值记为 1，反之为 0
    if abs(i) > wave_avg:
        morse_block_sum += 1
    else:
        morse_block_sum += 0
    morse_block_length += 1
    # 将数据按照指定长度划分
    if morse_block_length == 100:
        # 计算划分块的平均值
        if math.sqrt(morse_block_sum / 100) > 0.5:
            morse_arr.append(1)
        else:
            morse_arr.append(0)
        # 横坐标
        time_arr.append(len(time_arr))
        morse_block_length = 0
        morse_block_sum = 0

# 保存图像
pylab.plot(time_arr, morse_arr)
pylab.savefig('result.png')

# 摩斯电码按信号长度存储
morse_type = []
morse_len = []
# 摩斯电码长度 0  1
morse_obj_sum = [0, 0]
morse_obj_len = [0, 0]
for i in morse_arr:
    if len(morse_type) == 0 or morse_type[-1] != i:
        morse_obj_len[i] += 1
        morse_obj_sum[i] += 1
        morse_type.append(i)
        morse_len.append(1)
    else:
        if morse_len[-1] <= 100:
            morse_obj_sum[i] += 1
            morse_len[-1] += 1

# 计算信息与空位的平均长度
morse_block_avg = morse_obj_sum[1] / morse_obj_len[1]
print("摩斯电码信号平均长度：", morse_block_avg)
morse_blank_avg = morse_obj_sum[0] / morse_obj_len[0]
print("摩斯电码空位平均长度：", morse_blank_avg)

# 转换为摩斯电码
morse_result = ""
for i in range(len(morse_type)):
    if morse_type[i] == 1:
        # 大于平均长度为"-"
        if morse_len[i] > morse_block_avg:
            morse_result += "-"
        # 小于平均长度即为"."
        elif morse_len[i] < morse_block_avg:
            morse_result += "."
    # 大于平均空位长度的为分割
    elif morse_type[i] == 0:
        if morse_len[i] > morse_blank_avg:
            morse_result += "/"

print("摩斯电码结果：", morse_result)

# 摩斯电码解码
morse_array = morse_result.split("/")
plain_text = ""
for morse in morse_array:
    if morse != '':
        plain_text += morse_dict.get(morse, '?')  # 使用get方法，未知的摩斯电码用'?'代替

print("解码后的文本：", plain_text)

''' 将/替换回空格(space)的代码(其实都差不多)
import math
import numpy as np
import wave
import pylab
from tqdm import tqdm

# Morse code dictionary
morse_dict = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
    '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
    '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
    '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
    '-.--': 'Y', '--..': 'Z',
    '.----': '1', '..---': '2', '...--': '3', '....-': '4', '.....': '5',
    '-....': '6', '--...': '7', '---..': '8', '----.': '9', '-----': '0',
    '.-.-.-': '.', '---...': ':', '--..--': ',', '-.-.-.': ';', '..--..': '?',
    '-...-': '=', '.----.': '\'', '-..-.': '/', '-.-.--': '!', '-....-': '-',
    '..--.-': '_', '.-..-.': '"', '-.--.': '(', '-.--.-': ')', '...-..-': '$',
    '.-...': '&', '.--.-.': '@'
}

# Open the audio file
audio = wave.open('music.wav', 'rb')  # Open the audio file using the filename

# Read audio information
params = audio.getparams()
print("Audio Information:", params)
n_channels, _, sample_rate, n_frames = params[:4]

# Set the resolution of the graph
pylab.figure(dpi=200, figsize=(1000000 / n_frames * 50, 2))

# Read spectrum information
str_wave_data = audio.readframes(n_frames)
audio.close()

# Convert spectrum information to an array
wave_data = np.frombuffer(str_wave_data, dtype=np.short).T

# Calculate the average frequency
wave_avg = int(sum([abs(x / 10) for x in wave_data]) / len(wave_data)) * 10
print("Average Frequency:", wave_avg)

# Draw the Morse code image
morse_block_sum = 0  # Data to be segmented
morse_block_length = 0  # Length of data to be segmented
morse_arr = []
time_arr = []
pbar = tqdm(wave_data, desc="Drawing Morse Code Image")
for i in pbar:
    # Mark as 1 if above average, otherwise 0
    if abs(i) > wave_avg:
        morse_block_sum += 1
    else:
        morse_block_sum += 0
    morse_block_length += 1
    # Segment the data according to the specified length
    if morse_block_length == 100:
        # Calculate the average value of the segment
        if math.sqrt(morse_block_sum / 100) > 0.5:
            morse_arr.append(1)
        else:
            morse_arr.append(0)
        # X-axis
        time_arr.append(len(time_arr))
        morse_block_length = 0
        morse_block_sum = 0

# Save the image
pylab.plot(time_arr, morse_arr)
pylab.savefig('result.png')

# Store Morse code by signal length
morse_type = []
morse_len = []
# Morse code length 0  1
morse_obj_sum = [0, 0]
morse_obj_len = [0, 0]
for i in morse_arr:
    if len(morse_type) == 0 or morse_type[-1] != i:
        morse_obj_len[i] += 1
        morse_obj_sum[i] += 1
        morse_type.append(i)
        morse_len.append(1)
    else:
        if morse_len[-1] <= 100:
            morse_obj_sum[i] += 1
            morse_len[-1] += 1

# Calculate the average length of signal and space
morse_block_avg = morse_obj_sum[1] / morse_obj_len[1]
print("Average Length of Morse Signal:", morse_block_avg)
morse_blank_avg = morse_obj_sum[0] / morse_obj_len[0]
print("Average Length of Morse Space:", morse_blank_avg)

# Convert to Morse code
morse_result = ""
for i in range(len(morse_type)):
    if morse_type[i] == 1:
        # '-' for lengths greater than the average
        if morse_len[i] > morse_block_avg:
            morse_result += "-"
        # '.' for lengths less than the average
        elif morse_len[i] < morse_block_avg:
            morse_result += "."
    # Use ' ' (space) for lengths greater than the average space
    elif morse_type[i] == 0:
        if morse_len[i] > morse_blank_avg:
            morse_result += " "

print("Morse Code Result:", morse_result)

# Decode Morse code
morse_array = morse_result.split(" ")
plain_text = ""
for morse in morse_array:
    if morse != '':
        plain_text += morse_dict.get(morse, '?')  # Use the get method to replace unknown Morse codes with '?'

print("Decoded Text:", plain_text)

'''
