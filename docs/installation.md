# 预先安装

建议用conda管理包。

```shell
conda env create -f ./ubuntu_py39_bazi.yml
```

不做桌面程序，未来只考虑做成手机端APP，因此只用electron、cordova等。前端开发框架仍然使用framework7.

由于不做企业级开发，因此先不用ant-design。

```shell
sudo apt-get install libvips-dev
npm i -g framework7 cordova coffeescript @babel/core
```

