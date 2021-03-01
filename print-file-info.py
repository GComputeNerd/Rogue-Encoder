import sys, subprocess, json
from os import system
import bullet

show_usage = (
        f'{sys.argv[0]}'
        f'\n{"-"*len(sys.argv[0])}'
        f'\nUsage: python {sys.argv[0]} filename.extension\n'
        f'\nExample Usage : '
        f'\npython {sys.argv[0]} Cat\\ Video.mp4\n'
)

# Checking Arguments
if (len(sys.argv) != 2):
    print(show_usage)
    print("Error : Invalid Number of Arguments")
    exit()

info = subprocess.run(["ffprobe","-v","quiet","-print_format","json","-show_format","-show_streams",sys.argv[1]],
        stdout=subprocess.PIPE)

if (info.returncode != 0):
    print("It appears ffprobe has ran into an error. The output is given below. This might have occured because you wrote the wrong file path.")
    print(info.stdout)
    exit()

info = json.loads(info.stdout)
det = info['format']
streams = info['streams']
index = {
        'video': [i for i in range(len(streams)) 
            if (streams[i]['codec_type']) == 'video'],
        'audio': [i for i in range(len(streams))
            if (streams[i]['codec_type']) == 'audio'],
        'subtitle': [i for i in range(len(streams))
            if (streams[i]['codec_type']) == 'subtitle'],
        'attachment': [i for i in range(len(streams))
            if (streams[i]['codec_type']) == 'attachment']
        }

del info

print("\nInfo Retrieved")
print("-"*14)
print(
        f"Filename = {det['filename']}"
        f"\nNum. of Streams = {det['nb_streams']}"
        f"\nFormat = {det['format_long_name']}"
        f"\nDuration = {float(det['duration'])/60} mins\n"
        )

check = bullet.YesNo("Continue?").launch()

if (not check):
    print("Thank You For Opening This Program !")
    exit()

system('clear')
print("Lezz GO")
