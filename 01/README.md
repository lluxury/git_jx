git 歌易特

# 比较差异
diff -u hello world >diff.txt

# 反向操作
cp hello world
patch world < diff.txt
或
cp world hello
patch -R hello < diff.txt

