import sys, subprocess, json
from os import system
import bullet
import re

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

del info

# Stream Info

vInfo = lambda streams, i : print(
        f"Codec Type = video\n"
        f"Codec Name = {streams[i]['codec_name']}\n"
        f"Codec Long Name = {streams[i]['codec_long_name']}\n"
        f"Profile = {streams[i]['profile']}\n"
        f"Width = {streams[i]['width']}\n"
        f"Height = {streams[i]['height']}\n"
        f"Aspect Ratio = {streams[i]['display_aspect_ratio']}\n"
        f"Average Frame Rate = { int(streams[i]['avg_frame_rate'].split('/')[0]) / int(streams[i]['avg_frame_rate'].split('/')[1])}\n"
        f"Pixel Format = {streams[i]['pix_fmt']}\n"
) # The weird {} calculates average frame rate

aInfo = lambda streams, i : print(
        f"Codec Type = audio\n"
        f"Codec Name = {streams[i]['codec_name']}\n"
        f"Codec Long Name = {streams[i]['codec_long_name']}\n"
        f"Sample Format = {streams[i]['sample_fmt']}\n"
        f"Sample Rate = {streams[i]['sample_rate']}\n"
        f"Channels = {streams[i]['channels']}\n"
        f"Channel Layout = {streams[i]['channel_layout']}\n"
)

sInfo = lambda streams, i : print(
        f"Codec Type = subtitle\n"
        f"Codec Name = {streams[i]['codec_name']}\n"
        f"Codec Long Name = {streams[i]['codec_long_name']}\n"
        f"Duration = {float(streams[i]['duration'])/60} mins\n"
)

nl = "\n" # fstrings can't use backslashes T_T
atInfo = lambda streams, i : print(
        f"Codec Type = attachment\n"
        f"Tags :-\n"
        f"{nl.join([f'''{n} = {streams[i]['tags'][n]}''' for n in streams[i]['tags'].keys()])}"
)

index = {
        'video': [],
        'audio': [],
        'subtitle': [],
        'attachment': []
        }

for i in range(len(streams)):
    
    codecType = streams[i]['codec_type']

    if (codecType == 'video'):
        index['video'] += [i]
    elif (codecType == 'audio'):
        index['audio'] += [i]
    elif (codecType == 'subtitle'):
        index['subtitle'] += [i]
    elif (codecType == 'attachment'):
        index['attachment'] += [i]

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
stay = True

# Main Prompt
cli_main = bullet.Bullet(
        prompt = "\nCurrent Location : Home\n\nOptions :-",
        choices = ['File Info', 'Streams', 'Video', 'Audio', 'Subtitles', 'Attachments', 'Quit']
        )

while (stay):
    system('clear')
    print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
    choice = cli_main.launch()

    if (choice == 'File Info'):
        system('clear')
        print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
        print("\nCurrent Location : File Info\n")
        print(
            f"Filename = {det['filename']}"
            f"\nNum. of Streams = {det['nb_streams']}"
            f"\nFormat = {det['format_long_name']}"
            f"\nDuration = {float(det['duration'])/60} mins\n"
        )
        bullet.Bullet(
                choices = ['Back']
                ).launch()

    elif (choice == 'Streams'):
        while True:
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print("\nCurrent Location : Streams\n")

            # Choice
            choice = bullet.Bullet(
                    prompt = "Select Stream Number",
                    choices = [f"[{i}] type = {streams[i]['codec_type']}" for i in range(len(streams))] + ['Back']
                    ).launch()

            if (choice == 'Back'):
                break
            else:
                i = int(re.search(r"[(\d)]", choice).group()) # Selected stream index
                codecType = streams[i]['codec_type']

                system('clear')
                print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
                print(f"\nCurrent Location : Stream [{i}]\n")

                print("Stream Info :-")

                # Print Stream information acc. to Codec Type
                if (codecType == 'video'):
                    vInfo(streams, i)
                elif (codecType == 'audio'):
                    aInfo(streams, i)
                elif (codecType == 'subtitle'):
                    sInfo(streams, i)
                elif (codecType == 'attachment'):
                    atInfo(streams, i)

                bullet.Bullet(
                        choices = ["Back"]
                        ).launch()

    elif (choice == 'Video'):
        while True:
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print("\nCurrent Location : Video\n")

            if (len(index['video']) == 0):
                print("No Video Streams Found")
                bullet.Bullet(
                        choices=['Back']
                        ).launch()
                break

            choice = bullet.Bullet(
                    prompt = "Streams :-",
                    choices = [str(s) for s in index['video']] + ['Back']
                    ).launch()

            if (choice == 'Back'):
                break
            
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print(f"\nCurrent Location : Video [Stream [{choice}]]\n")

            vInfo(streams, int(choice))

            bullet.Bullet(
                    choices = ["Back"]
                    ).launch()

    elif (choice == 'Audio'):
        while True:
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print("\nCurrent Location : Audio\n")

            if (len(index['audio']) == 0):
                print("No Audio Streams Found")
                bullet.Bullet(
                        choices=['Back']
                        ).launch()
                break

            choice = bullet.Bullet(
                    prompt = "Streams :-",
                    choices = [str(s) for s in index['audio']] + ['Back']
                    ).launch()

            if (choice == 'Back'):
                break
            
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print(f"\nCurrent Location : Audio [Stream [{choice}]]\n")

            aInfo(streams, int(choice))

            bullet.Bullet(
                    choices = ["Back"]
                    ).launch()

    elif (choice == 'Subtitles'):
        while True:
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print("\nCurrent Location : Subtitles\n")

            if (len(index['subtitle']) == 0):
                print("No Subtitle Streams Found")
                bullet.Bullet(
                        choices=['Back']
                        ).launch()
                break

            choice = bullet.Bullet(
                    prompt = "Streams :-",
                    choices = [str(s) for s in index['subtitle']] + ['Back']
                    ).launch()

            if (choice == 'Back'):
                break
            
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print(f"\nCurrent Location : Subtitles [Stream [{choice}]]\n")

            sInfo(streams, int(choice))

            bullet.Bullet(
                    choices = ["Back"]
                    ).launch()

    elif (choice == 'Attachments'):
        while True:
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print("\nCurrent Location : Attachments\n")

            if (len(index['attachment']) == 0):
                print("No Attachment Streams Found")
                bullet.Bullet(
                        choices=['Back']
                        ).launch()
                break

            choice = bullet.Bullet(
                    prompt = "Streams :-",
                    choices = [str(s) for s in index['attachment']] + ['Back']
                    ).launch()

            if (choice == 'Back'):
                break
            
            system('clear')
            print(sys.argv[0], "-"*len(sys.argv[0]), sep="\n")
            print(f"\nCurrent Location : Attachment [Stream [{choice}]]\n")

            atInfo(streams, int(choice))

            bullet.Bullet(
                    choices = ["Back"]
                    ).launch()

    elif (choice == 'Quit'):
        system('clear')
        print("Thank You for Using This Program!")
        exit()
