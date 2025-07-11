import os
import json
from tqdm import tqdm
import decord
import cv2
import random
from multiprocessing import Process
import gc
import psutil
BATCH_SIZE = 100

def get_memory_mb():
    """current process memory usage (MB)"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def split_video_decord(video_reader, segment, save_path, is_frame=False):
    fps = video_reader.get_avg_fps()

    if is_frame:
        start_frame_index, end_frame_index = segment
    else:
        start_time, end_time = segment
        start_frame_index = int(start_time * fps)
        end_frame_index = int(end_time * fps)

    end_frame_index = min(end_frame_index, len(video_reader))
    if start_frame_index >= end_frame_index:
        raise ValueError("Invalid segment: start_frame_index must be less than end_frame_index")

    sample_frame = video_reader[start_frame_index].asnumpy()
    frame_height, frame_width = sample_frame.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height))

    ## edit here too many memory usage
    for idx in range(start_frame_index, end_frame_index):
        frame = video_reader[idx].asnumpy()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video_writer.write(frame_bgr)

    video_writer.release()

def get_vid_list(json_data, instruction_data):
    ins_vid_list = []
    with open(instruction_data, 'r') as f:
        raw_data = f.readlines()
        for item in raw_data:
            item = json.loads(item)
            if item['type'] == 'video':
                vid_name = item['video'].split('/')[-1][:-4]
                if vid_name not in ins_vid_list: ins_vid_list.append(vid_name)
    vid_list = []
    for vid_name in json_data.keys():
        if vid_name in ins_vid_list:
            vid_list.append(vid_name)
    return vid_list

def process(vid_list, video_root, json_data, event_save_path, clip_save_path):
    p_bar = tqdm(vid_list)
    for vid_name in p_bar:
        video_path = os.path.join(video_root, vid_name+'.mp4')
        video_reader = decord.VideoReader(video_path)
        vid_events = json_data[vid_name]['events']
        vid_clips = json_data[vid_name]['clips']
        for e_idx, event in enumerate(vid_events):
            e_dir = os.path.join(event_save_path, "{}_E{}.mp4".format(vid_name, e_idx))
            if not os.path.exists(e_dir): 
                split_video_decord(video_reader, event, e_dir, is_frame=False)
            p_bar.set_description("[Processing-{}-E{}]".format(e_idx, vid_name))
            for c_idx, clip in enumerate(vid_clips[e_idx]):
                c_dir = os.path.join(clip_save_path, "{}_E{}C{}.mp4".format(vid_name, e_idx, c_idx))
                if not os.path.exists(c_dir):
                    split_video_decord(video_reader, clip, c_dir, is_frame=False)
                p_bar.set_description("[Processing-{}-E{}C{}]".format(vid_name, e_idx, c_idx))


def segment(dataset, subset, n_thread=1):
    instruction_data = "./instruction/merge_instruction_{}_final.jsonl".format(subset)
    if 'ucf' in dataset:
        json_data = './raw_annotations/ucf_database_{}.json'.format(subset)
    elif 'xd' in dataset:
        json_data = './raw_annotations/xd_database_{}.json'.format(subset)
    video_root = './videos/{}/videos/{}'.format(dataset, subset)
    event_save_path = './videos/{}/events/{}'.format(dataset, subset)
    clip_save_path = './videos/{}/clips/{}'.format(dataset, subset)
    mkdir(clip_save_path)
    mkdir(event_save_path)
    
    with open(json_data, 'r') as f:
        json_data = json.load(f)
    vid_list = get_vid_list(json_data, instruction_data)
    random.shuffle(vid_list)

    batch = len(vid_list) // n_thread
    process_list = []
    for n in range(n_thread):
        videos = vid_list[batch*n:batch*(n+1)]
        p = Process(target=process, args=(videos, video_root, json_data, event_save_path, clip_save_path))
        p.start()
        process_list.append(p)
    if len(vid_list)%n_thread != 0:
        videos = vid_list[batch*n_thread:]
        p = Process(target=process, args=(videos, video_root, json_data, event_save_path, clip_save_path))
        p.start()
        process_list.append(p)

    for p in process_list:
        p.join()

    print('Done')

if __name__ == '__main__':
    import argparse
    import time
    import multiprocessing
    
    parser = argparse.ArgumentParser(description="Video segmentation runner") 
    parser.add_argument('-n_thrd','--n_thread' , type=int, default=12,
                        help="Number of thread to use for multiprocessing(default:12)")
    args = parser.parse_args()
    t_start = time.perf_counter() 
    
    n_thread = args.n_thread
    max_threads = multiprocessing.cpu_count()
    n_thread = min(args.n_thread, max_threads)
    print(f"[INFO] Requested threads: {args.n_thread}, limited to: {n_thread} (System max: {max_threads})")

    segment('ucf-crime', 'test', n_thread=n_thread)
    segment('xd-violence', 'test', n_thread=n_thread)
    segment('ucf-crime', 'train', n_thread=n_thread)
    segment('xd-violence', 'train', n_thread=n_thread)

    t_end = time.perf_counter()
    print('Running time: %s Seconds'%(t_end-t_start))
