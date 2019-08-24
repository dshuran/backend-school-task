import os


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    os.mkdir(os.path.join(path, 'post_requests'))
    os.mkdir(os.path.join(path, 'post_requests', 'input'))
    os.mkdir(os.path.join(path, 'post_requests', 'output'))
    os.mkdir(os.path.join(path, 'patch_requests'))
    os.mkdir(os.path.join(path, 'patch_requests', 'input'))
    os.mkdir(os.path.join(path, 'patch_requests', 'output'))
    os.mkdir(os.path.join(path, 'get_full_requests'))
    os.mkdir(os.path.join(path, 'get_full_requests', 'input'))
    os.mkdir(os.path.join(path, 'get_full_requests', 'output'))


if __name__ == '__main__':
    main()
