Chrome driver main downloads page https://googlechromelabs.github.io/chrome-for-testing/#stable


```
brew install wget
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.62/mac-arm64/chromedriver-mac-arm64.zip \
  && unzip chromedriver-mac-arm64.zip
wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/117.0.5938.62/mac-arm64/chrome-mac-arm64.zip \
  && unzip chrome-mac-arm64.zip
pip install -r requirements.txt
python qualio_bot.py
```


1. For macOS arm64 stable chromedriver: 


2. For macOS arm64 stable test chrome: 


Extract the two above in the root dir and then run the bot. 
