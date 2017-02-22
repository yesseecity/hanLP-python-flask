# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* 從 Dockerfile

  - 建立環境的image檔

    >```
    $ sudo docker build -t hanlp ./
    ```
    
    指令說明:

    1. `sudo` 指令在 mac 系統中不需要

    2. `-t hanlp` 作用為指定 image 的 tag 為 hanlp 版本為 latset，如需指定版本 可用 `-t hanlp:1.2.3`

    3. `./` 是指 Dockerfile 所在的資料夾  
  
  + 執行 docker image 並建立 container，並透過 volume 進行檔案的傳遞
   >```$ sudo run -it --name=hanlp-container -v ~/myProject:/root/localhome -p 0.0.0.0:5001:5001 hanlp /bin/bash```

    指令說明:

    1. `--name` 是指container name

    2. `-v ~/myProject:/root/localhome`   
  是把本地端 `~/myProject` 連結到 container 內的 `/root/localhome`

    3. `-p 0.0.0.0:5001:5001`
  把本地端的5001 port 映射到 container 的 5001 port

    4. 備註:如果建立 image 時，有指定版本可將 ``hanlp /bin/bash`` 換成 ``hanlp:1.2.3 /bin/bash``

  + git clone 本專案
  
  + 下載 hanLP 的 [data檔](https://drive.google.com/open?id=0B3fyfPWHm1TcYVZfaXR0MjNPZU0) 並解壓到本專案的`server/lib/hanlp-1.3.2/`

  + 未完...



* 

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact