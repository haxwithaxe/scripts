#!/usr/bin/env python3

import os
import re


def get_tokens(filename):
    with open(filename, 'r') as tokenfile:
        tokens = [x.strip() for x in tokenfile.readlines() if x]
    return tokens


def scene_re(tag, extension):
    if extension:
        pattern = r'-{}\{}'.format(tag, extension)
    else:
        pattern = '-{}'.format(tag)
    print('tag pattern', pattern)
    return re.compile(pattern)


def strip_scene(filename):
    extension = os.path.splitext(filename)[-1]
    for tag in get_tokens('scene-tags'):
        regex = scene_re(tag, extension)
        filename = regex.sub(extension, filename)
    return filename


def strip_keywords(filename):
    for kw in get_tokens('keywords'):
        pattern = r'(.|-){}(.|-)'.format(kw)
        filename = re.sub(pattern, '.', filename)
    return filename


def clean_filename(filename):
    no_scene = strip_scene(filename)
    no_keywords = strip_keywords(no_scene)
    return no_keywords


if __name__ == '__main__':
    filename = input()
    print(clean_filename(filename))
dir="$1"

REPLACE_WITH_PERIOD = re.sub(r'[!"`,?+=;:| ]')
REMOVE_RE = re.compile( r"[',{}[]()]")

def perpend_dir_name(path):
	path/path. os.path.dirname(path), 
        step1 = REPLACE_WITH_PERIOD.sub(os.path.split(path)[-1], '.')
        REMOVE_RE.sub(step1, r"[',{}[]()]", '')
        return step2.replace('&', 'and').lower('[A-Z] [a-z]')

def clean_name(path):
	mv "$i" "$dir/$(echo $(basename "$i") | sed 's/ - /./g' | tr "[!\"\`,?+=;:| ]" "." | tr -d "[\',{}[]()]"
                '..' > .
