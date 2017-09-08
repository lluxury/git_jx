

 现场版本控制
# 在客户现场或在产品部署的现场，进行源代码的修改，并在修改过程中进行版本控制


# svn版
# 在其他位置建立一个SVN版本库
svnadmin create /path/to/repos/project1

# 在需要版本控制的目录下检出刚刚建立的空版本库
svn checkout file:///path/to/repos/project1 .

# 执行文件添加操作，然后执行提交操作这个提交将是版本库中编号为1的提交
svn add *
svn ci -m "initialized"

# 在工作区中修改文件，提交
svn ci

# 通过创建补丁文件的方式将工作成果保存带走
# SVN很难对每次提交逐一创建补丁,一般用下面的命令与最早的提交进行比较

svn diff -r1 > hacks.patch

# SVN的补丁文件不支持二进制文件，
# 采用补丁文件的方式有可能丢失数据，如新增或修改的图形文件会丢失

svnadmin dump --incremental -r2:HEAD  /path/to/repos/project1/ > hacks.dump
# 版本库导出恢复


# git版
# 在需要版本控制的目录下执行Git版本库初始化命令
git init

# 添加文件并提交
git add -A
git commit -m "initialized"

# 为初始提交建立一个里程碑：v1
git tag v1

# 在工作区中工作——修改文件，提交
 git commit -a

# 打包带走,将从v1开始的历次提交逐一导出为补丁文件, 20章
git format-patch v1..HEAD
# 0001-Fix-typo-help-to-help.patch

# 通过邮件将补丁文件发出
git send-email *.patch

# 导入不能使用不能使用GNU patch命令, 38章




重写提交说明
# SVN
# SVN的提交说明默认是禁止更改的，因为SVN的提交说明属于不受版本控制的属性，一旦修改就不可恢复
# 在配置了版本库更改的外发邮件通知之后，再开放提交说明更改的功能
svn ps --revprop -r <REV> svn:log "new log message..."

# git
git commit --amend
# 修改最新提交

git rebase -i <commit-id>^
# 修改历史提交的提交说明 12章




想吃后悔药
# SVN
# 删除错误加入的大文件，再提交,没有效果,还在历史版本库里
# SVN管理员要是没有历史备份的话，只能从头用svnadmin dump导出整个版本库
# 再用svndumpfilter命令过滤掉不应检入的大文件
# 然后用svnadmin load重建版本库
# http://www.cnblogs.com/ckat/p/3642826.html


# Git
# 最新提交
git rm --cached winxp.img
git commit --amend

# 历史版本
git rebase -i <commit-id>^

# 执行交互式变基操作抛弃历史提交，版本库还不能立即瘦身，14章或 35章4节




更好用的提交列表
# 正确的版本控制系统的使用方法是，一次提交只干一件事：
# 完成一个新功能、修改了一个Bug、或是写完了一节的内容、或是添加了一幅图片

# SVN
svn changelist
# 功能有限制

# Git
# 筛选提交
# 执行git add命令将修改内容加入提交暂存区
# 执行git add -u命令可以将所有修改过的文件加入暂存区
# 执行git add -A命令可以将本地删除文件和新增文件都登记到提交暂存区
# 执行git add -p命令甚至可以对一个文件内的修改进行有选择性的添加
git add -p

# 一个修改后的文件被登记到提交暂存区后，可以继续修改，
# 继续修改的内容不会 被提交，除非再对此文件再执行一次git add命令

# 执行git commit命令提交，无须设定什么变更列表，直接将登记在暂存区中的内容提交
# Git支持对提交的撤消，而且可以撤消任意多次




更好的差异比较
# git支持对二进制文件的差异比较
git diff –word-diff     #进行逐字比较
# 工作区的文件修改可能会有两个不同的版本，一个是在提交暂存区，一个是在工作区
# git diff比较复杂, 5章

git diff
git diff –cached


工作进度保存
# 如果工作区的修改尚未完成时，忽然有一个紧急的任务，
# 需要从一个干净的工作区开始新的工作，或要切换到别的分支进行工作

# SVN
如果版本库规模不大，最好重新检出一个新的工作区，在新的工作区进行工作,或
svn diff > /path/to/saved/patch.file
svn revert -R
svn switch <new_branch>

# 在新的分支中工作完毕后，再切换回当前分支，将补丁文件重新应用到工作区
svn switch <original_branch>
patch -p1 < /path/to/saved/patch.file
#补丁为修改且未提交部分?, SVN的补丁文件不支持二进制文件


# git
# 在切换到新的工作分支之前，执行git stash保存工作进度，工作区会变得非常干净，然后就可以切换到新的分支中了
git stash
git checkout <new_branch>

# 修改完毕后，再切换回当前分支，调用git stash pop命令则可恢复之前保存的工作进度
git checkout <orignal_branch>
git stash pop

# 9章



代理SVN提交
# SVN集中式版本控制系统，要求使用者和版本控制服务器之间要有网络连接
# 当版本控制服务器无法实现从SVN到Git的迁移时，仍然可以使用Git进行工作
# Git作为客户端来操作SVN服务器，实现在移动办公状态下的版本提交（本地Git库）
# 访问SVN服务器，将SVN版本库克隆为一个本地的Git库，含针对SVN的扩展
git svn clone <svn_repos_url>

# 使用Git命令操作本地克隆的git版本库
git commit

# 将本地提交同步给SVN服务器,先获取SVN服务器上最新的提交，再执行变基操作
git svn fetch
git svn rebase
git svn dcommit
# 26章





分页器
# 常用的Git的命令都带有一个分页器
# 字母q：退出分页器
# 字母h：显示分页器帮助
# 按空格下翻一页，按字母 b 上翻一页
# 字母d和u：分别代表向下翻动半页和向上翻动半页
# 字母j和k：分别代表向上翻一行和向下翻一行
# 如果行太长被截断，可以用左箭头和右箭头使得窗口内容左右滚动
# 输入/pattern：向下寻找和pattern匹配的内容
# 输入?pattern：向上寻找和pattern匹配的内容
# 字母n或N：代表向前或向后继续寻找
# 字母g：跳到第一行；字母G：跳到最后一行；输入数字再加字母g：则跳转到对应的行
# 输入!<command>：可以执行Shell命令

git -p status
git config --global pager.status true

# 自动折行
export LESS=FRX
git config --global core.pager 'less -+$LESS -FRX'



