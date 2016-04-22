#! /bin/bash

for file in `find -iname "*.py"`;
do 
	diff <(head -n 17 LICENSE_ProgramFiles) <(head -n 17 $file) || `cat LICENSE_ProgramFiles | cat - $file > /tmp/out && mv /tmp/out $file`;
done
