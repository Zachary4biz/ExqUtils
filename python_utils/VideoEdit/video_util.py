import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from tqdm.auto import tqdm
import itertools
import functools
import subprocess
from pydub import AudioSegment


info="""    1 cv2.CAP_PROP_POS_FRAMES 下一帧的索引（0开始）
    2 cv2.CAP_PROP_POS_AVI_RATIO  进度比例
    3 cv2.CAP_PROP_FRAME_WIDTH  宽度
    4 cv2.CAP_PROP_FRAME_HEIGHT 高度
    7 cv2.CAP_PROP_FRAME_COUNT  总帧数"""
# 文件名转义
def escape(fp):
    fp_new=os.path.join(os.path.split(fp)[0],os.path.split(fp)[1].replace(" ","_"))
    os.rename(fp,fp_new)
    return fp_new

# 1:33:22 时间转成秒
def timeparse(timeStr):
    times=(['0']*3+timeStr.split(":"))[-3:]
    times=[float(i) for i in times]
    sec = times[0]*3600+times[1]*60+times[2]
    return sec

# PIP:picture in picture | 对于较短视频使用最后一帧填充
def merge_PIP(fp_list,row,col,output_fp,pad2longest=False,fps=30,width=854,height=480,auto_crop=False):
    """
    [排列]
    v1 v2 v3
    v4 v5
    [wxh的信息]
    1080p~480p: 1920x1080, 1280x720, 854x480
    [画面裁剪指令]
    ffmpeg -i <input> -vf crop=w:h:x:y -threads 5 -preset ultrafast -strict -2 <output>
    [音频提取] | <output>格式是 .aac
    ffmpeg -i <input> -vn -y -acodec copy <output>
    [自动获取第一个视频的长宽]
    v1=videoCap_list[0]
    fps = v1.get(cv2.CAP_PROP_FPS)
    width = (int(v1.get(cv2.CAP_PROP_FRAME_WIDTH)))
    height = (int(v1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    """
    videoCap_list =[cv2.VideoCapture(i) for i in fp_list]
    video_duration_ori = [cap.get(cv2.CAP_PROP_FRAME_COUNT)//cap.get(cv2.CAP_PROP_FPS) for cap in videoCap_list]
    print(f"原视频时长:")
    _ = [print(f"{fp} : {d}sec") for fp,d in zip(fp_list,video_duration_ori)]
    total_frame = [cap.get(cv2.CAP_PROP_FRAME_COUNT) for cap in videoCap_list]
    total_frame = max(total_frame) if pad2longest else min(total_frame)
    print(f"merge后的视频时长: {total_frame//fps}sec")
    assert col*row >= len(videoCap_list)

    sub_width, sub_height= width//col, height//row
    out = cv2.VideoWriter(output_fp, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))

    # [按帧读取视频]
    # .read 得到的结果是一个tuple2标记是否获取成功 (status, frame)
    pbar = tqdm(total=int(total_frame), desc="processing")
    readCap_list = [cap.read() for cap in  videoCap_list]
    sub_frame_list = []
    while (all([res[0] for res in readCap_list]) and not pad2longest) or (any([res[0] for res in readCap_list]) and pad2longest):
        last_frame_list = sub_frame_list # 用来保留上一帧，在pad2longest生效时会用最后一帧填充较短视频
        sub_frame_list = [] # 每次清空
        for idx, (status,frame) in enumerate(readCap_list):
            col_idx = idx % col
            row_idx = idx // col
            if status==False and pad2longest:
                # 较短的视频已经为获取不到frame了
                # frame = np.full(shape=(sub_width,sub_height,3), fill_value=255, dtype=np.uint8)
                # 不用空白填充，改用最后一帧填充
                frame = last_frame_list[idx][-1]
            frame_new = cv2.resize(frame, (sub_width, sub_height), interpolation=cv2.INTER_CUBIC)
            sub_frame_list.append((row_idx,col_idx,frame_new))
        res4vstack=[]
        for k, g in itertools.groupby(sub_frame_list,lambda x:x[0]):
            # 每相同一行的视频都hstack到一起,加到数组里等待vstack
            one_row = np.hstack([frame_new for (_,_,frame_new) in g])
            # 可能会出现最后一行的width不够col*sub_width，这就需要pad一下宽度（因为是hstack的结果，他们的高度都一样）
            # 比如3x3却只有8个视频，最后一行shape会是(sub_height,sub_width*2,channel)
            h,w,c = one_row.shape
            one_row=np.pad(one_row,((0,0),(0,sub_width*col-w),(0,0)),mode="constant",constant_values=(255,255))
            res4vstack.append(one_row)

        frame = np.vstack(res4vstack)
        # cv2写入视频文件时，要求frame帧大小和定义时完全一样
        # 而这里因为resize用的是取整后的sub_width,sub_height所以需要再对整个帧pad一次
        frame_h,frame_w,frame_c = frame.shape
        frame=np.pad(frame,pad_width=((0,height-frame_h),(0,width-frame_w),(0,0)),mode="constant",constant_values=(255,255))

        out.write(frame)
        pbar.update(1)
        readCap_list = [cap.read() for cap in  videoCap_list]
    out.release()
    _ = [cap.release() for cap in videoCap_list]

    print("使用ffmpeg添加声音（默认使用最长的文件的声音）")
    longest_fp=sorted(zip(fp_list,video_duration_ori),key=lambda x:x[1])[-1][0]
    tmpAcc_fp = "tmp.aac"
    tmp_output_fp = "tmpzac_video_util_output.mp4"
    cmd1 = f"ffmpeg -i {longest_fp} -vn -y -acodec copy {tmpAcc_fp}"
    cmd2 = f"ffmpeg -i {output_fp} -i {tmpAcc_fp} -vcodec copy -acodec copy {tmp_output_fp}"
    cmd3 = f"rm {tmpAcc_fp}"
    cmd4 = f"mv {tmp_output_fp} {output_fp}"
    
    for cmd in [cmd1,cmd2,cmd3,cmd4]:
        print(f">>> exec '{cmd}'")
        status, output = subprocess.getstatusoutput(cmd)
        print(output)
        if status!=0:
            print(">>>[ERROR] failed. output as:")
            break



# PIP:picture in picture | 较短视频从头循环
def merge_PIP2(fp_list,row,col,output_fp=None,pad2longest=False,fps=30,width=854,height=480, auto_size=False):
    """
    [排列]
    v1 v2 v3
    v4 v5
    
    [wxh的信息]
    1080p~480p: 1920x1080, 1280x720, 854x480

    [ffmpeg指令]
    画面裁剪指令
    ffmpeg -i <input> -vf crop=w:h:x:y -threads 5 -preset ultrafast -strict -2 <output>
    音频提取 <output>格式是 .aac
    ffmpeg -i <input> -vn -y -acodec copy <output>
    
    [cv2的一些全局变量]
    1 cv2.CAP_PROP_POS_FRAMES 下一帧的索引（0开始）
    2 cv2.CAP_PROP_POS_AVI_RATIO  进度比例
    3 cv2.CAP_PROP_FRAME_WIDTH  宽度
    4 cv2.CAP_PROP_FRAME_HEIGHT 高度
    5 cv2.CAP_PROP_FPS          帧率fps
    7 cv2.CAP_PROP_FRAME_COUNT  总帧数
    
    [自动获取第一个视频的长宽]
    v1=videoCap_list[0]
    fps = v1.get(cv2.CAP_PROP_FPS)
    width = (int(v1.get(cv2.CAP_PROP_FRAME_WIDTH)))
    height = (int(v1.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    """
    if output_fp is None:
        output_fp = os.path.splitext(fp_list[0])[0]+"_PIP"+os.path.splitext(fp_list[0])[1]
    
    videoCap_list =[cv2.VideoCapture(i) for i in fp_list]
    if auto_size:
        width = int(0.5*col*sum([cap.get(3) for cap in videoCap_list])//len(videoCap_list))
        height = int(0.5*row*sum([cap.get(4) for cap in videoCap_list])//len(videoCap_list))

    video_duration_ori = [cap.get(cv2.CAP_PROP_FRAME_COUNT)//cap.get(cv2.CAP_PROP_FPS) for cap in videoCap_list]
    print(f"原视频时长:")
    _ = [print(f"{fp} : {d}sec") for fp,d in zip(fp_list,video_duration_ori)]
    video_frames = [cap.get(cv2.CAP_PROP_FRAME_COUNT) for cap in videoCap_list]
    total_frame = max(video_frames) if pad2longest else min(video_frames)
    print(f"merge后的视频时长: {total_frame//fps}sec")
    assert col*row >= len(videoCap_list)

    sub_width, sub_height= width//col, height//row
    out = cv2.VideoWriter(output_fp, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))

    # [按帧读取视频]
    # .read 得到的结果是一个tuple2标记是否获取成功 (status, frame)
    pbar = tqdm(total=int(total_frame), desc="processing")
    cur_frame=0
    while cur_frame < total_frame:
        sub_frame_list = [] # 每次清空
        for idx,cap in enumerate(videoCap_list):
            # read
            status,frame = cap.read()
            if status != True:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                status,frame = cap.read()
            # resize
            col_idx = idx % col
            row_idx = idx // col
            frame_new = cv2.resize(frame, (sub_width, sub_height), interpolation=cv2.INTER_CUBIC)
            sub_frame_list.append((row_idx,col_idx,frame_new))
        res4vstack=[]
        for k, g in itertools.groupby(sub_frame_list,lambda x:x[0]):
            # 每相同一行的视频都hstack到一起,加到数组里等待vstack
            one_row = np.hstack([frame_new for (_,_,frame_new) in g])
            # 可能会出现最后一行的width不够col*sub_width，这就需要pad一下宽度（因为是hstack的结果，他们的高度都一样）
            # 比如3x3却只有8个视频，最后一行shape会是(sub_height,sub_width*2,channel)
            h,w,c = one_row.shape
            one_row=np.pad(one_row,((0,0),(0,sub_width*col-w),(0,0)),mode="constant",constant_values=(255,255))
            res4vstack.append(one_row)
        frame = np.vstack(res4vstack)
        # cv2写入视频文件时，要求frame帧大小和定义时完全一样
        # 而这里因为resize用的是取整后的sub_width,sub_height所以需要再对整个帧pad一次
        frame_h,frame_w,frame_c = frame.shape
        frame=np.pad(frame,pad_width=((0,height-frame_h),(0,width-frame_w),(0,0)),mode="constant",constant_values=(255,255))

        out.write(frame)
        pbar.update(1)
        cur_frame += 1
    out.release()
    _ = [cap.release() for cap in videoCap_list]

    print("使用ffmpeg添加声音（默认使用最长的文件的声音）")
    longest_fp=sorted(zip(fp_list,video_duration_ori),key=lambda x:x[1])[-1][0]
    tmpAcc_fp = "tmp.aac"
    tmp_output_fp = "tmpzac_video_util_output.mp4"
    cmd1 = f"ffmpeg -i {longest_fp} -vn -y -acodec copy {tmpAcc_fp}"
    cmd2 = f"ffmpeg -i {output_fp} -i {tmpAcc_fp} -vcodec copy -acodec copy {tmp_output_fp}"
    cmd3 = f"rm {tmpAcc_fp}"
    cmd4 = f"mv {tmp_output_fp} {output_fp}"
    
    for cmd in [cmd1,cmd2,cmd3,cmd4]:
        print(f">>> exec '{cmd}'")
        status, output = subprocess.getstatusoutput(cmd)
        print(output)
        if status!=0:
            print(">>>[ERROR] failed. output as:")
            break

# 根据秒进行视频截取，有不准的现象，整体都偏前了，推荐使用ffmpeg粗剪然后mac自带修剪功能细剪（ffmpeg剪过就带关键帧了，帧内编码）
def cut_bysec(fp,from_sec,to_sec,width=None,height=None,output_fp=None):
    assert " " not in fp
    if output_fp is None:
        output_fp = os.path.splitext(fp)[0]+f"_cut_{from_sec}_{to_sec}"+os.path.splitext(fp)[1]
    cap = cv2.VideoCapture(fp)
    fps = cap.get(cv2.CAP_PROP_FPS) # 不要取整，乘上时间后再取整
    total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT) # 总帧数
    print(f"fps: {fps} frame: {total_frame}")
    if width is None:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    if height is None:
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_fp, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))
    # 支持负数秒，表示倒着来如要最后三秒frome_frame=-3, to_frame=-1
    from_frame = from_sec*fps if from_sec>=0 else total_frame+from_sec*fps
    if to_sec>=0:
        to_frame = to_sec*fps
    elif to_sec==-1:
        # to_sec麻烦一点，如果是-1应该取最后一个索引了
        # 如果直接到最后一帧会报错
        to_frame = total_frame-1
    else:
        to_frame=total_frame+to_sec*fps
    from_frame,to_frame = int(from_frame),int(to_frame)
    assert from_frame <= to_frame, f"时间错误 {from_sec} to {to_sec}"
    print(f"sec:{from_sec}~{to_sec} 索引: {from_frame} ~ {to_frame}")
    pbar = tqdm(total=to_frame - from_frame,leave=False)
    cap.set(cv2.CAP_PROP_POS_FRAMES,from_frame)
    for _ in range(to_frame - from_frame):
        frame = cap.read()[1]
        frame_new = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
        out.write(frame_new)
        pbar.update(1)
    out.release()
    cap.release()

    tmpDir = "./video_util_tmp_res"
    if not os.path.exists(tmpDir):
        os.mkdir(tmpDir)
    # 同样的时间窗口获取音频
    sound = AudioSegment.from_file(fp)
    sound_trimed = sound[from_sec*1000:to_sec*1000]
    tmpAudio_mp3_fp = os.path.join(tmpDir,"trim.mp3")
    sound_trimed.export(tmpAudio_mp3_fp, format="mp3")

    # mp3->m4a
    tmpAudio_m4a_fp = os.path.splitext(tmpAudio_mp3_fp)[0]+'.m4a'
    cmd1 = f"ffmpeg -i {tmpAudio_mp3_fp} -c:a aac -b:a 192k {tmpAudio_m4a_fp}"
    # .mp4与.m4a合并
    tmp_output_fp = os.path.join(tmpDir,"tmp.mp4")
    cmd2 = f"ffmpeg -i {output_fp} -i {tmpAudio_m4a_fp} -vcodec copy -acodec copy {tmp_output_fp}"
    cmd3 = f"mv {tmp_output_fp} {output_fp}"
    cmd4 = f"rm -rf {tmpDir}"
    assert len(cmd4.split(" ")[-1])>3,"保险起见，避免rm -rf删错东西"
    for cmd in [cmd1,cmd2,cmd3,cmd4]:
        print(f">>> exec '{cmd}'")
        status, output = subprocess.getstatusoutput(cmd)
        if status!=0:
            print(">>>[ERROR] failed. output as:")
            print(output)
            break
    return output_fp

# 使用ffmpeg改变码率
def compress(fp,rate=480,w=854,h=480):
    fp_out = os.path.splitext(fp)[0]+"_comp"+os.path.splitext(fp)[1]
    cmd=f"ffmpeg -i {fp} -b:v {rate}k -s {w}x{h} {fp_out}"
    print(f"use cmd: {cmd}\ncompress saved to: {fp_out}")
    status, output = subprocess.getstatusoutput(cmd)
    if status!=0:
        assert False,">>> cmd ERROR: \n"+output
    return fp_out

# 根据秒获取某一帧
def get_frame_bysec(fp,sec):
    cap = cv2.VideoCapture(fp)
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 0
    while True:
        status,frame = cap.read()
        if status==True:
            if count == int(fps*sec):
                return frame
            elif count > int(fps*sec):
                return None
            else:
                pass
        else:
            return None
        count += 1

def play_bysec(fp,from_,to_):
    cap = cv2.VideoCapture(fp)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(1,from_*fps)
    plt.ion()
    for i in range(int(fps*(to_ - from_))):
        plt.cla()
        frame = cap.read()[1]
        frame_new = cv2.resize(frame, (854, 480), interpolation=cv2.INTER_CUBIC)
        plt.imshow(frame_new)
        plt.pause(0.01)
    plt.ioff()
    plt.show()

def concat(fp_list, output_fp=None):
    if output_fp is None:
        output_fp = os.path.splitext(fp_list[0])[0]+"_concat"+os.path.splitext(fp_list[0])[1]
    videoCap_list =[cv2.VideoCapture(i) for i in fp_list]
    width = int(sum([cap.get(3) for cap in videoCap_list])//len(videoCap_list))
    height = int(sum([cap.get(4) for cap in videoCap_list])//len(videoCap_list))
    fps = int(sum([cap.get(5) for cap in videoCap_list])//len(videoCap_list))+1
    out = cv2.VideoWriter(output_fp, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height))

    # [按帧读取视频]
    total_frame = sum([cap.get(7) for cap in videoCap_list])
    pbar = tqdm(total=int(total_frame), desc="processing",leave=False)
    for idx,cap in enumerate(videoCap_list):
        pbar_tmp=tqdm(total=int(cap.get(7)), desc=f"clip_{idx}", leave=False)
        while True:
            pbar.update(1)
            pbar_tmp.update(1)
            status,frame=cap.read()
            if status==True:
                frame_new = cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)
                out.write(frame_new)
            else:
                break
    out.release()
    _ = [cap.release() for cap in videoCap_list]

    tmpDir = "./video_util_tmp_res"
    if not os.path.exists(tmpDir):
        os.mkdir(tmpDir)
    # 同样的时间窗口获取音频
    sound_list=[AudioSegment.from_file(fp) for fp in fp_list]
    sound = functools.reduce(lambda a,b:a+b, sound_list)
    tmpAudio_mp3_fp = os.path.join(tmpDir,"trim.mp3")
    sound.export(tmpAudio_mp3_fp, format="mp3")

    # mp3->m4a
    tmpAudio_m4a_fp = os.path.splitext(tmpAudio_mp3_fp)[0]+'.m4a'
    cmd1 = f"ffmpeg -i {tmpAudio_mp3_fp} -c:a aac -b:a 192k {tmpAudio_m4a_fp}"
    # .mp4与.m4a合并
    tmp_output_fp = os.path.join(tmpDir,"tmp.mp4")
    cmd2 = f"ffmpeg -i {output_fp} -i {tmpAudio_m4a_fp} -vcodec copy -acodec copy {tmp_output_fp}"
    cmd3 = f"mv {tmp_output_fp} {output_fp}"
    cmd4 = f"rm -rf {tmpDir}"
    assert len(cmd4.split(" ")[-1])>3,"保险起见，避免rm -rf删错东西"
    for cmd in [cmd1,cmd2,cmd3,cmd4]:
        print(f">>> exec '{cmd}'")
        status, output = subprocess.getstatusoutput(cmd)
        if status!=0:
            print(">>>[ERROR] failed. output as:")
            print(output)
            break
    return output_fp

def multi_copy(fp,copy=3,output_fp=None):
    if output_fp is None:
        output_fp = os.path.splitext(fp)[0]+"_copy"+os.path.splitext(fp)[1]
    fp_list=[fp]*copy
    if copy in [2,3]:
        merge_PIP2(fp_list,row=1,col=copy,pad2longest=True,auto_size=True)
    elif copy==4:
        merge_PIP2(fp_list,row=2,col=2,pad2longest=True,auto_size=True)
    else:
        assert False,"must less than 4"

# 获取所有的clips并concat到一起
def get_clips(fp,clips,w=854,h=480):
    print(f">>> use size {w}x{h}")
    fp = escape(fp)
    clip_fp_list=[]
    for i in clip:
        begin,end=i.split("-")
        begin = timeparse(begin)
        end = timeparse(end)
        print(begin, end)
        clip_fp_list.append(cut_bysec(fp,begin,end,width=w,height=h))
    print(">>> 将要合并:\n    "+'\n    '.join(clip_fp_list))
    return concat(clip_fp_list)

# 缩放
# ROI裁剪


if __name__ == "__main__":
    # fp_list=[
    # ]
    # concat(fp_list)
    # exit(0)
    # merge_PIP2(fp_list,row=1,col=3,pad2longest=True,auto_size=True)
    # _ = [multi_copy(fp) for fp in fp_list]

    fp=""
    fp=escape(fp)
    w,h=(854,480)
    # w,h=(406,720)
    fp=cut_bysec(fp,0*60,1*60+43.5,width=w,height=h)
    # compress(fp,w=w,h=h)
    exit(0)

    fp=""
    w,h=(406,720)
    w,h=(854,480)
    clip=[]
    fp=get_clips(fp,clip,w=w,h=h)
    compress(fp,w=w,h=h)











