#### 破解淘宝sign加密算法实现爬虫

##### 破解大致流程



1. 查找实际请求地址提交参数，确定固定参数与可变参数

2. 发现可变参数中主要为sign的规律难寻找，通过sign值格式可以基本确定是经过MD5编码

3. 逐个查看所有请求过的js，发现包含sign算法的js
4. 通过设置断点查看sign生成过程

4. 实际是通过token、时间戳、appkey、data四个值组合并MD5编码	

5. token通过js从cookies中得来，按照约定的算法生成sign，sign在mtop的请求中带

6. mtop通过cookie中和token用同样的方式计算出sign，与请求的sign进行比较

7. 检查通过将返回api的应答，失败提示“FAIL_SYS_ILLEGAL_ACCESS:: 非法请求”

8. token有时效性，遇到失效返回json提示”令牌过期“，同时会写入新的token
9. 关于cookie中的token的自我检查，由于token在cookie中是明文的，可能会被仿冒，在输出的cookie中包含一个用非对称密钥的公钥加密后的token, MTOP在每次请求时会先检查cookie中的token是否是由服务端分配出去的（利用加密后的token和私钥还原token，与回传的明文token比较）
10. 对于token时效性可以通过另起程序如selenium在过期时重新获取cookies，爬虫只需去读取前者写入的文件

​	

- 请求地址

  https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/

  - 例：

    https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?jsv=2.4.5&appKey=12574478&t=1551347276166&sign=a6cda8e79f0b3668e2d0c0a600232859&api=mtop.relationrecommend.WirelessRecommend.recommend&v=2.0&preventFallback=true&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22appId%22%3A%223113%22%2C%22params%22%3A%22%7B%5C%22catmap_version%5C%22%3A%5C%223.0%5C%22%2C%5C%22tab%5C%22%3A%5C%22on%5C%22%2C%5C%22industry%5C%22%3A%5C%22%5C%22%7D%22%7D

    

- GET可变参数t、sign

```python
t:
1551347149021 
1551347163894
sign:
f434528deac7395a08033bae013a8f67
607f5e7ab24d8c55c027bc3cb06a25bd
```



- 获取值流程：

  - _m_h5_tk：从第一次登陆或访问时获取cookies中的token：

    ```python
    4404d7771729c4e66323479b4d0ef0f4_1551356782807
    ```

    token就为4404d7771729c4e66323479b4d0ef0f4

  - t：为时间戳*1000即：`int(time.time()\*1000)`

  - appkey：一般是固定值

  - data：一般是提交的参数

  - *sign：通过md5将以上数值加密生成*

    ```javascript
    md5Hex(token&t&appKey&data) # js
    ```

    ```python
    import hashlib
    hashlib.md5(b'123').hexdigest() # python
    ```

