#!/bin/sh

[ -f doc/B.txt ] && exit 1
exit 0

 # git bisect start master G
 # git bisect run sh good-or-bad.sh
 