from .utils import execute_command


def parse_lines(lines):
    return {
        'total_lines': int(lines[0].split()[-2]),
        'total_cost': float(lines[1].split()[-1][1:].replace(',', '_')),
    }


def grep(cmd_result):
    selected_lines = []
    for line in cmd_result.split('\n'):
        if 'Total' in line or 'Estimated' in line:
            selected_lines.append(line)
    return parse_lines(selected_lines)


def sloccount(path, salary='65210', parser=grep):
    return parser(execute_command('scc {} --avg-wage {}'.format(path, salary)))
