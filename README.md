# sjtu_sports_JLW 上海交大运动场馆捡漏王 
## 当前战果数量（开发者本人）：  
<img src="https://github.com/ghost-in-a-shell/sjtu_sports_JLW/assets/61978045/a0acc074-f057-4891-9945-a61deca0b41e"  align="middle" width = "150" height = "150"/>  
2024/03/09 19:00-20:00 霍英东羽毛球  
  
## 运行工具需要：  
Selenium  （驱动Chrome Driver）  
Chrome Browser (最新版本即可)  
Chromedriver (https://chromedriver.chromium.org/  要与Chrome版本对应，下载后与py文件放同一个文件夹)  
pytesseract (用于验证码识别)  
pycaw (用于系统声音调节)  

## 个性化设置与登录：  
![image](https://github.com/ghost-in-a-shell/sjtu_sports_JLW/assets/61978045/6586a7ef-16a2-4044-94e8-30c7b72ec37b)  
jaccount的用户名密码  
系统显示比例  
是否隐藏浏览器（建议设置False）  
要抢的运动（目前只支持羽毛球气膜馆）  
几天后 (支持0-7)  
开始结束时间 （目标时间段）  

## 如何适配更多运动和更多场馆：  
![image](https://github.com/ghost-in-a-shell/sjtu_sports_JLW/assets/61978045/dcf1d235-d92c-483f-bddf-d1dff97d543a)  
更改此处的url为目标场馆网址，例如霍英东：    
![image](https://github.com/ghost-in-a-shell/sjtu_sports_JLW/assets/61978045/b390e574-bcea-48c9-8ea1-bb644b524efc)  


  运动种类，更改此处的src：  
  ![image](https://github.com/ghost-in-a-shell/sjtu_sports_JLW/assets/61978045/a1618c52-d348-4779-bdf0-f89ddb2bd5f3)  
  获取src方式，f12查看网页html，找到对应的蓝色图片的src替换代码中的src，也可以用灰色图片的src替换同时前面的"=="换为"!="：  
  ![image](https://github.com/ghost-in-a-shell/sjtu_sports_JLW/assets/61978045/f853efd1-d73b-42e2-9d37-65b2e09f9503)  
## 下一版本功能：
### 丰富功能  
支持自选运动场馆  
支持自选运动种类 
其他细节优化  
### 运行鲁棒性  
登录的容错实现  
网络波动时等待
  
## 长期目标  
UI版本开发  
多样化提示功能  
自动化付款  
刷新频率等参数的详细配置  
适配mac系统
