# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* hanLP為 [hankcs](https://github.com/hankcs/HanLP) 所開發的中文NLP，這邊用python改寫成 api server 

* Version: 0.3.0


### How do I get set up? ###

* Git clone this hanlp-python

* 從 Dockerfile

  + 進入hanlp並建立環境的image檔
    
    >```
    $ cd hanlp-python
    ```

    >```
    $ sudo docker build -t hanlp:0.3.0 ./
    ```
    
    備註:

    1. `sudo` 指令在 mac 系統中不需要

    2. `./` 是指 Dockerfile 所在的資料夾，也就是本專案的根目錄 
  
  + 下載 hanLP 的 [data檔](https://drive.google.com/open?id=0B3fyfPWHm1TcYVZfaXR0MjNPZU0) 並解壓到本專案的`server/lib/hanlp-1.3.2/` 之後裡面會多一個 ``data``的資料夾

  + 執行 docker image 並建立 container，並透過 volume 進行檔案的傳遞
    
    >```
    $ sudo docker run -it --name=hanlp030 -v ~/hanLP-python:/hanlp -p 0.0.0.0:80:5001 hanlp:0.3.0 /bin/bash
    ```

    指令說明:

    1. `--name` 是指container name

    2. `-v ~/hanLP-python:/hanlp`   
    是把本地端 ``~/hanLP-python`` 連結到 container 內的 ``/hanlp``

    3. `-p 0.0.0.0:80:5001`
    把本地端的 80 port 映射到 docker container 的 5001 port

  + 透過python執行``python ./server/hanlp-server.py``