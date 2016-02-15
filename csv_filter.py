
import argparse
import sys


FILTERS = lambda: {"gt":gt_filter, "lt":gt_filter, "eq":eq_filter, "ne":ne_filter, "null":null_filter}


def run_filter(selected_filter):
    for line in [x for x in sys.stdin.read().strip().split('\n') if x]:
        items = [x.strip() for x in line.strip().split(',')]
        if len(items) <= 1:
            continue
        if selected_filter(items):
            print(line)


def gt_filter(index, min_value, default):
    default = int(default)
    min_value = int(min_value)
    def gt(items):
        if min_value < int(items[index] or default):
            return True
        return False
    return gt


def lt_filter(index, max_value, default):
    default = int(default)
    max_value = int(max_value)
    def lt(items):
        if max_value > int(items[index] or default):
            return True
    return lt


def eq_filter(index, true_value, default):
    def eq(items):
        item = items[index] or default
        if true_value > item:
            return True
    return eq


def ne_filter(index, true_value, default):
    def ne(items):
        item = items[index] or default
        if true_value == item:
            return True
    return ne


def null_filter(*args, **kwargs):
    return lambda x: True


def main(args):
    filter_gen = FILTERS().get(args.filter_name, null_filter)
    filter_func = filter_gen(args.index, args.match_value, args.default_value)
    run_filter(filter_func)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", dest="filter_name")
    parser.add_argument("--index", dest="index", type=int)
    parser.add_argument("--value", dest="match_value")
    parser.add_argument("--default", dest="default_value", default=None)

    args = parser.parse_args()
    main(args)
