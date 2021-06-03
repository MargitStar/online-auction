import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='Add host, user_file and config_file')
    parser.add_argument('--url', metavar='u', type=str,
                        help='url')
    parser.add_argument('--user_file', metavar='f', type=str,
                        help='user_file')
    parser.add_argument('--config_file', metavar='c', type=str,
                        help='config_file')
    return parser.parse_args()
