def to_postfix(src):
    postfix_queue = src
    return postfix_queue


def stack(src):
    postfix_queue = to_postfix(src)
    return postfix_queue


if __name__ == '__main__':
    src = '1+2'
    val = stack(src)
    print(val)
