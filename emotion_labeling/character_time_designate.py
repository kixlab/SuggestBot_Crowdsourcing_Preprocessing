import base64
from .models import *
import math
import json

TIME_DESIG_INTERVAL=15
TIME_DESIG_OFFSET = 15
MAXIMUM_TIME_POINTS = 7

def save_character_time_data(to_return, title, url):
    exp_video_num = 0
    for index, time_data in enumerate(to_return['figure_time_data']):
        image_data = to_return['figure_images'][index]
        #save image
        content = image_data.split(';')[1]
        image_encoded = content.split(',')[1]
        image_to_save = base64.decodebytes(image_encoded.encode('utf-8'))
        img_file = open("./preprocessing/static/img/figures/experiment/"+title+str(index)+".png", 'wb')
        img_file.write(image_to_save)
        img_file.close()
        #save time data
        time_points = []
        for time_range in time_data:
            for i in range(math.ceil(time_range[0]), math.floor(time_range[1])+1):
                time_points.append(i)
        time_points.sort()
        total_group_num = math.ceil((len(time_points)-TIME_DESIG_OFFSET)/TIME_DESIG_INTERVAL/MAXIMUM_TIME_POINTS)
        exp_video_objs = []
        exp_video_prompt_times = []
        for i in range(0, total_group_num):
            exp_video_obj = Experiment_Video(video_title = title+str(exp_video_num), video_url = url, video_img = title+str(index))
            exp_video_objs.append(exp_video_obj)
            exp_video_prompt_times.append({})
            exp_video_num = exp_video_num + 1
        cur_time = TIME_DESIG_OFFSET
        cur_video_obj_num = 0
        while cur_time < len(time_points):
            exp_video_prompt_times[cur_video_obj_num][time_points[cur_time]] = False
            cur_video_obj_num = (cur_video_obj_num +1)%total_group_num
            cur_time = cur_time + TIME_DESIG_INTERVAL
        for i in range(0, total_group_num):
            exp_video_objs[i].video_prompt_time = json.dumps(exp_video_prompt_times[i])
            exp_video_objs[i].video_prompt_num = len(exp_video_prompt_times[i])
            exp_video_objs[i].video_total_time = max(list(exp_video_prompt_times[i].keys()))+10
            exp_video_objs[i].save()
