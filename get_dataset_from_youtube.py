# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 12:57:58 2021

@author: feres
"""

import subprocess
import csv, sys
import os
import wave
import contextlib
import argparse
import youtube_dl
#import ffmpeg


project_path = os.path.dirname(os.path.abspath(__file__))
#project_path = "D:/Sistemas de Informação/TCC"
balanced_train_segments = project_path+"/segments/subset_balanced_train_segments.csv"
unbalanced_train_segments = project_path+"/segments/1600max_subset_unbalanced_train_segments.csv"
eval_segments = project_path+"/segments/subset_eval_segments.csv"
data_path = project_path+"/data/"
duration = 10

# idea from : https://github.com/lccambiaghi/02456-Project---Background-Audio-Classification
# specify the index of files that is downloaded last time (to resume downloading)
last_processed_row = 0

def create_error_file(vId, idx, path):
    with open(path + idx + '_' + vId + '_ERROR.wav', 'a'):
        os.utime(path + idx + '_' + vId + '_ERROR.wav', None)

def youtube_download_os_call(vId, start_time, duration, path) :    
    command = 'ffmpeg -n -ss ' + start_time + ' -t ' + duration +' -i $(youtube-dl -i -w --extract-audio --audio-format wav --audio-quality 0 --get-url https://www.youtube.com/watch?v=' + vId + ') -t ' + duration + ' -f wav ' + vId + '.wav'
    # This is used in windows as the PATH is not taken into consideration in os.system
    
    try:
        ret = subprocess.run(['powershell','-command', command], timeout=10).returncode
    except:
        ret = -1


    return ret

def youtube_downloader(vId, start_time, duration, path):    
    print('ffmpeg -n -ss ' + start_time + ' -t ' + duration +' -i $(youtube-dl -i -w --extract-audio --audio-format wav --audio-quality 0 --get-url https://www.youtube.com/watch?v=' + vId + ') -t ' + duration + ' -f wav ' + vId + '.wav')
    ret = youtube_download_os_call(vId, start_time, duration, path)
    return ret



# def create_error_file(path,id, idx):
#     with open(path + "errors.txt", "a") as myfile:
#         myfile.write(idx + '_' + id +"\n")


def download_data(segments,subfolder):

    rownum = 0

    #if not os.path.exists(data_path+subfolder+'video/'):
        #os.makedirs(data_path+subfolder+'video/')
    if not os.path.exists(data_path+subfolder+'audio/'):
        os.makedirs(data_path+subfolder+'audio/')


    with open(segments, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if rownum <= last_processed_row + 3:
                  rownum += 1
                  continue
                # Skip the 3 line header
                if rownum >= 3:
                    print(row)

                    # if (os.path.exists(data_path + subfolder +'video/'+ str(rownum - 3) + '_' + row[0] + '.mp4')):
                    #     print("file exists, skipping...")
                    #     rownum += 1
                    #     continue

                    #ret = youtube_downloader(data_path,subfolder, row[0], str(float(row[1].lstrip())), str(rownum - 3))
                    ret = youtube_downloader(row[0], str(float(row[1].lstrip())), str(duration), path)
                    # If there was an error downloading the file
                    # This sometimes happens if videos are blocked or taken down
                    if ret != 0:
                        #create_error_file(data_path+subfolder,row[0], str(rownum - 3))
                        create_error_file(row[0], str(rownum - 3), path)

                rownum += 1
                if(rownum % 1000 == 0): 
                    print(rownum)

        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(segments, reader.line_num, e))




if __name__ == '__main__':


    parser = argparse.ArgumentParser(
        description='Directy download from youtube the videos and audio files of youtube audioset.')
    parser.add_argument('--train', action='store_true')
    parser.add_argument('--eval',  action='store_true')
    parser.add_argument('--unbalanced_train', action='store_true')


    # if len(sys.argv) < 2:
    #     parser.print_usage()
    #     sys.exit(1)

    args = parser.parse_args()


    # Only use what you need
    if args.train:
        print('Downloading balanced trainig datased defined in',balanced_train_segments)
        path = data_path+'balanced_train/audio/'
        download_data(balanced_train_segments,"balanced_train/")
    if args.eval:
        print('Downloading evaluation datased defined in',eval_segments)
        path = data_path+'eval/audio/'
        download_data(eval_segments,"eval/")
    if args.unbalanced_train:
        print('Downloading unbalanced training datased defined in',unbalanced_train_segments)
        path = data_path+'2000unbalanced_train/audio/'
        download_data(unbalanced_train_segments,"2000unbalanced_train/")