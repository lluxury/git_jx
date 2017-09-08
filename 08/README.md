# 重置命名实际上所针对的是头指针HEAD

# HEAD可以理解为“头指针”，是当前工作区的“基础版本”，
# 当执行提交时，HEAD指向的提交将作为新提交的父提交

cat .git/HEAD
git branch -v

git checkout 4902dc3^
# 检出该ID的父提交
cat .git/HEAD
# 分离头指针状态指的就是HEAD头指针指向了一个具体的提交ID，而不是一个引用分支

git reflog -1
git rev-parse HEAD master
# master没变,HEAD变了
# git checkout命令并不像git reset命令，分支master的指向并没有改变，仍旧指向原有的提交ID


# 测试分离状态下的提交文件
touch detached-commit.txt
git add detached-commit.txt
git status
git commit -m "commit in detached HEAD mode."
cat .git/HEAD
git log --graph --pretty=oneline
# 记录提交的id 9df1c18
git checkout master
cat .git/HEAD
ls
# 切换之后，之前本地建立的新文件detached-commit.txt不见了
# 刚才的提交日志也不见了

git log --graph --pretty=oneline
git show 9df1c18
# 提交现在仍在版本库中, 但是不在分支
# 当reflog中含有该提交的日志过期后，这个提交随时都会从版本库中彻底清除





挽救分离头指针
# 使用git reset可以将master分支重置到该测试提交acc2f69，但是会丢掉master分支原先的提交4902dc3
# 将提交acc2f69合并到master分支
git branch -v
git merge acc2f69
# 自动融合的冲突会以最后一次提交为准,checkout还原的文件也视为一次提交

git log --graph --pretty=oneline
git cat-file -p HEAD


深入了解git checkout命令
git checkout -- paths
# 默认从暂存区（index）进行检出
# 包含了路径<paths>不会改变HEAD头指针，主要是用于指定版本的文件覆盖对应的文件
# 如果省略<commit>，会拿暂存区的文件覆盖工作区的文件，
# 否则用指定提交中的文件覆盖暂存区和工作区中对应的文件

git checkout branch
# 切换分支, 无branch只执行状态检查
# 只有HEAD切换到一个分支才可以对提交进行跟踪，否则会进入“分离头指针”的状态
# 在“分离头指针”状态下的提交不能被引用关联到而可能会丢失

git checkout -b new_branch
# 创建和切换到新的分支，新的分支从<start_point>指定的提交开始创建




git checkout branch
# 检出branch分支 更新HEAD以指向branch分支，以branch指向的树更新暂存区和工作区

git checkout
git checkout HEAD
# 汇总显示工作区、暂存区与HEAD的差异

git checkout – filename
# 用暂存区中filename文件来覆盖工作区中的filename文件
# 取消自上次执行git add filename以来本地的修改, 无提示无法还原

git checkout branch –- filename
# HEAD的指向不变 将branch所指向的提交中的filename替换暂存区和工作区中相应的文件
# 暂存区和工作区中的filename文件直接覆盖

git checkout – . 
git checkout .
# 会取消所有本地的修改,暂存区的所有文件直接覆盖本地文件

