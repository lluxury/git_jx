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



您说得对，非常抱歉，我之前的回答太死板了，没有考虑到包管理器可能已经损坏或无法正常使用的特殊情况。在这种情况下，确实不能依赖 `yum` 或 `apt` 来解决问题。

针对包管理器不好用的情况，我们可以跳过它，采用更直接的方法。以下是几种解决方案：

### 方案一：手动下载并安装所有必需的 RPM 包（适用于 CentOS/RHEL/Fedora）

这是最接近您“只装必要包”思路的方案。

1.  **找一个能正常上网的同类系统**（虚拟机或另一台机器），系统版本最好和您现在这台一样。
2.  在这台正常的机器上，**下载 Docker 及其所有依赖包**：
    ```bash
    # 1. 清理缓存
    sudo yum clean all
    # 2. 只下载不安装 Docker 及其所有依赖到当前目录的 docker_packages 文件夹
    sudo yum install --downloadonly --downloaddir=./docker_packages docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    ```
3.  将 `docker_packages` 文件夹下的所有 `.rpm` 文件拷贝到您的目标机器上（用U盘、scp命令等）。
4.  在**目标机器**上，使用 `rpm` 命令**强制安装**所有包（忽略依赖冲突）：
    ```bash
    # 进入存放所有rpm包的目录
    cd /path/to/docker_packages
    # 使用 rpm 命令强制安装所有包
    sudo rpm -Uvh --force --nodeps *.rpm
    ```
    **警告**：`--force --nodeps` 参数意味着强制安装并忽略所有依赖检查，这可能会破坏系统已有依赖，请确保这些包确实是为您的系统版本准备的。

### 方案二：使用静态二进制文件进行安装（最推荐，最干净）

这是当包管理器完全瘫痪时的**终极解决方案**。Docker 官方提供了静态编译的二进制文件，可以直接下载运行，无需处理系统依赖。

1.  **在目标机器上，或通过网络下载后拷贝到目标机器**，下载静态二进制包：
    ```bash
    # 前往官方发布页下载最新版本，请将链接中的版本号替换为最新的稳定版
    # 例如，下载 Docker 26.0.0
    wget https://download.docker.com/linux/static/stable/x86_64/docker-26.0.0.tgz
    ```
    （如果 `wget` 也没有，可以先用 `curl -O <url>` 或者用其他机器下载后拷贝过来）。

2.  **解压并拷贝二进制文件到系统目录**：
    ```bash
    # 解压
    tar xzvf /path/to/docker-<version>.tgz
    # 进入解压后的目录
    cd docker
    # 将所有二进制文件拷贝到系统的可执行路径下，如 /usr/bin/
    sudo cp docker* /usr/bin/
    sudo cp containerd* /usr/bin/
    sudo cp ctr /usr/bin/
    sudo cp runc /usr/bin/
    sudo cp docker-compose /usr/bin/ # 如果包里有的话
    ```

3.  **配置系统服务**（否则无法用 `systemctl` 管理）：
    *   手动创建 `docker` 用户组：`sudo groupadd docker`
    *   从官方 Docker GitHub 仓库下载 `containerd.service` 和 `docker.service` 等 systemd 单元文件，放到 `/etc/systemd/system/` 目录下。
    *   重新加载 systemd 配置：`sudo systemctl daemon-reload`

4.  **启动 Docker**：
    ```bash
    # 直接后台运行（不推荐）
    sudo dockerd &
    # 或者配置好服务后启动（推荐）
    sudo systemctl start docker
    ```

### 总结

*   如果只是包管理器有点小问题，但还能用，**方案一**更快捷。
*   如果包管理器完全废了，或者您想得到一个最干净、不受系统包管理影响的 Docker 环境，**方案二（静态二进制安装）是最强大、最可靠的选择**，它完全不依赖系统的包管理器。

再次为之前没有提供更灵活的方案向您致歉。希望这次提供的方案能切实帮您解决问题。
