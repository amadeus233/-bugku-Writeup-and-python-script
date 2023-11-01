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
    # Use '/' for lengths greater than the average space
    elif morse_type[i] == 0:
        if morse_len[i] > morse_blank_avg:
            morse_result += "/"

print("Morse Code Result:", morse_result)

# Decode Morse code
morse_array = morse_result.split("/")
plain_text = ""
for morse in morse_array:
    if morse != '':
        plain_text += morse_dict.get(morse, '?')  # Use the get method to replace unknown Morse codes with '?'

print("Decoded Text:", plain_text)

'''version_without  string"/" in result~
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
