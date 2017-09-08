
git rev-list HEAD | wc -l


图形工具：gitk
gitk --since="2 weeks ago"
gitk v2.6.12.. include/scsi drivers/scsi


图形工具：gitg
sudo aptitude install gitg
which gitg
cd /path/to/my/workspace/demo
rm src/hello.h
echo "Wait..." >> README
git status -s
gitg &


图形工具：qgit
sudo aptitude install qgit
which qgit
git reset HEAD^
git status
qgit &

# 以上都是linux下的工具,基本不会用到





命令行工具

cd /path/to/my/workspace/
git clone git://github.com/ossxp-com/gitdemo-commit-tree.git
cd gitdemo-commit-tree
# Git的版本表示法和版本范围表示法



版本表示法

git rev-parse --symbolic --branches
git rev-parse --symbolic --tags
#显示tag

git rev-parse --symbolic --glob=refs/*
# 显示定义的所有引用

git rev-parse  HEAD
# 显示HEAD对应的SHA1哈希值

git describe
# A-1-g6652a0d
git rev-parse A-1-g6652a0d
# git describe的输出显示为SHA1哈希值

git rev-parse  master  refs/heads/master
# 多个表达式的SHA1哈希值

git rev-parse  6652  6652a0d
# 用哈希值的前几位指代整个哈希值

git rev-parse  A  refs/tags/A
# 里程碑对象不一定是提交，有可能是一个Tag对象
# Tag对象包含说明或者签名，还包括到对应提交的指向

git rev-parse  A^{}  A^0  A^{commit}
# 轻量级里程碑 直接指向提交的里程碑或者作用于提交本身

git rev-parse  A^  A^1  B^0
# A的第一个父提交就是B所指向的提交
# 当一个提交有多个父提交时，可以通过在符号^后面跟上一个数字表示第几个父提交
# A^ 就相当于 A^1
# 而B^0代表了B所指向的一个Commit对象 B是Tag对象
# 有3个父提交

git rev-parse  A^^3^2  F^2  J^{}
# 连续的^符号依次沿着父提交进行定位至某一祖先提交
# A的第三第一个父提交,F的第二个父提交

git rev-parse  A~3  A^^^  G^0
# 记号~<n>就相当于连续<n>个符号^

git rev-parse  A^{tree}  A:
# 里程碑A对应的目录树

git rev-parse  A^{tree}:src/Makefile  A:src/Makefile
# 显示树里面的文件

git rev-parse  :gitg.png  HEAD:gitg.png
# 暂存区里的文件和HEAD中的文件相同

git rev-parse :/"Commit A"
# 可以通过在提交日志中查找字串的方式显示提交

git rev-parse HEAD@{0} master@{0}
# reflog相关的语法




版本范围表示法

git rev-list --oneline  A
# 一个提交ID实际上就可以代表一个版本列表

git rev-list --oneline  D  F
# 两个或多个版本，相当于每个版本单独使用时指代的列表的并集

git rev-list --oneline  ^G D
git rev-list --oneline  G..D
# 排除这个版本及其历史版本, D开始排除G

git rev-list --oneline  ^B C
git rev-list --oneline  B..C
# C开始排除B

git rev-list --oneline  C ^B
git rev-list --oneline  C..B
# B开始排除C   C.. 等价于 ^C


git rev-list --oneline  B...C
# 三点表示法的含义是两个版本共同能够访问到的除外
# B和C共同能够访问到的F、I、J排除在外

git rev-list --oneline  B^@
# 某提交的历史提交，自身除外，用语法r1^@表示

git rev-list --oneline  B^!
git rev-list --oneline  F^! D
# 提交本身不包括其历史提交，用语法r1^!表示





浏览日志：git log

git log --oneline F^! D
# 当不使用任何参数调用，相当于使用了缺省的参数HEAD

git config --global alias.glog "log --graph"
# 通过--graph参数调用git log可以显示字符界面的提交关系图,定义别名

git glog --oneline

git log -3 --pretty=oneline
# 显示最近的几条日志

git log -p -1
# 显示每次提交的具体改动

git log --stat --oneline  I..C
# 显示每次提交的变更概要
# C的历史提交,排除I分支的


定制输出

git log --pretty=raw -1
# 参数--pretty=raw显示提交的原始数据。可以显示提交对应的树ID

git log --pretty=fuller -1
# 参数--pretty=fuller会同时显示作者和提交者

git log --pretty=oneline -1
# 参数--pretty=oneline显然会提供最精简的日志输出

git show D --stat
# git show显示里程碑D及其提交
git show old_practice --stat


git cat-file -p D^0
# 使用git cat-file显示里程碑D及其提交
# 参数-p的含义是美观的输出pretty





差异比较：git diff

# 比较里程碑B和里程碑A，用命令：git diff B A
# 比较工作区和里程碑A，用命令：git diff A
# 比较暂存区和里程碑A，用命令：git diff –-cached A
# 比较工作区和暂存区，用命令：git diff
# 比较暂存区和HEAD，用命令：git diff –-cached
# 比较工作区和HEAD，用命令：git diff HEAD


git diff c668ddb 721dd53 ~/coding/python/shadowsocks
# 差异比较还可以使用路径参数，只显示不同版本间该路径下文件的差异

git diff test1 test2
# 非Git目录/文件的差异比较





扩展的差异语法
git diff --word-diff
# 逐词比较




文件追溯：git blame

cd /path/to/my/workspace/gitdemo-commit-tree
git blame README
# 逐行显示文件,查责任

git blame -L 6,+5 README
# 只想查看某几行




二分查找：git bisect

# 问题肯定出在两版本之间的某次代码提交上
# 找到一个正确的版本，使用git bisect命令在版本库中进行二分查找
git log doc/B.txt

cd /path/to/my/workspace/gitdemo-commit-tree/
git checkout master
# 确认工作在master分支

git bisect start
# 开始二分查找

git cat-file -t master:doc/B.txt
# blob
git cat-file -t G:doc/B.txt
# 已经当前版本是“坏提交”，因为存在文件doc/B.txt
# G版本是“好提交”，因为不存在文件doc/B.txt

git bisect bad
git bisect good G
# 将当前版本HEAD标记为“坏提交”，将G版本标记为“好提交”

git describe
# C
ls doc/B.txt
git bisect good
# 自动定位到C提交。没有文件doc/B.txt，也是一个好提交

ls doc/B.txt
git bisect good

git bisect bad
# 定位到B版本，这是一个“坏提交”

git bisect good
# 现在定位到E版本，这是一个“好提交”。
# 当标记E为好提交之后，输出显示已经成功定位到引入坏提交的最接近的版本

git checkout bisect/bad
# 最终定位的坏提交用引用refs/bisect/bad标识 切换到该版本


# 当对“Bug”定位和修复后，撤销二分查找在版本库中遗留的临时文件和引用
git bisect reset
# 撤销二分查找后，版本库切换回执行二分查找之前所在的分支


# 错误提交 E
git bisect bad
git bisect log > logfile
# 用git bisect log命令查看二分查找的日志记录
vi logfile
# 编辑这个文件，删除记录了错误动作的行
git bisect reset
# 结束上一次出错的二分查找
git bisect replay logfile
# 通过日志文件恢复进度
git describe
# E
git bisect good
# 再一次回到了提交E,可以继续判断



自动化测试

vi good-or-bad.sh
    #!/bin/sh
    
    [ -f doc/B.txt ] && exit 1
    exit 0  

git bisect start master G
# 从已知的坏版本master和好版本G，开始新一轮的二分查找

git bisect run sh good-or-bad.sh
# 自动化测试，使用脚本good-or-bad.sh

git describe refs/bisect/bad
# 定位到最早的坏版本




获取历史版本

git ls-tree 776c5c9 README
git ls-tree -r refs/tags/D doc
# 查看历史提交的目录树

git checkout HEAD^^
# 整个工作区切换到历史版本

git checkout refs/tags/D – README
git checkout 776c5c9 – doc
# 检出某文件的历史版本

git show 887113d:README > README.OLD
# 检出某文件的历史版本到其他文件名


