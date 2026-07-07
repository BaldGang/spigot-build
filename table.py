import os
import re
from collections import defaultdict
from typing import TextIO

def get_version_map() -> dict[str, list[str]]:
    files = os.listdir()
    version_map = defaultdict(list)
    pattern = re.compile(r'^spigot-(\d+(?:\.\d+)+)\.jar$')
    for file in files:
        match = pattern.match(file)
        if match is None:
            continue
        version = match.group(1)
        parts = version.split('.')
        if parts[0] == '1':  # 1.x.y => 1.x (e.g. 1.21.8)
            family = '.'.join(parts[:2])
        else:  # x.y => x (e.g. 26.1.2)
            family = parts[0]
        version_map[family].append(version)
    version_map = dict(sorted(
        version_map.items(),
        key=lambda item: tuple(int(p) for p in item[0].split('.')),
        reverse=True,
    ))
    for family in version_map:
        version_map[family] = sorted(
            version_map[family],
            key=lambda version: tuple(int(p) for p in version.split('.')),
        )
    return version_map

def generate_table(versions: dict[str, list[str]], repo: str, tag: str, file: TextIO) -> None:
    longest = max((len(versions[v]) for v in versions), default=0)

    file.write(f'| Version Family |')
    for _ in range(longest):
        file.write(' |')
    file.write('\n|:---:|')
    for _ in range(longest):
        file.write('---|')
    file.write('\n')

    for family in versions:
        file.write(f'| {family} |')
        for version in versions[family]:
            file.write(f' {generate_version_link(version, repo, tag)} |')
        for _ in range(longest - len(versions[family])):
            file.write(' |')
        file.write('\n')

def generate_version_link(version: str, repo: str, tag: str) -> str:
    return f'[{version}](https://github.com/{repo}/releases/download/{tag}/spigot-{version}.jar)'

if __name__ == '__main__':
    repo = os.sys.argv[1]
    tag = os.sys.argv[2]
    versions = get_version_map()
    output = os.sys.argv[3]
    f = open(output, 'w')
    generate_table(versions, repo, tag, f)
    f.close()
