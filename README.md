# LINE-weather-bot

## Useage:
* 輸入縣市名稱時(Ex:臺南市)，會回應該地的天氣狀況

* 貼圖等非文字類的訊息，會回應"講中文啦！"

* 非上述情況者則是會echo使用者輸入的訊息。


## Setup:

### 基本上按照這個部落格的流程就可以完成echobot了
### http://lee-w-blog.logdown.com/posts/1129876-apply-line-messaging-api

### 1.先申請line messaging api

'''
   -可以在line manager上設定一些基礎的回應設定
   -記得要進入settings來開啟message api的服務
'''

### 2.安裝python、django後按照流程設定檔案
	
  * 安裝官方的line bot sdk
'''
  -pip3 install line-bot-sdk   
'''
	* 開啟專案
'''
	-django-admin startproject line_echobot
'''  
	* Create app
'''	
	-python3 manage.py startapp echobot
""    
	* 接下來就是將設定檔以及views.py補齊就行了
	* 注意:將secret key直接打在檔案裡是十分不安全的，可以將其設定為heroku的環境變數來保護它

### 3.申請heroku帳號，並將secret key設定在其上，開始部屬
'''
	-heroku login
	-heroku git:remote -a YOUR_APP
	-git add --all
	-git commit -m "your commit"
	-git push heroku master
'''	
	* 完成後你的domain 會是 https://YOUR_APP.herokuapp.com/
	* 如果成功部屬並可以運行成功，你的 domain應該會是空白的，反之則有error message
	* 因此你要在line上設定的webhook url就是 https://YOUR_APP.herokuapp.com/echobot/callback/
		

### 4.echobot成功後就開始改成weatherbot

	* 使用bs4來爬取台灣36小時天氣的資料
	* 將views.py裡的echo code進行修改，使其能夠回傳爬取所獲得的天氣
