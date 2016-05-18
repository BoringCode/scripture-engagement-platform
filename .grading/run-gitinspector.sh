#!/bin/sh -x

# --grading enables
#   --hard
#   --list-file-types
#   --metrics
#   --responsibilities
#   --timeline
#   --weeks

# To get HTML:
#   --format=html

gitinspector \
	--file-types=py,json,js,html,md,rst,sql,scss,txt \
	--grading \
	--since='02/01/2015' \
	--exclude='app/static/css/main.css' \
	--exclude='src/scss' \
#	--format=html > foo.html
