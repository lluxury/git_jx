 

cd /path/to/my/workspace/
git clone git://github.com/ossxp-com/gitdemo-commit-tree.git i-am-admin

cd /path/to/my/workspace/i-am-admin
git show-ref
# 看看所含的引用

# 以refs/heads/开头的是分支
# 以refs/remotes/开头的是远程版本库分支在本地的映射
# 以refs/tags/开头的是里程碑

find .git/refs/ -type f
git pack-refs --all
find .git/refs/ -type f
# 文件被打包了，放到.git/packed-refs中,文本文件

head -5 .git/packed-refs

find .git/objects/ -type f
# 以.pack结尾的文件是打包文件，以.idx结尾的是索引文件
# 保存于.git/objects/pack/目录下
# 松散对象打包后会提高访问效率

git show-index < .git/objects/pack/pack-*.idx | head -5





暂存区操作引入的临时对象

cp /boot/initrd.img-2.6.32-5-amd64 /tmp/bigfile
du -sh bigfile

cd /path/to/my/workspace/i-am-admin
cp /tmp/bigfile bigfile
cp /tmp/bigfile bigfile.dup

git add bigfile bigfile.dup
du -sh .

du -sh .git/
find .git/objects/ -type f

git status -s
git reset HEAD
git status -s

du -sh .git/
git fsck

git prune
git fsck
du -sh .git/
# 对象库中产生临时对象占用磁盘空间,清理演示

git clean -nd
# 一个清理版本库,一个清理工作区





重置操作引入的对象

cd /path/to/my/workspace/i-am-admin
cp /tmp/bigfile bigfile
cp /tmp/bigfile bigfile.dup

git add bigfile bigfile.dup
git commit -m "add bigfiles."
du -sh .git/
git reset --hard HEAD^
find .git/objects/ -type f
git cat-file -t 1160e9
# commit
git cat-file -t 397920
# tree
git cat-file -t 6256e4
# blob

git prune
git fsck
git fsck --no-reflogs

git reflog
# Git认为撤销的提交和大文件都还被可以被追踪到，无法用git prune命令删除

git reflog expire --all
git reflog
# 对版本库的reflog做过期操作，相当于将.git/logs/下的文件清空
# 缺省只会让90天前的数据过期

git reflog expire --expire=now --all
git reflog
# 没有了 reflog,该提交对应的 commit tree和 blob 成为dangling 对象

git prune
du -sh .git/






 Git管家

 # 实际操作中会很少用到git prune命令来清理版本库
cp /tmp/bigfile bigfile
cp /tmp/bigfile bigfile.dup
echo "hello world" >> bigfile.dup

git add bigfile bigfile.dup
git commit -m "add bigfiles."

git ls-tree HEAD | grep bigfile
git reset --hard HEAD^

du -sh .git/
find .git/objects -type f -printf "%-20p\t%s\n"
# 输出的每一行用空白分隔，前面是文件名，后面是以字节为单位的文件大小

git gc
du -sh .git/
find .git/objects -type f -printf "%-20p\t%s\n" | sort

git reflog expire --expire=now --all
git fsck
git show c3e748

git gc
du -sh .git/
git gc --prune=now

du -sh .git/


