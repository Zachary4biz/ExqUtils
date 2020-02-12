import sys
import os
import time
import requests
from tqdm.auto import tqdm
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def download_google_pic(driver,target,hold_cnt,max_load_cnt=None,all_use_screenshot=False,save_dir=None):
    if max_load_cnt is None:
        max_load_cnt=hold_cnt//100 +3
        print(f"use max_load_cnt as {max_load_cnt}")
    if save_dir is None:
        save_dir="/Users/zac/Downloads/tmp"
    target_asfp=target.replace(' ','_')
    save_dir=os.path.join(save_dir,target_asfp)
    os.makedirs(save_dir,exist_ok=True)
    print(f"download to {save_dir}")
    driver.get("https://www.google.com/imghp")
    inp=driver.find_element_by_xpath(".//input[@name='q' and @type='text']")
    inp.send_keys(target)
    inp.send_keys(Keys.ENTER)

    # google pic是每次下滑到底部会加载100张图
    # 加载到400张图后需要点击「显示更多搜索结果」的button （在此之前xpath可以找到这个item但是不可交互）
    # 点击一次显示更多后，btn又变为不可点击，需要下滑加载
    print("开始加载图片")
    load_cnt=0
    while len(driver.find_elements_by_xpath('.//img'))<hold_cnt and load_cnt<max_load_cnt:
        load_cnt += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)
        print(f"scroll to bottom, current image-cnt: {len(driver.find_elements_by_xpath('.//img'))}")
        if driver.find_element_by_xpath(".//input[@type='button']").is_displayed():
            try:
                driver.find_element_by_xpath(".//input[@type='button']").click()
                time.sleep(1.5)
                print(f"click load-more, current image-cnt: {len(driver.find_elements_by_xpath('.//img'))}")
            except:
                print("click fail")
                pass

    print("开始保存图片")
    for idx,el in tqdm(enumerate(driver.find_elements_by_xpath('.//img'))):
        save_fp=os.path.join(save_dir,f"{target.replace(' ','_')}_{idx}.jpg")
        if all_use_screenshot:
            el.screenshot(save_fp)
            continue
        url=el.get_attribute("data-iurl")
        if url is None or len(url)<1:
            url=el.get_attribute("src")
        if url is not None:
            try:
                res = requests.get(url, timeout=10)
                if res.status_code==200:
                    with open(save_fp,"wb+") as fwb:
                        fwb.write(res.content)
            except Exception as e:
                # el.screenshot(save_fp)
                # screenshot存下来的有不少都是全白色的，有时候还会因为元素width/height为0报错
                pass
                print(f"[ERROR] at [{idx}] {url}: {repr(e)}")
        else:
            # el.screenshot(save_fp)
            # screenshot存下来的有不少都是全白色的，有时候还会因为元素width/height为0报错
            pass

if __name__ == "__main__":
    # 初始化并访问网页
    options = webdriver.ChromeOptions()
    # options.add_experimental_option('prefs', {'profile.default_content_setting_values': {'images': 2}})
    options.add_argument('headless')
    driver = webdriver.Chrome(chrome_options=options)

    target="porn pic"
    hold_cnt=600
    # download_google_pic(driver,target,hold_cnt)
    t0=['blowjob','pussy close porn','dick close porn','breast close porn']
    t1=["porn pic","indian porn","brunette porn",'indian nude selfie','indian nude girl','naked guy porn','indian naked guy']
    t2=['woman bodybuilder','lady photo pose','indian guy full body','indian people','selfie','couple','indian love']
    t3=['indian models','male bodybuilder','indian celebrity','normal guys']
    t4=['vagina closeup']
    for t in t4:
        print("\n"*2+"*"*10+t+"*"*10+"\n"*2)
        download_google_pic(driver,t,hold_cnt=300)
    # download_google_pic(driver,'naked statue',hold_cnt=500)
    driver.close()

