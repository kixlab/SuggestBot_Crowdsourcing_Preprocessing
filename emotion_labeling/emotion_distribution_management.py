import json
import scipy.ndimage.filters as fi
from .models import *
import numpy as np
MIN_DATA_NUM_FOR_EXAMPLE = 5


# function that builds example
def build_examples():
    exp_videos = Emotion_Distribution_Collection.objects.all().values_list('experiment_video', flat=True).distinct()
    print(exp_videos)
    for exp_video in exp_videos:
        exp_video_times = Emotion_Distribution_Collection.objects.filter(experiment_video = exp_video).values_list('time', flat=True).distinct()
        for exp_video_time in exp_video_times:
            print(exp_video_time)
            dist_objs = Emotion_Distribution_Collection.objects.filter(experiment_video = exp_video, time = exp_video_time)
            if dist_objs.count()>=MIN_DATA_NUM_FOR_EXAMPLE:
                dist = None
                for dist_obj in dist_objs:
                    if dist is None:
                        dist = np.asarray(json.loads(dist_obj.distribution))
                    else:
                        dist = dist + np.asarray(json.loads(dist_obj.distribution))
                    print(dist)
                dist = json.dumps(dist.tolist())
                #save the distribution as example
                candi_example = Emotion_Distribution_Example.objects.filter(experiment_video = exp_video, time = exp_video_time)
                if candi_example.count()>0:
                    candi_example[0].distribution = dist
                    candi_example[0].save()
                else:
                    exp_vd = Experiment_Video.objects.get(id=exp_video)
                    print(exp_vd)
                    new_example = Emotion_Distribution_Example(experiment_video = exp_vd, time = exp_video_time, distribution = dist)
                    new_example.save()
    return
# TODO function that picks 'representative' examples
def extract_representative_examples(task_to_throw, NUM_OF_EXAMPLES = 3):
    example_sources=[]
    example_seconds=[]
    example_distributions=[]
    example_figs=[]
    example_objs = []
    examples = Emotion_Distribution_Example.objects.all()
    for i in range(NUM_OF_EXAMPLES):
        example_sims = np.zeros(examples.count())
        # change below to gauge examples that appear
        if i == 0:
            kernel = point_gaussian(5, 5)
        elif i == 1:
            kernel = point_gaussian(5, 1)
        elif i == 2:
            kernel = point_gaussian(3, 3)
        elif i == 3:
            kernel = vertical_gaussian(2)
        elif i == 4:
            kernel = vertical_gaussian(4)
        elif i == 5:
            kernel = horizontal_gaussian(3)
        for index, example in enumerate(examples):
            distribution = np.asarray(json.loads(example.distribution))
            cur_sim = np.sum(np.multiply(kernel, distribution))
            example_sims[index] = cur_sim
        print(example_sims)
        ranking = np.argsort(example_sims)
        ranking = ranking[::-1]
        rank_id=0
        print(examples[int(ranking[rank_id])])

        while examples[int(ranking[rank_id])] in example_objs:
            rank_id = rank_id + 1
        if rank_id<len(examples):
            example_objs.append(examples[int(ranking[rank_id])])
            example_sources.append(example_objs[-1].experiment_video.video_url)
            example_seconds.append(example_objs[-1].time)
            example_distributions.append(json.loads(example_objs[-1].distribution))
            example_figs.append(example_objs[-1].experiment_video.video_img)
    print(example_objs)
    task_to_throw['target_video_source'] = json.dumps(example_sources)
    task_to_throw['target_second'] = json.dumps(example_seconds)
    task_to_throw['target_video_distribution'] = json.dumps(example_distributions)
    task_to_throw['target_img'] = json.dumps(example_figs)
    return task_to_throw

def point_gaussian(arousal, valence):
    inp = np.zeros((7,7))
    inp[arousal, valence] = 1
    inp = fi.gaussian_filter(inp, 1)
    return inp

def vertical_gaussian(valence):
    inp = np.zeros((7,7))
    for i in range(7):
        inp[i, valence] = 1/7
    inp = fi.gaussian_filter(inp, 1)
    return inp

def horizontal_gaussian(arousal):
    inp = np.zeros((7,7))
    for i in range(7):
        inp[arousal, i] = 1/7
    inp = fi.gaussian_filter(inp, 1)
    return inp

# TODO function that takes preliminary points and propose examples
def extract_example_from_preliminary_points(distribution_points, NUM_OF_EXAMPLES = 2):
    cur_dist_kernelized = np.asarray(distribution_points)
    total_points = np.sum(np.sum(cur_dist_kernelized))
    cur_dist_kernelized = cur_dist_kernelized/total_points
    cur_dist_kernelized = fi.gaussian_filter(cur_dist_kernelized, (1-total_points/50))

    example_sources = []
    example_seconds = []
    example_distributions = []
    example_figs = []

    examples = Emotion_Distribution_Example.objects.all()
    example_sims = np.zeros(examples.count())
    for index, example in enumerate(examples):
        distribution = np.asarray(json.loads(example.distribution))
        cur_sim = np.sum(np.multiply(cur_dist_kernelized, distribution))
        example_sims[index] = cur_sim
    ranking = np.argsort(example_sims)
    ranking = ranking[::-1]
    for i in range(NUM_OF_EXAMPLES):
        ex_obj = examples[int(ranking[i])]
        example_sources.append(ex_obj.experiment_video.video_url)
        example_seconds.append(ex_obj.time)
        example_distributions.append(json.loads(ex_obj.distribution))
        example_figs.append(ex_obj.experiment_video.video_img)

        to_return = {
            'target_second' : example_seconds,
            'target_video_source' : example_sources,
            'target_video_distribution' : example_distributions,
            'target_img' : example_figs,
        }
    return to_return
