# SRUN-UESTC
## UESTC Graduate SRUN Auto Login Script
本库用于自动登录电子科技大学研究生深澜软件网络。它使用Selenium WebDriver来自动化登录过程，并在网络断开时重新连接。

*源自 [LambdaYH/UESTC-SRUN](https://github.com/LambdaYH/UESTC-SRUN)*

### 依赖安装步骤

#### 1. 安装Google Chrome


如果尚未安装Google Chrome，请使用以下命令进行安装：

```bash
sudo apt-get update
sudo apt-get install -y wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

#### 2. 安装Selenium和webdriver_manager

使用pip安装Selenium和webdriver_manager库：

```bash
pip install selenium
pip install webdriver-manager
```

#### 3. 下载并安装ChromeDriver

根据你的Chrome版本下载对应的ChromeDriver。若Chrome版本大于115，请在 Chrome for Testing 查看下载地址。例如，对于Chrome版本126.0.6478.126，下载地址为：

```bash
wget https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
```

### 使用说明
#### 1. 克隆或下载项目

```bash
git clone https://github.com/your-repo/UESTC-SRUN-Auto-Login.git
cd UESTC-SRUN-Auto-Login
```
#### 2. 运行脚本

运行以下命令启动自动登录脚本：

```bash
python auto_login.py
```
脚本将根据配置文件中的设定，在网络断开时自动尝试重新连接，并在日志文件中记录相关信息。

### 设置开机自启
在Linux系统上，可以通过systemd服务实现脚本的开机自启。以下是配置步骤：

#### 1. 创建服务文件

```bash
sudo vim /etc/systemd/system/uestc-srun-login.service
```
在文件中添加以下内容：
```ini
[Unit]
Description=UESTC SRUN Auto Login Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/caesarg/UESTC-SRUN/auto_login.py
Restart=on-failure
User=your_username

[Install]
WantedBy=multi-user.target
```

请将your_username替换为你在系统中的用户名。

#### 2. 重新加载systemd配置

```bash
sudo systemctl daemon-reload
```

#### 3. 启动并启用服务

启动服务：

```bash
sudo systemctl start uestc-srun-login.service
```
启用服务，使其在开机时自动启动：

```bash
sudo systemctl enable uestc-srun-login.service
```

#### 4. 检查服务状态

你可以使用以下命令来检查服务的状态：

```bash
sudo systemctl status uestc-srun-login.service
```
这样，脚本将在每次系统启动时自动运行。