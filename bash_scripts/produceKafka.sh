
#################
# 自测试用的topic
#topic="test.rec"
#######################
# 云服务联调使用的topic 新闻数据
#topic="test.rec.news-data"
######################
# 云服务联调的 video 数据
#topic="test.rec.video-data"

dataType=$1

if [ ! -n "$dataType" ]; then
	echo "未传入dataType，默认为新闻数据测试流程"
	topic="test.rec.news-data"
	file="sampleJSONData_news.json"
elif [ $dataType = "news" ]; then
	echo "传入news，新闻流程"
	topic="test.rec.news-data"
	file="sampleJSONData_news.json"
elif [ $dataType = "video" ]; then
	echo "传入video,视频流程"
	topic="test.rec.video-data"
	file="sampleJSONData_video.json"
elif [ $dataType = "video_update" ]; then
	echo "传入video_update,视频更新数据"
	topic="rec.video-update-data"
	file="sampleJSONData_video_update.json"
elif [ $dataType = "news_update" ]; then
        echo "传入news_update,视频更新数据"
        topic="rec.news-update-data"
        file="sampleJSONData_news_update.json"
elif [ $dataType = "words" ]; then
	echo "sensitive words .. "
	topic="rec.news.config"
	file="sampleJSONData_sensitiveWords.json"
elif [ $dataType = "cut" ]; then
	echo "cutcut"
	topic="rec.image-data"
	file="sampleJSONData_cutcut.json.big"
fi

echo "produce [file] '${file}' to [topic] ${topic}"
kafka-console-producer \
	--broker-list eekafka004.eq-sg-2.apus.com:9092,eekafka005.eq-sg-2.apus.com:9092,eekafka006.eq-sg-2.apus.com:9092 \
	--topic $topic < $file
    