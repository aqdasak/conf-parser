from io import TextIOWrapper


def load(f: TextIOWrapper) -> dict:
    return loads(f.read())


def loads(s: str) -> dict:
    config = {}
    section = config
    for i, line in enumerate(s.split('\n')):
        line = line.strip()

        # Empty line
        if len(line) == 0:
            section[f'meta{i}'] = ''

        # E.g
        # Comment
        elif line[0] == '#':
            section[f'meta{i}'] = line

        # E.g.
        # [section_heading]
        elif line[0] == '[' and line[-1] == ']':
            section = {}
            config.update({line[1:-1]: section})

        # E.g.
        # [section_heading] # Inline comment
        elif (lambda x: x[0] == '[' and x[-1] == ']')(line.split('#', maxsplit=1)[0].strip()):
            line, comment = line.split('#', maxsplit=1)
            section = {f'inline_comment{i}': '#'+comment}
            config.update({line.strip()[1:-1]: section})

        # E.g.
        # variable = value
        # elif '=' in line:
        #     # print(f'${line}$')
        #     line = line.split('=')
        #     # print(line)
        #     section.update(dict([(line[0].strip(), line[1].strip())]))

        # E.g.
        # variable = value # Inline comment
        elif (lambda x: '=' in x)(line.split('#', maxsplit=1)[0].strip()):
            line = line.split('#', maxsplit=1)
            if len(line) == 1:
                key, value = line[0].split('=', maxsplit=1)
                section.update(dict([(key.strip(), value.strip())]))

            else:
                line, comment = line
                key, value = line.split('=', maxsplit=1)
                section.update(dict([(key.strip(), value.strip())]))
                section.update({f'inline_comment{i}': '#'+comment})

        # Invalid cases
        else:
            section.update(dict([(f'meta{i}', line)]))

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
            elif k.startswith('inline_comment'):
                # print(config_str)
                # input()
                config_str = config_str[:-1] + ' ' + v
            else:
                config_str += f'{k} = {v}'

        config_str += '\n'

    return config_str[:-1]
