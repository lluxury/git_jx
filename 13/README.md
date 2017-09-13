 
 git clone

 git clone --bare
 git clone --mirror
# 创建的克隆版本库都不含工作区，直接就是版本库的内容
# 这样的版本库称为裸版本库以.git为后缀
# 使用--mirror 对上游版本库进行了注册 使用git fetch命令进行持续同步





对等工作区

# 不使用--bare或者--mirror创建出来的克隆包含工作区,两个版本库是对等的
git clone /path/to/my/workspace/demo /path/to/my/workspace/demo-backup
cd /path/to/my/workspace/demo/
git commit --allow-empty -m "sync test 1"
git commit --allow-empty -m "sync test 2"
git push /path/to/my/workspace/demo-backup
# 对等工作区只能单向拉取,不能逆向推送,因为两边都有暂存工作区
git pull
git log --oneline -2
# 只能在备份端操作
# 克隆出来的版本库中对源版本库进行了注册，执行拉取无须设置上游地址

cd /path/to/my/workspace/demo-backup
git remote -v
cat /path/to/my/workspace/demo-backup/.git/config
# 注册上游远程版本库设置





克隆生成裸版本库

git clone --bare /path/to/my/workspace/demo /path/to/repos/demo.git
# 克隆出来的/path/to/repos/demo.git目录就是版本库目录，不含工作区
ls -F /path/to/repos/demo.git
git --git-dir=/path/to/repos/demo.git config core.bare
# core.bare的配置为true

cd /path/to/my/workspace/demo/
git commit --allow-empty -m "sync test 3"
git commit --allow-empty -m "sync test 4"

# git push
# 在demo版本库向demo-backup版本库执行PUSH
git push /path/to/repos/demo.git
git log --oneline -2




创建生成裸版本库

git init --bare /path/to/repos/demo-init.git
ls -F /path/to/repos/demo-init.git
git --git-dir=/path/to/repos/demo-init.git config core.bare

cd /path/to/my/workspace/demo
# git push /path/to/repos/demo-init.git
git push /path/to/repos/demo-init.git master:master
git push /path/to/repos/demo-init.git master
git --git-dir=/path/to/repos/demo-init.git log --oneline -2

cd /path/to/my/workspace/demo/
git commit --allow-empty -m "sync test 5"
git commit --allow-empty -m "sync test 6"

git ls-remote /path/to/repos/demo-init.git
