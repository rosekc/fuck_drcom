# fuck_drcom

在没有网页界面下登录 szu 教工区 drcom 。不保证其他地方可用性。

## 环境要求

python 3.x， 依赖 `requests` 与 `click` 。

<!-- 
install_winrar.rar ??
```bash
pip install requests click
```
注：如果有 anaconda 环境就直接用就好。在不同机器上 `pip` 与 `python` 可能要改为 `pip3` 和 `python3` 。 -->

建议离线安装 anaconda 后使用。

## 下载源码

```bash
git clone git@github.com:rosekc/fuck_drcom.git
```

或者[直接下载](https://github.com/rosekc/fuck_drcom/archive/master.zip)。

## 使用方法

### 方法一（推荐）

复制一份 `config_sample.py` ，命名为 `config.py`, 在里面输入账号密码，之后直接 `python main.py` 即可。

### 方法二

使用 `CLI`。

```bash
Usage: main.py [OPTIONS]

Options:
  -u, --username TEXT
  -p, --password TEXT
  -a, --keep_alive BOOLEAN
  --help                    Show this message and exit.
```
