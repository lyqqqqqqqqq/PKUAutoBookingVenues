# PKUAutoBookingVenues
PKU智慧场馆自动预约工具

部分代码和这个README的一部分引用自大佬的自动报备项目 https://github.com/Bruuuuuuce/PKUAutoSubmit


## 说明

- 本工具采用 Python3 搭配 `selenium` 完成自动化操作，实现全自动预约场馆
- 支持基于[Server酱](https://sct.ftqq.com/)的备案结果微信推送功能，体验更佳
- 采用定时任务可实现定期（如每周）免打扰预约，请设置在三天前的11:55-12:00之间
- 第三方依赖包几乎只有 `selenium` 一个
- 由于我只测试过羽毛球场的预约，其他场馆只是理论上可行，如果出现任何问题，可以提issue
- 支持时间上的“或”关系，支持按照星期几设定时间
- 时间上的“与”关系可通过设置多份`config[0-9][0-9].ini`文件实现
- `config`参数填写`config.ini`文件的名称，类型为字符串
- `lst_config`为config文件名称字符串构成的列表
- `page(config)`单独处理每个`config.ini`文件,`muilti_run(lst_config)`并行处理`lst_config`列表中的所有`config.ini`，`sequence_run(lst_config)`按序处理
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

1. 将 `config.sample.ini` 文件重命名为 `config0.ini` ，如果需要多个账号预约，或者需要时间上的“与”关系，请设置多个.ini文件（最多为两位数），
   请不要新建文件，不然自己搞定编码问题

2. 用文本编辑器（建议代码编辑器）打开 `config0.ini` 文件

3. 配置 `[login]` 、`[type]` 、`[time]`、`[wechat_notice]` 这几个 Section 下的变量，在 `config0.ini.sample` 文件内有详细注释


## 定时运行

### Windows

本项目中的 `autoRun.bat` 文件可提供在静默免打扰情况下运行程序的选择，配合 Windows 任务计划管理可实现定期自动填报，具体请参考[Win10下定时启动程序或脚本](https://blog.csdn.net/xielifu/article/details/81016220)

### mac OS

进入项目根目录，以命令 `./macAutoRun.sh` 执行 `macAutoRun.sh` 脚本即可，可设定或取消定时运行

### Linux

使用 `crontab` 设置

**Note:** 静默运行的弊端为无法看到任何报错信息，若程序运行有错误，使用者很难得知。故建议采用定时静默运行时，设置微信推送，在移动端即可查看到备案成功信息。

## 微信推送

本项目支持基于[Server酱](https://sct.ftqq.com/)的微信推送功能，仅需登录并扫码绑定，之后将获取到的 SCKEY 填入 `config0.ini` 文件即可

## 责任须知

- 本项目仅供参考学习，造成的一切后果由使用者自行承担

## 证书

[Apache License 2.0](https://github.com/yanyuandaxia/PKUAutoBookingVenues/blob/main/LICENSE)

## 版本历史
### version 2.6

- 发布于 2022.3.11
- 增加场地编号选项，增加稳定性

### version 2.5

- 发布于 2022.1.6
- 优化微信提醒内容，增加稳定性

### version 2.4

- 发布于 2021.12.21
- debug

### version 2.3

- 发布于 2021.12.17
- 增加Firefox支持，增加稳定性，优化速度，优化提醒消息

### version 2.2

- 发布于 2021.12.10
- 增加调试代码，取消多次运行（现可通过计划任务实现）

### version 2.1

- 发布于 2021.12.08
- 修复bug

### version 2.0

- 发布于 2021.12.08
- 优化逻辑，可提前1min进入预约页面等待，丰富log功能

### version 1.3

- 发布于 2021.12.04
- 优化逻辑，增加log功能

### version 1.2

- 发布于 2021.11.29
- 增加并行预约功能

### version 1.1

- 发布于 2021.11.28
- 修改时间选项，增加“与”、“或”关系和多用户配置

### version 1.0

- 发布于 2021.11.28
- 项目初始版本
