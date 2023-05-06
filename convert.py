import cv2
import os
import requests
import time
import glob

def save_all_frames(video_path, dir_path, basename, ext='jpg'):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    os.makedirs(dir_path, exist_ok=True)
    base_path = os.path.join(dir_path, basename)

    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))

    n = 0

    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('{}_{}.{}'.format(base_path, str(n).zfill(digit), ext), frame)
            n += 1
        else:
            return
        
def convert_jpg2svg(dir_path,prefix,result_path,api_kei):
    frames = len(glob.glob(f"{dir_path}/*.jpg"))
    for i in range(frames, result_path, ):
        response = requests.post(
            'https://vectorizer.ai/api/v1/vectorize',
            files={'image': open(f"{dir_path}/{prefix}_{str(i).zfill(2)}.jpg", 'rb')},
            headers={
                'Authorization':
                api_kei
            },
        )
        if response.status_code == requests.codes.ok:
            # Save result
            os.makedirs(dir_path, exist_ok=True)
            with open(f'{result_path}/result{i}.svg', 'wb') as out:
                out.write(response.content)
                i+=1
        else:
            print("Error:", response.status_code, response.text)
            if(response.status_code==429):
                time.sleep(5)
            else:
                break

if __name__ == "__main__": 
    movie_path = 'sampleMovie.mov'#変換したい動画のファイルパス
    dir_path = 'resultimg'
    result_path = 'result'
    prefix = 'sample_video_img'
    api_kei = ''#Vectorize AI のAPIキー

    save_all_frames(movie_path, dir_path, prefix)
    convert_jpg2svg(dir_path,prefix,result_path,api_kei)