#作者：王屿轩 Eason Wang
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time
import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import os
import shutil
from PIL import Image
import pytesseract
import winsound
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import tkinter as tk
from tkinter import ttk
import threading


devices = AudioUtilities.GetSpeakers()
sport_place_list=["https://sports.sjtu.edu.cn/pc/#/apointmentDetails/1/9096787a-bc53-430a-9405-57dc46bc9e83/%25E5%2585%25A8%25E9%2583%25A8","https://sports.sjtu.edu.cn/pc/#/apointmentDetails/1/3b10ff47-7e83-4c21-816c-5edc257168c1/%25E7%25BE%25BD%25E6%25AF%259B%25E7%2590%2583"]


def selenium_function(sport_name,sport_place,days_after,start_time,end_time):
    #设置jaccount的用户名和密码
    jaccountid="xxx"
    jaccountpwd="xxx"
    #系统相关参数
    zoom=1.25
    #设置Chrome参数
    hide_browser=False

    
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    vl = volume.GetMasterVolumeLevel()


    options = Options()
    if hide_browser:
        options.add_argument('headless')  #不显示浏览器
        zoom=1
    browser = webdriver.Chrome(executable_path ='./chromedriver.exe',options=options)

    print(browser.title)




    browser.set_page_load_timeout(100)
    url = sport_place
    browser.get(url)
    while True:
        try:
            browser.get(url)
        except TimeoutException:
            print('Timeout')
            browser.execute_script('window.stop()')
            continue
        time.sleep(2)
        break

    while True:
        time.sleep(2)
        gotologin_button=browser.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div[2]/div[2]/button")
        gotologin_button.click()
        time.sleep(2)
        jaccountid_input=browser.find_element_by_xpath("//*[@id='user']")
        jaccountid_input.send_keys(jaccountid)

        time.sleep(0.1)
        jaccountpwd_input=browser.find_element_by_xpath("//*[@id='pass']")
        jaccountpwd_input.send_keys(jaccountpwd)

        time.sleep(0.1)
        captcha_img=browser.find_element_by_xpath("//*[@id='captcha-img']")
        browser.save_screenshot('./tmpscreen.png')
        captcha_left = captcha_img.location['x']
        captcha_top = captcha_img.location['y']
        captcha_right = captcha_img.location['x'] + captcha_img.size['width']
        captcha_bottom = captcha_img.location['y'] + captcha_img.size['height']
        captcha_picture = Image.open('./tmpscreen.png')
        captcha_picture = captcha_picture.crop((captcha_left*zoom, captcha_top*zoom, captcha_right*zoom, captcha_bottom*zoom))
        captcha_picture.save('./tmpcaptcha.png')
        captcha_string = pytesseract.image_to_string(Image.open('./tmpcaptcha.png'))
        #print(captcha_string)
        os.remove('./tmpscreen.png')
        os.remove('./tmpcaptcha.png')
        captcha_input=browser.find_element_by_xpath("//*[@id='captcha']")
        captcha_input.send_keys(captcha_string.strip())

        time.sleep(2)
        login_button=browser.find_element_by_xpath("//*[@id='submit-button']")
        try:
            login_button.click()
        except:
            print("初始化完成！")
        else:
            print("初始化完成！")
        failcount=0
        
        time.sleep(3)
        while True:
            try:
                browser.get(url)
            except TimeoutException:
                print('Timeout')
                browser.execute_script('window.stop()')
                continue
            time.sleep(2)
            break
        while True:
            try:
                time.sleep(1)
                browser.refresh()    
                time.sleep(2)
                sport_list=browser.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[1]/div[1]/div/div/div")
                sport_blocks=sport_list.find_elements(By.XPATH, "./div")[1:]
                for sport_block in sport_blocks:
                    if sport_block.text==sport_name:
                        sport_block.click()
                
                date_list=browser.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[2]/div[1]/div[2]/div[1]/div/div/div")
                date_wanted=date_list.find_elements(By.XPATH, "./div")[days_after+1]
                date_wanted.click()

                time.sleep(2)
                time_list=browser.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/div[1]")
                time_wanted_list=time_list.find_elements(By.XPATH, "./div")[start_time-7:end_time-7]
                #print(len(time_wanted_list))
                found=False
                for time_wanted in time_wanted_list:
                    targets_all=time_wanted.find_elements(By.XPATH, "./div")
                    #print(len(targets_all))
                    for target_all in targets_all:
                        target_picsrc=target_all.find_element_by_xpath("./div/div/img").get_attribute("src")
                        if target_picsrc!="https://api.sjtu.edu.cn/v1/file/1a04b1ee-6dd7-4a2b-9fe8-1d6e6206aa09":
                            target=target_all.find_element_by_xpath("./div/div")
                            target.click()
                            found=True
                            break
                    if found:
                        break
                if found:
                    time.sleep(0.1)
                    confirm_button=browser.find_element_by_xpath("/html/body/div/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[3]/button")
                    confirm_button.click()
                    time.sleep(0.5)
                    read_checkbox=browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div[1]/label/span[1]")
                    read_checkbox.click()
                    time.sleep(0.3)
                    gotopay_button=browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div[2]/button[2]")
                    gotopay_button.click()
                    print("成功！")
                    volume.SetMute(0, None)
                    volume.SetMasterVolumeLevel(0.0, None)
                    winsound.Beep(1500, 5000)
                    volume.SetMasterVolumeLevel(vl, None)
                    volume.SetMute(1, None)
                    time.sleep(900)
                else:
                    failcount+=1
                    print("\r已抢"+str(failcount)+"次",end="",flush=True)
                    time.sleep(1)
            except:
                continue
        time.sleep(9999)

def button_click():
    sport_name = option_var1.get()
    print(sport_name)
    selected_option_place = option_var2.get()
    sport_place=sport_place_list[option_menu2['menu'].index(selected_option_place)]
    print(sport_place)
    days_after=int(option_var3.get())
    print(days_after)
    start_time=int(option_var4.get())
    print(start_time)
    end_time=int(option_var5.get())
    print(end_time)
    thread =threading.Thread(target=selenium_function,args=(sport_name,sport_place,days_after,start_time,end_time))
    thread.start()
root = tk.Tk()
root.title("图形界面示例")

# 创建文本框
text_entry = tk.Text(root, height=10, width=30)
text_entry.pack()

# 创建下拉菜单
option_var1 = tk.StringVar()
option_choices1 = ["羽毛球"]
option_menu1 = ttk.OptionMenu(root, option_var1, option_choices1[0], *option_choices1)
option_menu1.pack()
# 创建下拉菜单
option_var2 = tk.StringVar()
option_choices2 = ["霍英东", "气膜"]
option_menu2 = ttk.OptionMenu(root, option_var2, option_choices2[0], *option_choices2)
option_menu2.pack()
# 创建下拉菜单
option_var3 = tk.StringVar()
option_choices3 = [str(i) for i in range(8)]
option_menu3 = ttk.OptionMenu(root, option_var3, option_choices3[0], *option_choices3)
option_menu3.pack()
# 创建下拉菜单
option_var4 = tk.StringVar()
option_choices4 = [str(i) for i in range(7,22)]
option_menu4 = ttk.OptionMenu(root, option_var4, option_choices4[0], *option_choices4)
option_menu4.pack()
# 创建下拉菜单
option_var5 = tk.StringVar()
option_choices5 = [str(i) for i in range(8,23)]
option_menu5 = ttk.OptionMenu(root, option_var5, option_choices5[0], *option_choices5)
option_menu5.pack()
# 创建按钮
button = ttk.Button(root, text="开始", command=button_click)
button.pack()

root.mainloop()