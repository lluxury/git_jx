git --version

# 全局文件: 主目录下的.gitconfig 或 /etc/gitconfig

git config --global user.name "yann"
git config --global user.email tmp4321@qq.com

# 全局
sudo git config --system alias.br branch
sudo git config --system alias.ci "commit -s"
sudo git config --system alias.co checkout
sudo git config --system alias.st "-p status"

# 本人
git config --global alias.st status
git config --global alias.ci "commit -s"
git config --global alias.co checkout
git config --global alias.br branch

# 建库
# cd /path/to/my/workspace
# mkdir demo
# cd demo
# git init
# 初始化空的 Git 版本库于 /path/to/my/workspace/demo/.git/

cd /path/to/my/workspace
git init demo
# 初始化空的 Git 版本库于 /path/to/my/workspace/demo/.git/
cd demo

# 隐藏的.git目录就是Git版本库,仓库,repository
# .git版本库目录所在的目录，即/path/to/my/workspace/demo目录称为工作区

echo "Hello." > welcome.txt
git add welcome.txt
git ci -m "initialized"






# CVS，工作区的根目录及每一个子目录下都有一个CVS目录
# Subversion来说，工作区的根目录下都一个.svn目录
# xx 服务器端建立的文件跟踪

git grep "工作区文件内容搜索"

# 当在Git工作区目录下执行操作的时候，会对目录依次向上递归查找.git 目录，找到的.git目录就是工作区对应的版本库，
# .git所在的目录就是工作区的根目录，文件.git/index记录了工作区文件的状态,暂存区的状态

strace -e 'trace=file' git status
# sudo dtruss git status     os x
# 跟踪git status命令时的磁盘访问

# 显示版本库.git目录所在的位置
git rev-parse --git-dir

# 显示工作区根目录
git rev-parse --show-toplevel

# 相对于工作区根目录的相对目录
git rev-parse --show-prefix

显示从当前目录到工作区的根的深度
git rev-parse --show-cdup





# git config 命令实际操作的文件
cd /path/to/my/workspace/demo/
git config -e

# 全局配置文件进行编辑
git config -e --global

# 系统级配置文件进行编辑
git config -e --system

# 版本库级别的配置文件、全局配置文件（用户主目录下）和系统级配置文件（/etc目录下）其中版本库级别配置文件的优先级最高

INI文件格式
git config core.bare
git config a.b something
git config x.y.z others

# 可以用git config命令操作任何其他的INI文件
GIT_CONFIG=test.ini git config a.b.c.d "hello, world"
GIT_CONFIG=test.ini git config a.b.c.d
# 设定值,读值







# 删除设置
git config --unset --global user.name
git config --unset --global user.email

cd /path/to/my/workspace/demo
git commit --allow-empty -m "who does commit?"
--allow-empty 空提交

git log --pretty=fuller
git config --global user.name "yann"
git config --global user.email tmp4321@qq.com
git commit --amend --allow-empty --reset-author

# Git对提交者的用户名和邮件地址做了的猜测




# Android项目Gerrit的审核服务器
# Redmine 一款实现需求管理和缺陷跟踪的项目管理软件



git config --global alias.ci "commit -s"
# 会在提交的说明中自动添加上包含提交者姓名和邮件地址的签名标识，
# 类似于Signed-off-by: User Name <email@address>




备份
cd /path/to/my/workspace
git clone demo demo-step-1