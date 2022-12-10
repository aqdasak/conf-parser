from io import TextIOWrapper


def load(f: TextIOWrapper) -> dict:
    return loads(f.read())


def loads(s: str) -> dict:
    config = {}
    section = config
    i = 0
    for line in s.split('\n'):
        line = line.strip()

        if len(line) == 0:
            section[f'meta{i}'] = ''
            i += 1

        elif line[0] == '#':
            section[f'meta{i}'] = line
            i += 1

        elif line[0] == '[' and line[-1] == ']':
            section = {}
            config.update({line[1:-1]: section})

        elif '=' in line:
            # print(f'${line}$')
            line = line.split('=')
            # print(line)
            section.update(dict([(line[0].strip(), line[1].strip())]))

        else:
            section.update(dict([(f'meta{i}', line)]))
            i += 1

    return config


def dump(config: dict[str:str], f: TextIOWrapper) -> None:
    f.write(dumps(config))


def dumps(config: dict[str:str]) -> str:
    return __dumps(config)+'\n'


def __dumps(config: dict[str:str]) -> str:
    config_str = ''
    for k, v in config.items():
        if type(v) == dict:
            config_str += f'[{k}]\n{__dumps(v)}'
        else:
            # print(v.encode())
            if k.startswith('meta'):
                config_str += v
            else:
                config_str += f'{k} = {v}'

        config_str += '\n'

    return config_str[:-1]
