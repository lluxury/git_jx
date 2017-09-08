cd /path/to/my/workspace/demo
git log --stat

echo "Nice to meet you." >> welcome.txt
# 和本地比较, 中间状态的文件
git diff
git commit -m "Append a nice line."

 git log --pretty=oneline
 git status -s

 # add操作对于其他版本控制系统来说是向版本库添加新文件用的，
 # 修改的文件（已被版本控制跟踪的文件）在下次提交时会直接被提交

 git add welcome.txt
 git diff
 git diff HEAD
 git status

 git status -s
# 位于第一列的字符M的含义是：
#   版本库中的文件和处于中间状态——提交任务（提交暂存区，即stage）中的文件相比有改动
# 位于第二列的字符M的含义是：
#   工作区当前的文件和处于中间状态——提交任务（提交暂存区，即stage）中的文件相比也有改动

echo "Bye-Bye." >> welcome.txt
git status
git status -s
# 暂存区文件,工作区文件,最新版本库中文件,都有改动

git diff
# 工作区最新改动，即工作区和提交任务（暂存区，stage）中相比的差异

git diff HEAD
# 将工作区和HEAD（当前工作分支）最新库版

git diff --cached
git diff --staged
# 暂存区（提交任务，stage）和版本库中已提交最新文件的差异

git commit -m "which version checked in?"
git log --pretty=oneline
git status -s
# 第一列的M被提交
# 暂存区,stage,index






git checkout -- welcome.txt
git status -s     # 执行 git diff 
ls --full-time .git/index

git status -s     # 执行 git diff 
ls --full-time .git/index


touch welcome.txt
git status -s     # 执行 git diff 
ls --full-time .git/index
# 当执行git status命令（或者git diff命令）扫描工作区改动的时候，
# 先依据.git/index文件中记录的（工作区跟踪文件的）时间戳、长度等信息判断工作区文件是否改变

# 文件.git/index实际上就是一个包含文件索引的目录树，
# 在这个虚拟工作区的目录树中，记录了文件名、文件的状态信息（时间戳、文件长度等）

# 文件的内容并不存储其中，而是保存在Git对象库.git/objects目录中，
# 文件索引建立了文件和对象库中对象实体之间的对应


# HEAD实际是指向master分支的一个“游标”
# objects标识的区域为Git的对象库，实际位于.git/objects目录下

暂存区
# git add 暂存区的目录树被更新，
# 变更内容被写入到对象库中的一个新的对象中，而该对象的ID被记录在暂存区的文件索引中

# git commit
# 暂存区的目录树写到版本库（对象库）中，master分支会做相应的更新

# git reset HEAD 暂存区的目录树会被重写，
# 被master分支指向的目录树所替换，但是工作区不受影响

# git rm –-cached <file> 会直接从暂存区删除文件，工作区则不做出改变

# git checkout .或者git checkout – <file> 会用暂存区文件替换工作区的文件

# git checkout HEAD .或者git checkout HEAD <file> 
# 用HEAD指向的master分支中文件替换暂存区和以及工作区中的文件
# 会清除工作区中未提交的改动，也会清除暂存区中未提交的改动






# 暂存区目录树的浏览
git ls-tree -l HEAD

cd /path/to/my/workspace/demo
git clean -fd
git checkout .
# 清除当前工作区中没有加入版本库的文件和目录
# git checkout .命令，用暂存区内容刷新工作区

echo "Bye-Bye." >> welcome.txt
mkdir -p a/b/c
echo "Hello." > a/b/c/hello.txt
git add .
echo "Bye-Bye." >> a/b/c/hello.txt
git status -s

find . -path ./.git -prune -o -type f -printf "%-20p\t%s\n"
git ls-files -s
# 显示暂存区的目录树


# 如果想要使用git ls-tree命令，需要先将暂存区的目录树写入Git对象库
# git write-tree，然后在针对git write-tree命令写入的 tree 执行git ls-tree命令
git write-tree
git ls-tree -l 9431f4a
# git write-tree的输出就是写入Git对象库中的Tree ID

git write-tree | xargs git ls-tree -l -r -t
# 递归操作显示目录树的内容


# 不要使用git commit -a


git stash
git status








