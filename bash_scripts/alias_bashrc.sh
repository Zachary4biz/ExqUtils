# hadoop+yarn
alias hdfsl="hdfs dfs -ls -h"
alias hdfsc="hdfs dfs -cat"
alias hdfslt="hdfs dfs -ls -t -h"
alias hdfsdh="hdfs dfs -du -h"
alias hdfsls="hdfs dfs -ls"
alias hdfsrm="hdfs dfs -rm -r"
alias hdfsdhs="hdfs dfs -du -h -s"
alias hdfscp="hdfs dfs -cp"
alias hdfsmv="hdfs dfs -mv"
alias yarns="yarn application -list | grep "
alias yarnk="yarn application -kill "

# generic
alias vib="vim ~/.bashrc"
alias sourceb="source ~/.bashrc"
alias lt="ll -th"
alias lth="ll -th | head"
alias search="ps -ef| grep"
alias getip="ifconfig | grep -Eo 'inet [0-9\.]+' | grep -v 127.0.0.1 | grep -Eo '[0-9\.]+'" # 实体机如mac下会有多个网口（wifi和usb网线）
alias current_time="date +%Y-%m-%d_%H:%M:%S"
alias getpid="awk '{print \$2}'"  # 这里用\$是因为alias里必须转义
# tensorboard2.0 没有--bind_all不能用ip访问只能用localhost访问
alias tel="tensorboard --bind_all --logdir ./"
alias workon="conda activate"
alias now='date "+%Y-%m-%d %H:%M:%S"'
alias today="date +%Y-%m-%d"


#########
# ffmpeg
#########
alias ffmpeg_crop="echo 'ffmpeg -i <input> -vf crop=w:h:x:y -threads 5 -preset ultrafast -strict -2 crop.mp4'"
alias ffmpeg_cut="echo 'ffmpeg -ss 00:00:00 -t 00:00:30 -i <input> -vcodec copy -acodec copy cut.mp4'"
alias ffmpeg_concat="echo 'ffmpeg -f concat -i list.txt -c copy concat.mp4'"
alias ffmpeg_scale="echo 'ffmpeg -i <input> -vf scale=320:240 <output>'"
alias ffmpeg_comp="echo 'ffmpeg -i <input> -b:v 500k -s 854x480 <output>'"
alias video_crop=ffmpeg_crop
alias video_cut=ffmpeg_cut
alias video_concat=ffmpeg_concat
alias video_scale=ffmpeg_scale
alias video_comp=ffmpeg_comp

# 视频下载
alias pdv="python ~/ExqUtils/CrawlDownload/download_video.py"

# otehrs
alias grepid="grep -Eo '\"id\":[0-9]{16}'"
alias grepalgoprofile="grep -Eo '\"algo_profile\".+\"status\"\:\"\w+\"}'"

# init git lg
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"

tfhub="/var/folders/zy/690m3fw13ylfsgp2zdly27km0000gn/T/tfhub_modules/"


########################
# rm替换为移动到Trash目录
# 不要做这种培养坏习惯的事
# 不要不加提示地修改默认指令
########################
alias rm="echo 'maybe rmtrash? (or stick to /bin/rm)'"

# 坚果云目录
nut="/Users/zac/Nutstore_Files/我的坚果云/"