import os


def create_1m_file():
    n = 0
    if not os.path.isdir("folder"):
        os.mkdir("folder")
    os.chdir("folder")
    dir_with_files = os.getcwd()
    while n < 5000000:
        with open(dir_with_files + '/' + str(n), 'w') as f:
            pass
        n += 1
        if n % 1000 == 0:
            print(n)


if __name__ == '__main__':
    create_1m_file()
