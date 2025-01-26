import os

# 视频路径列表
name1 = "mechine"
name2="mechine_pizza"
video_paths = [name1+".mp4", name2+".mp4", name2+"_3.mp4", name2+"_tailor3d.mp4"]

# 转码后的视频路径
converted_videos = []
for i, video in enumerate(video_paths):
    converted_video = f"converted_{i}.mp4"
    os.system(f"ffmpeg -y -i {video} -vf scale=512:512 -r 10 -c:v libx264 -preset veryfast -crf 23 -an {converted_video}")
    converted_videos.append(converted_video)

# 水平拼接视频
output_video_path = name2+"_combine.mp4"
concat_command = (
    f"ffmpeg -y " + \
    " ".join([f"-i {video}" for video in converted_videos]) + \
    f" -filter_complex \"hstack=inputs={len(converted_videos)}\" " + \
    f"-c:v libx264 -b:v 1M -r 10 {output_video_path}"
)

os.system(concat_command)

# 清理临时文件
for video in converted_videos:
    os.remove(video)

print(f"视频已保存到 {output_video_path}")
