import os
import argparse

def convert_videos(video_paths):
    converted_videos = []
    for i, video in enumerate(video_paths):
        converted_video = f"converted_{i}.mp4"
        os.system(
            f"ffmpeg -y -i {video} -vf \"scale=512:512,fps=10,setpts=0.9*PTS\" "
            f"-r 10 -t 7.2 -vsync cfr -c:v libx264 -preset veryfast -crf 23 -an {converted_video}"
        )
        converted_videos.append(converted_video)
    return converted_videos

def merge_videos(video_list, output_path):
    inputs = " ".join([f"-i {video}" for video in video_list])
    filter_complex = """
        [0:v][1:v][2:v]hstack=inputs=3[top];
        [3:v][4:v][5:v]hstack=inputs=3[bottom];
        [top][bottom]vstack=inputs=2[v]
    """.replace("\n", "")
    
    merge_command = f"ffmpeg -y {inputs} -filter_complex \"{filter_complex}\" -map \"[v]\" -c:v libx264 -b:v 1M -r 10 {output_path}"
    os.system(merge_command)

def main():
    parser = argparse.ArgumentParser(description='合并六个视频为 2 行 3 列')
    parser.add_argument('--name1', type=str, help='第一个视频名称前缀')
    parser.add_argument('--name2', type=str, help='第二个视频名称前缀')
    args = parser.parse_args()
    
    video_paths = [
        f"{args.name1}.mp4", f"{args.name2}.mp4", f"{args.name2}_3.mp4",
        f"{args.name2}_tailor3d.mp4", f"{args.name2}_MVEdit.mp4", f"{args.name2}_3DAdapter.mp4"
    ]
    
    converted_videos = convert_videos(video_paths)
    output_video_path = f"{args.name2}_combine.mp4"
    merge_videos(converted_videos, output_video_path)
    
    for video in converted_videos:
        os.remove(video)
    
    print(f"视频已保存到 {output_video_path}")

if __name__ == "__main__":
    main()

