# 伟大的 `lae` 由此开始

### How to usage:
```bash
lae docker    # 以当前项目按照 app.yaml 里的描述 build docker image
lae env       # 安装当前项目的依赖到 env 目录
lae runserver # 以开发模式启动本项目
```

### Install
```bash

git clone git@gitlab.linkedsee.com:platform/lae.git
cd lae
python setup.py install
```

### TODO:
- [ ] app.yaml 静态资源部分，并生成 nginx 配置
- [ ] 解析 app.yaml mqs 部分
- [ ] 向 项目提供 统一的 db， redis， 存储， upload 等服务
- [ ] 添加 service 的暴露，app.yaml server 依赖解析