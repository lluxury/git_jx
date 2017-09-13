 
cd /path/to/my/workspace/demo
git log --stat -2

git commit --amend -m "Remove hello.h, which is useless."
git log --stat -2
# 修改说明

git checkout HEAD^ -- src/hello.h
git status
git commit --amend -m "commit with --amend test."
git log --stat -2
# 取消删除,修改说明,注意--两边都有空格



多步悔棋
git log --stat --pretty=oneline -3
git reset --soft HEAD^^
#最新为HEAD,再往前数2个,再下一个
#到回去为add状态,因为暂存区存在
git status
git commit -m "modify hello.h"
# 多个提交合并为一个,最后的修改会覆盖前面的,快速合并?
git log --stat --pretty=oneline -2




回到未来

# 方式一
git tag F
git tag E HEAD^
git tag D HEAD^^
git tag C HEAD^^^
git tag B HEAD~4
git tag A HEAD~5
#练习环境

git log --oneline --decorate -6
git checkout C
# 将HEAD头指针切换到C,指针分离

git cherry-pick master^
# master还是指在最前面f,master^就是下面的一个e
git cherry-pick master
git log --oneline --decorate -6
#检出完毕,D已近不存在

git log --pretty=fuller --decorate -2
# 创作提交日期不同,所以SHA1值也变了

git checkout master
git reset --hard HEAD@{1}
# 切回master,HEAD指向新提交
# HEAD@{1}相当于切换回master分支前的HEAD指向

git checkout master
git reset --hard F
git log --oneline --decorate -6
# 还原测试环境

git checkout D
# HEAD在D
git reset --soft HEAD^^
# 融合,捡出,毁棋2次,HEAD在B
git commit -C C
git cherry-pick E
git cherry-pick F
git log --oneline --decorate -6
# 提交内容还在,SHA1变了,tag丢失
git checkout master
git reset --hard HEAD@{1}

git checkout master
git reset --hard F




# 方式二
# git rebase  --onto  <newbase>  <since>  <till>
# git rebase --onto C E^ F
# 将E和F提交跳过提价D，“嫁接”到C提交上
# <since>..<till>, 等价与 E^,F, 排除点E及之前,到F集合,嫁接到C

# git rebase --onto C D
# E^等价于D，并且F和当前HEAD指向相同省略

git status -s -b
git log --oneline --decorate -6


git rebase --onto C E^ F
git checkout master
git reset --hard HEAD@{1}

git log --oneline --decorate -6
# F是一个里程碑指向一个提交，而非master
# 会导致后面变基完成还需要对master分支执行重置

git checkout master
git reset --hard F


git checkout D
git reset --soft HEAD^^
git commit -C C
git tag newbase
git rev-parse newbase
git rebase --onto newbase E^ master
# 使用分支master。变基操作会直接修改master分支，无须重置

git log --oneline --decorate -6
git branch
git tag -d newbase
# tag不受版本影响?

git checkout master
git reset --hard F



# 方式三
# 交互式变基操作，会将<since>..<till>的提交悉数罗列在一个文件中，
# 然后自动打开一个编辑器来编辑这个文件。通过修改文件内容完成多项操作

git status -s -b
git log --oneline --decorate -6

git rebase -i D^
    pick 0f025e5 Change right flag 'init' to 'admin' and update the document.
    pick aa7f90d Handle user's key in gitolite way. user@host.pub = user.pub, but != user@ossxp.com.pub.
    pick 7496bc0 Also handle user's key in gitolite way when install gitosis.
# 删除第一行,保存退出,变基自动开始，即刻完成

git log --oneline --decorate -6


git checkout master
git reset --hard F


git rebase -i C^
# 因为要将C和D压缩为一个，因此变基从C的父提交
pick -> squash
# 将动作由pick修改为squash
git log --oneline --decorate -6
git cat-file -p HEAD^^




丢弃历史
# 抛弃部分早期历史提交的精简版本
# 只保留最近的100次提交
git log --oneline --decorate
git cat-file -p A^{tree}
# 查看里程碑A指向的目录树
echo "Commit from tree of tag A." | git commit-tree A^{tree}
# 使用git commit-tree命令直接从该目录树创建提交
git log 1c24ffeb
# 这个提交没有历史提交，孤儿提交
git rebase --onto 1c24ffeb A master
# 执行变基，将master分支从里程碑到最新的提交全部迁移到孤儿提交
git log --oneline --decorate



反转提交
# 更改历史操作只能是针对自己的版本库，而无法去修改他人的版本库
git show HEAD
git revert HEAD
# 在不改变这个提交的前提下对其修改进行撤销
# 将HEAD提交反向再提交一次，在提交说明编辑状态下暂停
# 修改提交说明，撤销提交,进行反向操作并提交
git log --stat -2



