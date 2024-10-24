# IP Info Tool

## 简介

IP Info Tool 是一个简单的工具，用于获取当前设备的 IP 信息和归属地。该工具使用 Python 编写，并提供图形用户界面（GUI），方便用户查看和复制 IP 信息。

## 功能

- 获取设备的公网 IP 地址
- 显示 IP 地址的详细地理位置信息（城市、地区、国家）
- 复制 IP 地址到剪贴板
- 图标化界面

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/weixin008/IPInfoTool.git
cd IPInfoTool
```

### 2. 安装依赖

你需要安装 Python 和以下依赖库：

```bash
pip install requests
```

### 3. 运行项目

```bash
python IP-Show.py
```

## 调整

你可以根据需要调整以下部分：

- **IP-Show.py**：可以修改脚本中的 API 调用、更改界面布局或添加新功能。
- **icon.ico**：如果你希望更换图标，可以替换此文件。

## 存在问题

- **网络依赖**：该工具需要网络连接以获取公网 IP 信息，如果网络连接不可用，工具将无法正常工作。
- **API 限制**：使用的 IP 信息查询 API 可能有调用限制，如果达到限制，工具将无法获取 IP 信息。
- **兼容性**：工具主要在 Windows 系统上开发和测试，其他操作系统可能需要额外的配置和测试。

## 依赖库

- [requests](https://pypi.org/project/requests/) - 用于发送 HTTP 请求获取 IP 信息。
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Python 标准库中的 GUI 工具包。

你可以使用以下命令来安装依赖库：

```bash
pip install requests
```

## 打包成可执行文件

你可以使用 PyInstaller 将脚本打包成可执行文件：

```bash
pyinstaller --onefile --windowed --icon=icon.ico IP-Show.py
```

## 贡献

欢迎提交 issues 和 pull requests 来改善这个工具。

## 许可

本项目基于 MIT 许可进行分发。
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.