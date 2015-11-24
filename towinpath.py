#!/usr/bin/env python3

import os
import ntpath

NET_TYPE = 'net'
DISK_TYPE = 'disk'


def _split_path(path):
	path_list = []
	path_tuple = (path, '')
	while path_tuple[0]:
		path_list.append(path_tuple[1])
		path_tuple = os.path.split(path_tuple[0])
	path_list.append(path_tuple[1])
	path_list.reverse()
	return path_list


def to_windows_local(path, drive_letter=None):
	if drive_letter:
		drive_letter = drive_letter.strip(':\\')+':\\'
	return _to_windows_path(drive_letter, path)


def to_windows_net(path, domain=None):
	domain = '\\\\'+(domain or '')
	return _to_windows_path(domain, path)


def _to_windows_path(drive_letter, path):
	return ntpath.join(drive_letter or '', *_split_path(path))


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--net', default=False, action='store_true')
	parser.add_argument('--domain', default='')
	parser.add_argument('--drive', default='')
	parser.add_argument('path')
	args = parser.parse_args()
	if args.domain or args.net:
		print(to_windows_net(args.path, args.domain))
	else:
		print(to_windows_local(args.path, args.drive))
