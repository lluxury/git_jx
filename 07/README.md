cat .git/refs/heads/master
git log --graph --oneline
# --pretty=oneline --abbrev-commit

touch new-commit.txt
git add new-commit.txt
git commit -m "does master follow this new commit?"

# new-commit.txt  welcome.txt

cat .git/refs/heads/master
git log --graph --oneline
git reset --hard HEAD^
#上一次提交
cat .git/refs/heads/master

# welcome.txt

git log --graph --oneline
git reset --hard 9e8a761
# cat welcome.txt  最初提交, 日志也消失


git config core.logallrefupdates
tail -5 .git/logs/refs/heads/master
# reflog
git reflog show master | head -5
git reset --hard master@{2}
# 提交恢复,但未提交修改消失
git log --oneline
git reflog show master | head -5



git reset –hard
# 替换引用指向,替换暂存区,替换工作区

git reset –soft
# 替换引用指向,不改变暂存区,工作区

git reset 
git reset HEAD
# git reset  –mixed
# 替换引用指向,替换暂存区,不改变工作区

git reset – filename
# git reset HEAD filename
# 相当于对命令git add filename的反向操作


git reset –soft HEAD^
# 工作区和暂存区不改变，但是引用向前回退一次。撤销最新的提交以便重新提交


# git commit –amend相当于
git reset --soft HEAD^
git commit -e -F .git/COMMIT_EDITMSG
# .git/COMMIT_EDITMSG保存了上次的提交日志?


git reset HEAD^
git reset –mixed HEAD^
# 工作区不改变，但是暂存区会回退到上一次提交之前，引用也会回退一次
# 不知道哪里会用到

git reset –hard HEAD^
# 自上一次以来的提交全部丢失








