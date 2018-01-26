def get_logs_from_file(file):
    with open(file, 'r') as f:
        r = f.read()
        lines = r.splitlines()

    result = ''
    for line in lines:
        result = result + str(line) + '\n'


    print('result: {}'.format(lines))
    return lines
