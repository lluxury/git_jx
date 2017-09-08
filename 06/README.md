git log -1 --pretty=raw

git cat-file -t e695606
# commit
git cat-file -t f58d
# tree
git cat-file -t a0c6
# commit
# 查看类型

git cat-file -p e695606
# 查看内容

git cat-file -t fd3c0
git cat-file -p fd3c0
#查看blob对象的内容

for id in e695606 f58da9a a0c641e fd3c069; do \
  ls .git/objects/${id:0:2}/${id:2}*; done
  #对象在库中的实际位置


# 提交跟踪链
git log --pretty=raw --graph e695606


# HEAD和master

git status -s -b
git branch
#状态,分支


git log -1 HEAD
git log -1 master
git log -1 refs/heads/master
# HEAD、master和refs/heads/master具有相同的指向


find .git -name HEAD -o -name master
# .git/HEAD
#   .git/logs/HEAD
#   .git/logs/refs/heads/master
#   .git/logs/refs/remotes/origin/HEAD
# .git/refs/heads/master
# .git/refs/remotes/origin/HEAD

cat .git/HEAD
# refs/heads/master

cat .git/refs/heads/master
git cat-file -t 89a987
git cat-file -p 89a987
# master指向的是最新提交



# 目录.git/refs是保存引用的命名空间，
# .git/refs/heads目录下的引用又称为分支

git rev-parse master
git rev-parse refs/heads/master
git rev-parse HEAD
# git rev-parse 显示引用对应的提交ID,3个都一样



SHA1哈希值
echo -n Git |sha1sum

# HEAD对应的提交的内容
git cat-file commit HEAD
git cat-file commit HEAD | wc -c
# 在提交信息的前面加上内容commit 234<null>（<null>为空字符），然后执行SHA1哈希算法
( printf "commit 234\000"; git cat-file commit HEAD ) | sha1sum
git rev-parse HEAD


# 文件内容的SHA1哈希值生成方法
git cat-file blob HEAD:welcome.txt
git cat-file blob HEAD:welcome.txt | wc -c
# 在文件内容的前面加上blob 25<null>的内容，然后执行SHA1哈希算法
( printf "blob 25\000"; git cat-file blob HEAD:welcome.txt ) | sha1sum
git rev-parse HEAD:welcome.txt


# 树的SHA1哈希值的形成方法
git cat-file tree HEAD^{tree} | wc -c
# 在树的内容的前面加上tree 39<null>的内容，然后执行SHA1哈希算法
( printf "tree 39\000"; git cat-file tree HEAD^{tree} ) | sha1sum
git rev-parse HEAD^{tree}



哈希值的访问方法
# HEAD^^
# a573106^2
# HEAD^1相当于HEAD^
# a573106~5
# a573106^^^^^
# a573106^{tree}    提交的树对象
# a573106:path/to/file   提交的文件对象
# :path/to/file    暂存区的文件对象

git rev-parse HEAD
git cat-file -p e695
git cat-file -p e695^
git rev-parse e695^{tree}
git rev-parse e695^^{tree}