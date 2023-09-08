# genshin-impact-skip-dialogue
a tool to  skip genshin impact skip dialogue 

# Skip Genshin Impact Dialogue
[English](docs/README.en.md)

genshin-impact-skip-dialogue 是一个用于跳过原神游戏中的对话和剧情场景的工具。这个工具可以帮助自动点击对话、选择对话选项，拾取物品。基于opencv-pythond的图像识别，不支持对话加速功能。


## 配置文件选项

需要以1920*1080窗口模式运行游戏， 默认暂停快捷键 `pause` , `alt+p`

```yaml
# tasks pause shortcut keys
tasks_pause: alt+p
```

## 使用说明

### 使用打包好的Releases

从 [releases](https://github.com/liu-stan/genshin-impact-skip-dialogue/releases) 下载解压， 以管理员身份运行gs_skip.exe

### 从源代码运行

1. 克隆项目仓库到你的本地计算机, 下载源码到本地

```

git clone https://github.com/liu-stan/genshin-impact-skip-dialogue.git

cd genshin-impact-skip-dialogue

```

2. 创建一个Python虚拟环境, 激活虚拟环境， 安装依赖项

```

python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```


3. 运行，需要管理员身份运行

```
python gs_skip.py

```

4. 使用 pyinstaller 打包，复制文件夹images和config.yaml到dist文件夹下，然后以管理员身份gs_skip.exe

```
pyinstaller --onefile gs_skip.py

```