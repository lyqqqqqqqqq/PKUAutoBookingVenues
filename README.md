# PKUAutoBookingVenues
PKU智慧场馆自动预约工具

部分代码和这个README引用自大佬的自动报备项目 https://github.com/Bruuuuuuce/PKUAutoSubmit

感谢同学们的支持，祝大家一切顺利，学业有成！
## 注意这是会自动付款的！！！付款方式是校园卡，所以如果只是试一试的话，要记得手动取消预约退款！！！
## 如果校园卡余额不足也是会预约失败的

是我的第一个 `selenium` 练手小项目，完善程度较低，欢迎任意类型的使用与开发改进

## 说明

- 本工具采用 Python3 搭配 `selenium` 完成自动化操作，实现全自动预约场馆
- 支持基于[Server酱](https://sct.ftqq.com/)的备案结果微信推送功能，体验更佳
- 采用定时任务可实现定期（如每周）免打扰预约
- 第三方依赖包几乎只有 `selenium` 一个
- 由于我只测试过羽毛球场的预约，其他场馆只是理论上可行，如果出现任何问题，可以提issue
- 目前不支持多人多项目，以后可能会更新
- 支持时间上的“或”选项，支持按照星期几设定时间
- 定时任务还未经过完全测试
- 部分代码和这个README引用自大佬的自动出入校报备项目 https://github.com/Bruuuuuuce/PKUAutoSubmit
- 注意这是会自动付款的！！！付款方式是校园卡，所以如果只是试一试的话，要记得手动取消预约退款！！！
- 如果校园卡余额不足也是会预约失败的


## 安装与需求

### Python 3

本项目需要 Python 3，可以从[Python 官网](https://www.python.org/)下载安装

### Packages

#### selenium

采用如下命令安装 `selenium`，支持 2.48.0 及以上版本：

```python
pip3 install selenium==2.48.0
```

## 基本用法

1. 将 `config.sample.ini` 文件重命名为 `config.ini` ，请不要新建文件，不然自己搞定编码问题

2. 用文本编辑器（建议代码编辑器）打开 `config.ini` 文件

3. 配置 `[login]` 、`[type]` 、`[time]`、`[wechat_notice]` 这几个 Section 下的变量，在 `config.ini` 文件内有详细注释


## 定时运行

### Windows

本项目中的 `autoRun.bat` 文件可提供在静默免打扰情况下运行程序的选择，配合 Windows 任务计划管理可实现定期自动填报，具体请参考[Win10下定时启动程序或脚本](https://blog.csdn.net/xielifu/article/details/81016220)

### mac OS

进入项目根目录，以命令 `./macAutoRun.sh` 执行 `macAutoRun.sh` 脚本即可，可设定或取消定时运行

### Linux

使用 `crontab` 设置

**Note:** 静默运行的弊端为无法看到任何报错信息，若程序运行有错误，使用者很难得知。故建议采用定时静默运行时，设置微信推送，在移动端即可查看到备案成功信息。

## 微信推送

本项目支持基于[Server酱](https://sct.ftqq.com/)的微信推送功能，仅需登录并扫码绑定，之后将获取到的 SCKEY 填入 `config.ini` 文件即可

## 责任须知

- 本项目仅供参考学习，造成的一切后果由使用者自行承担

## 证书

[Apache License 2.0](https://github.com/Bruuuuuuce/PKUAutoSubmit/blob/main/LICENSE)

## 版本历史

### version 1.1

- 发布于 2021.11.28
- 修改时间选项

### version 1.0

- 发布于 2021.11.28
- 项目初始版本
