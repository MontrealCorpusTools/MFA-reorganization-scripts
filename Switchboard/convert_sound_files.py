import subprocess
import os
import re
import sys

SPH_REGEX = re.compile(".*\.sph$")

def convert_directory(input_dir, output_dir):
    """
    convert the .sph sound files in input_dir to .wav in destination_dir
    checks first if there's a .textgrid for the sound file, since there are many 
    more sound files than textgrids
    """

    done = set()
    for root, dirs, files in os.walk(input_dir):
        for file in sorted(files):
            if SPH_REGEX.match(file) is not None:
                filename = os.path.join(root, file)
                if filename in done:
                    return
                
                just_name = file.split(".")[0]
                just_num = int(just_name[2:])
                
                if os.path.exists(os.path.join(output_dir, "sw"+"0"+str(just_num) +".textgrid")):
                    print(filename)
                    subprocess.call(['ffmpeg', '-i', filename, '-y', os.path.join(output_dir, just_name + ".wav")])
                    done.update(filename)


def convert_file(path, destination):
    file = os.path.split(path)[-1]
    just_name = file.split(".")[0]

    subprocess.call(['ffmpeg', '-i', path, '-y', '-hide_banner', os.path.join(destination, just_name + ".wav")])




if __name__ == '__main__':
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    # convert_directory(input_dir, output_dir)
    sf_locations = {}
    for root,dirs,files in os.walk(input_dir):
        for file in files:
            if file.endswith(".sph"):
                name = file.split(".")[0]
                path = os.path.join(root, file)
                sf_locations.update({name:path})

    unfound = 0
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".textgrid"):
                name = file.split(".")[0]
                try: 
                    path = sf_locations[name]
                    convert_file(path, output_dir)
                except KeyError:
                    print("no path for ", name)
                    unfound +=1

    print("unfound: ", unfound)








