#!/usr/bin/env python
import subprocess
import openpyxl
import sys
import os
from sys import platform
import tqdm


dataset_dir = "DR-VCTK"

download_tool = ""

if platform == "linux" or platform == "linux2":
    print ("Assuming LINUX platform... using wget to download")
    download_tool = "wget"
    # linux
elif platform == "darwin":
    # OS X
    print ("Assuming MAC platform... not yet supported!")
    sys.exit(0)
else:
    #assuming Windows...
    print ("Assuming WINDOWS platform... not yet supported!")
    sys.exit(0)


def download_expand_speech_folder (sheet=None):
    speech_dir = os.path.join(dataset_dir, sheet["A1"].value)
    if not os.path.exists (speech_dir):
        os.mkdir (speech_dir)
    
    i = 0
    for folder, download_path in tqdm.tqdm([(a.value, b.value) for a,b in sheet.rows][2:]):
        i += 1

        # handle sparse entries
        if (download_path == None):
            continue

        print ("Current download:", ' '.join(download_path.split('/')[-2:]))

        # filename the archive will be loaded to
        download_fn = folder + ".zip"

        # download the zipped folder
        download_command = f"{download_tool} {download_path} -O {download_fn} -q --show-progress"
        subprocess.call(download_command, cwd = speech_dir, shell = True)

        # unzip it
        unzip_command = f"unzip -o -q {download_fn} -d {folder} 2>/dev/null"
        subprocess.call(unzip_command, cwd = speech_dir, shell = True)

        # delete .zip archive to save space
        remove_command = f"rm {download_fn}"
        subprocess.call(remove_command, cwd = speech_dir, shell = True)

        print (f"{folder} downloaded and extracted")

    return

def expand_DR_VCTK (path="Download-links.xlsx"):
    if not os.path.exists (dataset_dir):
        os.mkdir (dataset_dir)

    wb_obj = openpyxl.load_workbook(path)
    
    ## downloading README
    #readme = wb_obj['README']
    #subprocess.call(f"{download_tool} {readme['B1'].value} -O README -q", cwd = dataset_dir, shell = True)

    # downloading and unzipping SRC
    src = wb_obj['src']
    subprocess.call(f"{download_tool} {src['B1'].value} -O src.zip -q", cwd = dataset_dir, shell = True)
    subprocess.call(f"unzip -o src.zip -d src 2>/dev/null", cwd = dataset_dir, shell = True)
    subprocess.call(f"rm src.zip", cwd = dataset_dir, shell = True)

    # donwloading and unzipping audio
    closed_window = wb_obj['DR-VCTK_Office1_ClosedWindow']
    opened_window = wb_obj['DR-VCTK_Office1_OpenedWindow']
    download_expand_speech_folder(opened_window)
    download_expand_speech_folder(closed_window)

    return




if __name__ == "__main__":
    if len (sys.argv) == 1:
        expand_DR_VCTK ()
    elif len (sys.argv) == 2:
        expand_DR_VCTK (sys.argv[1])
    else:
        print ("too many arguments")
        sys.exit(0)
