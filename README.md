# EvernoteDup

## 简介
将印象笔记账户中的笔记复制到evernote账户中<br>
如果需要将evernote账户中的笔记转移到印象笔记账户中或在印象笔记账户之间转移请使用[NoteDup](https://appcenter.yinxiang.com/app/notedup/windows/)

## 使用方法
1. 安装python2.7
2. 安装evernote sdk `pip install evernote`
3. 获取两个账户的token
    获取方法
    * 生成开发者token<br>
        **需要向客服申请权限**
        * [印象笔记账户token获取](https://app.yinxiang.com/api/DeveloperToken.action)
        * [evernote账户token获取](https://www.evernote.com/api/DeveloperToken.action)
    * 从浏览器中获取
        1. 登陆网页版
            * [印象笔记网页版](https://app.yinxiang.com/Login.action)
            * [evernote网页版](https://www.evernote.com/Home.action?login=true)
        2. 打开浏览器开发者模式后刷新主页
        ![](https://user-images.githubusercontent.com/37578699/41496568-3d339d44-7175-11e8-8efc-15ea0a88b299.png)
        将图中auth后的内容分别保存
4. 将获得的token填写在相应的位置
![](https://user-images.githubusercontent.com/37578699/41496560-1428703c-7175-11e8-8121-798169fa4fe7.png)
5. 运行程序<br>
![](https://user-images.githubusercontent.com/37578699/41496563-1a89311e-7175-11e8-880c-10ef3b3d2e97.png)

## 效果
* 可以复制笔记本的名称，对应的笔记本组，**不能**复制笔记本的分享等属性
* 可以复制笔记的所有内容，包括附件和标签到对应名称的笔记本
* 可以复制所有标签和其上下级关系

## 参考
* [印象笔记API使用_豆瓣](https://www.douban.com/note/578622628/)
* [使用Python操作Evernote API_简书](https://www.jianshu.com/p/bda26798f3b3)
* [印象笔记开发者文档](https://dev.yinxiang.com/doc/)
* [sdk-python-demo](https://github.com/evernote/evernote-sdk-python/blob/master/sample/client/EDAMTest.py)
