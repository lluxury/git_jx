 
Git支持的协议


# Git提供了丰富的协议支持，包括：SSH、GIT、HTTP、HTTPS、FTP、FTPS、RSYNC及本地
ssh://[user@]example.com[:port]/path/to/repo.git/
[user@]example.com:path/to/repo.git/
git://example.com[:port]/path/to/repo.git/ # 只读协议
http[s]://example.com[:port]/path/to/repo.git/  
ftp[s]://example.com[:port]/path/to/repo.git/
RSYNC协议 rsync://example.com/path/to/repo.git/
file:///path/to/repo.git     
/path/to/repo.git

# 智能协议:两端打开程序交换, git-send-pack
# SSH、GIT及本地协议file://属于智能协议
# HTTP协议需要特殊的配置用git-http-backend配置CGI使用

# 哑协议
# 远程版本库不会运行辅助程序，而是完全依靠客户端去主动发现
# 需要要在版本库的钩子脚本post-update中设置运行git update-server-info

git clone git://git.kernel.org/pub/scm/git/git.git
git clone http://www.kernel.org/pub/scm/git/git.git
# HTTP(S)哑协议
git clone https://github.com/git/git.git
# HTTP(S)智能协议



多用户协同的本地模拟

git init --bare /path/to/repos/shared.git
cd /path/to/user1/workspace
git clone file:///path/to/repos/shared.git project

cd project
git config user.name user1
git config user.email user1@sun.ossxp.com


echo Hello. > README
git add README
git commit -m "initial commit."

git push origin master



cd /path/to/user2/workspace
git clone file:///path/to/repos/shared.git project

cd /path/to/user2/workspace/project
git config user.name user2
git config user.email user2@moon.ossxp.com

git log





强制非快进式推送

cd /path/to/user1/workspace/project/
mkdir team
echo "I'm user1." > team/user1.txt
git add team
git commit -m "user1's profile."

git push

git log --oneline --graph

cd /path/to/user2/workspace/project/
mkdir team
echo "I'm user1?" > team/user2.txt
git add team
git commit -m "user2's profile."

git push
# 快进式推送
# 要推送的本地版本库的提交是建立在远程版本库相应分支的现有提交基础上的
git rev-list HEAD
git ls-remote origin

git push -f

echo "I'm user2." > team/user2.txt
git diff

git add -u
git commit --amend -m "user2's profile."

git push -f
# 用来对历史提交进行修补,在别人下载之前




合并后推送

# 理性的工作协同要避免非快进式推送
# 向服务器推送后，发现错误，不要使用会更改历史的操作 变基 修补提交，
# 而是采用不会改变历史提交的反转提交等操作

cd /path/to/user1/workspace/project/
git push

git pull

git log --graph --oneline
git push




禁止非快进式推送

git --git-dir=/path/to/repos/shared.git config receive.denyNonFastForwards true
git reset --hard HEAD^1
git log --graph --oneline

git push -f

# 通过钩子脚本进行设置,Gitolite服务架设，通过授权文件用版本库的update钩子脚本实现