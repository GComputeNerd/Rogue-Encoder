import sys, subprocess, json

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

