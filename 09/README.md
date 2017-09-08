

暂存区实践总结
git stash list
git stash pop

git commit -m "add new file: hello.txt"
git status -s
# 提交

git reset --soft HEAD^
git log -1 --pretty=oneline
git status -s
# 撤销提交

git add welcome.txt
git status -s

git reset HEAD a/b/c
git status -s
#撤出暂存区

git reset
# 撤出添加

git checkout -- welcome.txt
#清除修改

git status
git clean -nd
git clean -fd
git status -s
# 删除多余文件






使用git stash

git stash
# 保存当前工作进度 会分别对暂存区和工作区的状态进行保存

git stash list

git stash pop
# --index除了恢复工作区的文件外，还尝试恢复暂存区

git stash save --patch "message..."
# 使用参数--patch会显示工作区和HEAD的差异
# 使用-k或者--keep-index参数，不重置, 缺省会将暂存区和工作区强制重置

git stash apply 
# 不删除恢复的进度

git stash drop 
# 删除一个存储的进度

git stash clear
# 删除所有存储的进度

git stash branch 
# 基于进度创建分支





探秘git stash
git --exec-path
ls /usr/libexec/git-core/
#脚本目录

file /usr/libexec/git-core/git-stash
#shell脚本开发

git stash list
echo Bye-Bye. >> welcome.txt
echo hello. > hack-1.txt
git add hack-1.txt
git status -s

git stash save "hack-1: hacked welcome.txt, newfile hack-1.txt"

git status -s
ls

echo fix. > hack-2.txt
git stash
# 进度保存失败 本地没有被版本控制系统跟踪的文件并不能保存进度


git add hack-2.txt
git stash

git stash list
# git stash用引用和引用变更日志reflog来实现的

ls -l .git/refs/stash .git/logs/refs/stash
git reflog show refs/stash
# 用git stash保存进度，会将进度保存在引用refs/stash所指向的提交中
# refs/stash引用的变化由reflog 即.git/logs/refs/stash所记录下来

git log --graph --pretty=raw  refs/stash -2
# 同时保存暂存区的进度和工作区中的进度
# 进度保存的最新提交是一个合并提交 最新的提交说明中有WIP


git log --graph --pretty=raw  stash@{1} -3
# 用“原基线”代表进度保存时版本库的状态，即提交2b31c199；
# 用“原暂存区”代表进度保存时暂存区的状态，即提交4560d76；
# 用“原工作区”代表进度保存时工作区的状态，即提交6cec9db

git diff stash@{1}^2^ stash@{1}^2
# 原基线和原暂存区的差异比较

git diff stash@{1}^2 stash@{1}
# 原暂存区和原工作区的差异比较

git diff stash@{1}^1 stash@{1}
# 原基线和原工作区的差异比较

git stash apply stash@{1}
git stash list
git stash clear
ls -l .git/refs/stash .git/logs/refs/stash
# 删除进度列表之后，stash相关的引用和reflog也都不见了















