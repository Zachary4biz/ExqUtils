import sys
import os
import time
import requests
from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys 
# 初始化并访问网页
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {'profile.default_content_setting_values': {'images': 2}})
# options.add_argument('headless')
driver = webdriver.Chrome(chrome_options=options)

def download_video_url(video_url,fp):
    fp = fp.replace(" ","_").replace("\n","_")
    res=requests.get(video_url, stream=True)
    if res.status_code==200:
        print("save to "+fp)
        with open(fp,"wb+") as fwb:
            for chunk in tqdm(res.iter_content(chunk_size=1024)):
                if chunk:
                    fwb.write(chunk)
                    fwb.flush()
    else:
        assert False,f"video_url request fail: {res.status_code}\nurl: {video_url}"

def bili(url):
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

def youtube1(url):
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

def youtube(url):
    #https://www.savido.net/sites
    parser_url="https://www.findyoutube.net/"
    driver.get(parser_url)
    input_item=driver.find_element_by_xpath(".//input[@id='url']")
    input_item.clear()
    input_item.send_keys(url)
    driver.find_element_by_xpath(".//input[contains(@class,'btn btn-default') and @type='submit' and @name='submit']").click()

def twitter(url):
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
# url_ytb="https://www.youtube.com/watch?v=KoSo-fEzo1g"
# twitter(url_twt)

if __name__ == "__main__":
    url = sys.argv[1]
    if "twitter.com" in url:
        twitter(url)
    elif "bilibili.com" in url:
        bili(url)
    elif "youtube.com" in url:
        assert False, "youtube下载要进外网下"
        youtube(url)
    driver.close()
# driver.close()

