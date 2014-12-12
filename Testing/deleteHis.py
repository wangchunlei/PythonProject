#!/usr/bin/env python
import os, shutil

folders = sorted([o for o in os.listdir('.') if os.path.isdir(o)],reverse=True)
for idx, val in enumerate(folders):
	if idx >= 4:
		print "Delete:",val
		shutil.rmtree(val)

