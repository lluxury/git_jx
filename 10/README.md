
cd /path/to/my/workspace/demo
git tag -m "Say bye-bye to all previous practice." old_practice
ls .git/refs/tags/old_practice
git rev-parse refs/tags/old_practice

git describe
# 显示当前版本库的最新提交的版本号,最近里程碑




删除文件
git status -s
git stash
git stash apply

git add detached-commit.txt
rm detached-commit.txt
git ls-files|grep deta
# 在工作区删除，对暂存区和版本库没有任何影响
git status


git rm detached-commit.txt
git status
git commit -m "delete trash files. (using: git rm)"
# 删除再提交, 确认删除

git ls-files --with-tree=HEAD^
# 历史版本中尚在的删除文件的内容



git reset --hard HEAD^
git stash apply -q
# 参数-q使得命令进入安静模式
git add detached-commit.txt
rm detached-commit.txt
git add -u
# 将被版本库追踪的本地文件的变更 修改、删除全部记录到暂存区中
git status -s
# 工作区删除的文件全部被标记为下次提交时删除
git commit -m "delete trash files. (using: git add -u)"
# 提交,删除


git cat-file -p HEAD~1:welcome.txt > welcome.txt
# 从历史中恢复文件技巧

git add -A
git status -s

git commit -m "restore file: welcome.txt"
# 通过再次添加的方式恢复被删除的文件, svn不建议用





移动文件
git mv welcome.txt README
git status
git commit -m "改名测试"
# 或
git reset --hard HEAD^
git status -s
git ls-files

mv welcome.txt README
git status -s
echo "Bye-Bye." >> README
git add -A
git status
git commit -m "README is from welcome.txt."





显示版本号
git describe
git log --oneline --decorate -4
# 显示版本号

# src/main.c
# src/version.h.in
# src/Makefile
# 动态版本号,获取git版本号并显示
cd src
make
./hello





选择性添加
cd /path/to/my/workspace/demo
ls src
# hello,main.o和version.h都是在编译时生成的程序，不应该加入到版本库中
git add -i
git status -s
git commit -m "Hello world initialized."




cd /path/to/my/workspace/demo/src
make clean && make
./hello
# 修改版本号显示
git tag -m "Set tag hello_1.0." hello_1.0
make clean && make
git status






文件忽略
cd /path/to/my/workspace/demo/src
git status -s
cat > .gitignore << EOF
> hello
> *.o
> *.h
> .gitignore  
> EOF
或
git status -s
git add .gitignore
git commit -m "ignore object files."

git mv .gitignore ..
git status
git commit -m "move .gitignore outside also works."

echo "/* test */" > hello.h
git status
git status --ignored -s
git add -f hello.h
# 只有在添加操作的命令行中明确的写入文件名，并且提供-f参数才能真正添加


# 忽略只对未跟踪文件有效，对于已加入版本库的文件无效
git commit -a -m "偷懒了，直接用 -a 参数直接提交。"


# .git/info/exclude来设置文件忽略
# 全局配置变量core.excludesfile指定的一个忽略文件

git config --global core.excludesfile /home/yann/_gitignore
git config core.excludesfile
cat /home/yann/_gitignore




文件归档
# 如果使用压缩工具tar、7zip、winzip、rar等将工作区文件归档，
# 一不小心会把版本库.git目录包含其中，甚至将工作区中的忽略文件、临时文件也包含其中

git archive -o latest.zip HEAD
基于最新提交建立归档文件latest.zip

git archive -o partial.tar  HEAD src doc
# 只将目录src和doc建立到归档partial.tar中

git archive --format=tar --prefix=1.0/ v1.0 | gzip > foo-1.0.tar.gz
# 基于里程碑v1.0建立归档，并且为归档中文件添加目录前缀1.0
# 没有前缀的话,解压会在当前目录,既先建目录,再解压

git get-tar-commit-id
#用途未知