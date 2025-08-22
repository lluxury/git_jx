# RedHat 导出 Docker 25.0.8 及依赖安装包

## 1. 在有网络的环境中下载所有 RPM 包

### 创建下载目录
```bash
mkdir -p ~/docker-25.0.8-offline
cd ~/docker-25.0.8-offline
```

### 下载 Docker 25.0.8 及所有依赖
```bash
# 启用 Docker 仓库（仅用于获取包信息，不安装）
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 下载 Docker 25.0.8 及所有依赖
yumdownloader --resolve --destdir=. \
    docker-ce-25.0.8-1.el9 \
    docker-ce-cli-25.0.8-1.el9 \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

# 或者指定架构（x86_64）
yumdownloader --resolve --arch=x86_64 --destdir=. \
    docker-ce-25.0.8-1.el9 \
    docker-ce-cli-25.0.8-1.el9 \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin
```

## 2. 手动下载特定版本（如果 yumdownloader 不行）

```bash
# Docker 25.0.8 主包
curl -L -O https://download.docker.com/linux/centos/9/x86_64/stable/Packages/docker-ce-25.0.8-1.el9.x86_64.rpm

# Docker CLI
curl -L -O https://download.docker.com/linux/centos/9/x86_64/stable/Packages/docker-ce-cli-25.0.8-1.el9.x86_64.rpm

# containerd.io
curl -L -O https://download.docker.com/linux/centos/9/x86_64/stable/Packages/containerd.io-1.6.28-3.1.el9.x86_64.rpm

# 其他可能需要的依赖
curl -L -O https://download.docker.com/linux/centos/9/x86_64/stable/Packages/docker-buildx-plugin-0.12.1-1.el9.x86_64.rpm
curl -L -O https://download.docker.com/linux/centos/9/x86_64/stable/Packages/docker-compose-plugin-2.24.5-1.el9.x86_64.rpm

# 系统依赖（可能需要）
curl -L -O http://mirror.centos.org/centos/9/BaseOS/x86_64/os/Packages/container-selinux-2.189.0-1.el9.noarch.rpm
curl -L -O http://mirror.centos.org/centos/9/BaseOS/x86_64/os/Packages/libcgroup-2.0.2-4.el9.x86_64.rpm
```

## 3. 打包所有下载的 RPM 文件

```bash
# 创建离线安装包
tar -czvf docker-25.0.8-offline-el9.tar.gz *.rpm

# 查看包内容
tar -tzvf docker-25.0.8-offline-el9.tar.gz
```

## 4. 在目标机器上安装

### 上传并解压包到目标机器
```bash
# 创建安装目录
mkdir -p ~/docker-offline-install
cd ~/docker-offline-install

# 上传并解压（如果从其他机器传输）
tar -xzvf docker-25.0.8-offline-el9.tar.gz
```

### 按依赖顺序手动安装
```bash
# 先安装系统依赖
sudo rpm -ivh container-selinux-*.rpm
sudo rpm -ivh libcgroup-*.rpm

# 安装容器运行时
sudo rpm -ivh containerd.io-*.rpm

# 安装 Docker CLI
sudo rpm -ivh docker-ce-cli-*.rpm

# 安装 Docker 主包
sudo rpm -ivh docker-ce-*.rpm

# 安装插件（可选）
sudo rpm -ivh docker-buildx-plugin-*.rpm
sudo rpm -ivh docker-compose-plugin-*.rpm
```

### 或者一次性安装所有包
```bash
# 一次性安装所有 RPM 包（rpm 会自动处理依赖顺序）
sudo rpm -ivh *.rpm
```

## 5. 如果遇到依赖问题，手动解决

```bash
# 查看缺少的依赖
sudo rpm -ivh docker-ce-*.rpm 2>&1 | grep "is needed"

# 手动下载缺少的依赖（在有网络的机器上）
# 例如：如果缺少 libseccomp
yumdownloader --destdir=. libseccomp

# 然后上传并安装缺少的依赖包
sudo rpm -ivh libseccomp-*.rpm
```

## 6. 安装后配置和验证

```bash
# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 验证安装
docker --version
# 应该显示: Docker version 25.0.8, build 2ae903e

# 测试 Docker
sudo docker run --rm hello-world

# 检查服务状态
sudo systemctl status docker
```

## 7. 完整的依赖包列表（参考）

通常需要以下包：
- `docker-ce-25.0.8-1.el9.x86_64.rpm`
- `docker-ce-cli-25.0.8-1.el9.x86_64.rpm`
- `containerd.io-1.6.28-3.1.el9.x86_64.rpm`
- `container-selinux-2.189.0-1.el9.noarch.rpm`
- `libcgroup-2.0.2-4.el9.x86_64.rpm`
- `docker-buildx-plugin-0.12.1-1.el9.x86_64.rpm`（可选）
- `docker-compose-plugin-2.24.5-1.el9.x86_64.rpm`（可选）

## 8. 注意事项

1. **架构匹配**：确保下载的包与目标机器架构一致（通常是 x86_64）
2. **系统版本**：确认是 EL9（CentOS 9/RHEL 9）的包
3. **依赖顺序**：如果一次性安装失败，按上面顺序手动安装
4. **SELinux**：如果遇到 SELinux 问题，可以临时禁用 `sudo setenforce 0`

使用这种方法可以完全离线安装 Docker 25.0.8，不需要使用 yum 安装命令。
