# 输出日志里的id，转换前10位为时间
# tail consume_news_profile_append.out| grepid | grep -Eo "[0-9]{10}" | awk '{print($0,":",strftime("%F %T", $0))}'
topic=$1
if [ ! -n "$1" ]; then
echo "Usage:\t$0 <topic>"
echo "topic信息:"
echo "新闻输入数据 test.rec.news-data"
echo "新闻画像数据 test.rec.news-profile"
echo "视频输入数据 test.rec.video-data"
echo "视频画像数据 test.rec.video-profile"
#topic="rec.news-data-16partition"
fi

echo "监听${topic}"

kafka-console-consumer \
--property print.timestamp=true \
--property print.offsets=true \
--bootstrap-server test-kafka.apuscn.com:9092,test-kafka.apuscn.com:9093,test-kafka.apuscn.com:9094 \
--topic $topic
