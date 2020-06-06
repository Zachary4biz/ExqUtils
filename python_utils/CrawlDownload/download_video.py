import sys
import os
import time
import requests
import re
from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys 

proxies = {
  "http": "http://85.10.219.100:1080",
  "https": "http://85.10.219.100:1080",
}



def init_driver():
    # 初始化并访问网页
    options = webdriver.ChromeOptions()
    # 关闭图片加载
    options.add_experimental_option('prefs', {'profile.default_content_setting_values': {'images': 2}})
    # options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_page_load_timeout(20)
    driver.set_script_timeout(20) # 这两种设置都进行才有效
    return driver

video_url=""
video_ph=""
def download_video_url(video_url,fp,proxies=None):
    fp = fp.replace(" ","_").replace("\n","_")
    res=requests.get(video_url, stream=True, proxies=proxies, timeout=10)
    if res.status_code==200:
        print("save to "+fp)
        with open(fp,"wb+") as fwb:
            for chunk in tqdm(res.iter_content(chunk_size=1024)):
                if chunk:
                    fwb.write(chunk)
                    fwb.flush()
    else:
        assert False,f"video_url request fail: {res.status_code}\nurl: {video_url}"

def bili(url,driver):
    # https://www.parsevideo.com/bilibili/
    print("[domain]: bili")
    parser_url="https://www.parsevideo.com/bilibili/"
    driver.get(parser_url)
    input_item=driver.find_element_by_id("url_input")
    input_item.send_keys(url)
    btn=driver.find_element_by_id("url_submit_button")
    btn.click()
    time.sleep(1.5)
    download_btn=driver.find_element_by_id("video").find_element_by_xpath(".//span[@class='input-group-btn']/a[contains(@class,'btn btn-primary get-dowmload')]")
    if download_btn is None:
        assert False,"[ERROR] faild to download"
    video_url=download_btn.get_attribute("href")
    video_desc=driver.find_element_by_id("video").find_element_by_xpath(".//p[@class='get-desc']/span[@class='text-danger']").get_attribute("innerText").split(" ")[-1].split("/")[-1]
    download_video_url(video_url,fp=os.path.expanduser("~/Downloads/{}.mp4".format(video_desc)))

@DeprecationWarning
def _youtube1(url,driver):
    # https://www.findyoutube.net/
    print("[domain]: youtube")
    torequest= url.replace("://www.","://www.add")
    driver.get(torequest)
    tr_list=driver.find_elements_by_xpath(".//table[contains(@class,'table table-hover table-condensed/tbody/tr')]")
    tr_list=[tr.find_elements_by_xpath("./td") for tr in tr_list]
    tr_mp4_list=[tr for tr in tr_list if "MP4" in tr[0]]
    tr_target=sorted(tr_mp4_list, key=lambda tr: tr[1], reverse=True)[0]
    video_url = tr_target[2].find_element_by_xpath("./a").get_attribute("href")
    video_desc=driver.find_element_by_xpath(".//div[contains(@class,'container panel panel-default') and @il_cc1='4']")
    video_desc=video_desc.split(" ")[-1].split("/")[-1]
    download_video_url(video_url,fp=os.path.expanduser("~/Downloads/{}.mp4".format(video_desc)))

def compareMP4toWEBM(item0,item1):
    # format0=item0.find_element_by_xpath(".//td[1]")
    # 只关心把mp4放在webm、m4a前面，mp4之间怎么排、其他之间怎么排不重要
    format1=item1.find_element_by_xpath(".//td[2]")
    if format1 == "mp4":
        return 1
    else:
        return -1


def youtube(url,driver,quality_priority=["480p","720p","240p","1080p"]):
    #https://www.savido.net/sites
    parser_url="https://www.savido.net/sites"
    driver.get(parser_url)
    input_item=driver.find_element_by_xpath(".//input[@id='curl']")
    assert input_item is not None, "%s 的网页更新了结构，需要重新获取input元素" % parser_url
    # 输入url并加载
    input_item.clear()
    input_item.send_keys(url)
    driver.find_element_by_xpath(".//button[contains(@class,'btn btn-warning') and @id='downloadButton']").click()
    # 页面中检查可用下载项
    tr_list = driver.find_elements_by_xpath(".//div[@class='table-responsive']//tbody/tr")
    assert tr_list is not None, "%s savido的下载页里元素查找失败" % url
    tr_list = [(tr,tr.get_attribute("innerText").split("\t")[0]) for tr in tr_list if "audio only" not in tr.get_attribute("innerText")]
    if len(tr_list) == 0:
        print("%s 此链接没有视频类的下载项"% url)
        return False
    # 找到每个可用下载项的下载按钮和尺寸（quality）
    # 字典形式为 480p:[item1,item2,item3]，后面依次遍历去找真正可用的下载
    quality_item_dict = {}
    for item,_quality in tr_list:
        b,e=re.search("\\([0-9]+p\\)",_quality).span()
        quality=_quality[b+1:e-1]
        # 如果已有480p则扩充它的list，按MP4格式排在前的顺序，否则新建
        if quality in quality_item_dict:
            exist_item_list = quality_item_dict[quality]
            item_list = exist_item_list + [item]
            item_list = sorted(item_list,key=compareMP4toWEBM)
        else:
            item_list = [item]
        quality_item_dict.update({quality:item_list})
    # 按顺序找下载项
    for q in quality_priority:
        if q in quality_item_dict:
            item_list = quality_item_dict[q]
            for item in item_list:
                # 点击下载按钮后需要手动切换到新的选项卡
                download_a=item.find_element_by_xpath(".//td[3]/a")
                # 1.从url下载 | 
                download_url=download_a.get_attribute("href")
                video_desc=str(int(time.time()))
                download_video_url(download_url,fp=os.path.expanduser("~/Downloads/{}.mp4".format(video_desc))) 
                # 2.点击下载 | 页面有遮罩，直接.click()不生效，需要使用js执行点击
                driver.execute_script("arguments[0].click();", download_a)
                driver.switch_to.window(driver.window_handles[1])
                break
        else:
            continue
    print("%s 的所有可用视频下载，格式都不在 %s" % (url,",".join(quality_priority)))
    return False

def twitter(url,driver):
    # https://twsaver.com/zh/
    print("[domain]: twitter")
    parser_url="https://twsaver.com/zh/twitter.php?url={}"
    driver.get(parser_url.format(url))
    elements=driver.find_elements_by_xpath(".//a[contains(@class,'btn btn-download')]")
    # [e.get_attribute("innerText") for e in elements]
    # elements[0].click()
    video_url=elements[0].get_attribute("href")
    video_desc="".join(elements[0].get_attribute("download").split(" ")[:-1])
    if len(video_desc)<2:
        video_desc=f"twitter_video_{time.time()}"
    download_video_url(video_url,fp=os.path.expanduser("~/Downloads/{}.mp4".format(video_desc)))


url_twt="https://twitter.com/ALCXWW/status/1207518098460266498"
url_bili="https://www.bilibili.com/video/av79929515?from=search&seid=15805744542498691504"
url_ytb=""
url_ph=""

if __name__ == "__main__":
    # url = sys.argv[1]
    url = ""

    driver = init_driver()
    try:
        if "twitter.com" in url:
            twitter(url,driver)
        elif "bilibili.com" in url:
            bili(url,driver)
        elif "youtube.com" in url:
            # assert False, "youtube下载要进外网下"
            youtube(url,driver)
    except Exception as e:
        print(e)
    driver.close()
# driver.close()

