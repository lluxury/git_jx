
拉回操作中的合并

# git pull = git fetch + git merge
# 将远程的共享版本库的对象 提交、里程碑、分支等复制到本地

git merge <commit>
# 合并操作将<commit>对应的目录树和当前工作分支的目录树的内容进行合并，
# 合并后的提交以当前分支的提交作为第一个父提交


自动合并

# 修改不同的文件
git pull
git reset --hard origin/master

cd /path/to/user1/workspace/project/
echo "hack by user1 at `date -R`" >> team/user1.txt
git add -u
git commit -m "update team/user1.txt"
git push

cd /path/to/user2/workspace/project/
echo "hack by user2 at `date -R`" >> team/user2.txt
git add -u
git commit -m "update team/user2.txt"

git push

git fetch
git merge origin/master
git push

git log -3 --graph --stat



# 修改相同文件的不同区域
git pull

git add -u
git commit -m "User1 hack at the beginning."
git push

git add -u
git commit -m "User2 hack at the end."

git fetch

git merge refs/remotes/origin/master

git push

git blame README



# 同时更改文件名和文件内容
git pull
cd /path/to/user1/workspace/project/
mkdir doc
git mv README doc/README.txt
git commit -m "move document to doc/."
git push

cd /path/to/user2/workspace/project/
echo "User2 hacked again." >> README
git add -u
git commit -m "User2 hack README again."

git fetch

git merge refs/remotes/origin/master

git push

git log -1 -m --stat
# 使用-m参数可以查看合并操作所做出的修改





逻辑冲突
# 在项目中引入单元测试及自动化集成




冲突解决

git pull

git add -u
git commit -m "Say hello to user1."
git push

git add -u
git commit -m "Say hello to user2."

git pull

git status

# 文件.git/MERGE_HEAD记录所合并的提交ID
# 文件.git/MERGE_MSG记录合并失败的信息
# 文件.git/MERGE_MODE标识合并状态
git ls-files -s

# # 100644 a72ca0b4f2b9661d12d2a0c1456649fc074a38e3 1       team/user2.txt
# 当合并冲突发生后，会用到0以上的暂存区编号

git show :1:doc/README.txt
# 编号为1的暂存区保存冲突文件修改之前的副本，冲突双方共同的祖先版

git show :2:doc/README.txt
# 当前分支中修改的副本

git show :3:doc/README.txt
# 合并版本 分支 中修改的副本

cat doc/README.txt
# 编辑完毕后执行git add命令将文件添加到,再提交就完成了冲突解决
# 放弃合并操作 执行git reset将暂存区重置



# 打开文件doc/README.txt，将冲突标识符所标识的文字替换为
git add -u
git commit -m "Merge completed: say hello to all users."
git log --oneline --graph -3

# .git/MERGE_HEAD、.git/MERGE_MSG、.git/MERGE_MODE文件都自动删除
# 暂存区中的三个副本也都清除了


git reset --hard HEAD^
git status
git merge refs/remotes/origin/master

git mergetool
# 安装相关的工具软件，如：kdiff3、meld、tortoisemerge、araxis

git status
git ls-files -s
git commit -m "Say hello to all users."




树冲突

# 两人同时改名,树冲突
git pull
cd /path/to/user1/workspace/project
git mv doc/README.txt readme.txt
git commit -m "rename doc/README.txt to readme.txt"

git push

cd /path/to/user2/workspace/project
git mv doc/README.txt README
git commit -m "rename doc/README.txt to README"

git pull

git status

git ls-files -s
ls -l readme.txt README


git rm readme.txt
git rm doc/README.txt
git add README
#删除不要的,添加需要的

git ls-files -s
git commit -m "fixed tree conflict."
git log --oneline --graph -3 -m --stat




cd /path/to/user2/workspace/project
git reset --hard HEAD^
git clean -fd

git merge refs/remotes/origin/master
git status -s

git mergetool
# cd
git status -s
git commit -m "fixed tree conflict."
git push




合并相关的设置

merge.conflictstyle
merge.tool
git config --global merge.tool kdiff3

git config --global mergetool.kdiff3.path /path/to/kdiff3

git config --global merge.tool mykdiff3
git config --global mergetool.mykdiff3.cmd '/usr/bin/kdiff3
             -L1 "$MERGED (Base)" -L2 "$MERGED (Local)" -L3 "$MERGED (Remote)"
             --auto -o "$MERGED" "$BASE" "$LOCAL" "$REMOTE"'

merge.log