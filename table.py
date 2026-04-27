import os
import re
from typing import TextIO

def get_version_map() -> dict[str, dict[int, str]]:
    files = os.listdir()
    version_map = {}
    pattern = re.compile(r'^spigot-(\d+\.\d+)(?:\.(\d+))?\.jar$')
    for file in files:
        version = pattern.match(file)
        if version is None:
            continue
        family = version.group(1)
        patch = int(version.group(2) or 0)
        if family in version_map:
            version_map[family][patch] = file
        else:
            version_map[family] = {patch: file}
    version_map = dict(sorted(
        version_map.items(),
        key=lambda item: tuple(int(p) for p in item[0].split('.')),
        reverse=True,
    ))
    for family in version_map:
        version_map[family] = dict(sorted(version_map[family].items()))
    return version_map

def generate_table(versions: dict[str, dict[int, str]], repo: str, tag: str, file: TextIO) -> None:
    longest = max(len(versions[v]) for v in versions) if versions else 0

    file.write(f'| Version Family |')
    for _ in range(longest):
        file.write(' |')
    file.write('\n|:---:|')
    for _ in range(longest):
        file.write('---|')
    file.write('\n')

    for family in versions:
        file.write(f'| {family} |')
        for patch in versions[family]:
            file.write(f' {generate_version_link(family, patch, repo, tag)} |')
        for _ in range(longest - len(versions[family])):
            file.write(' |')
        file.write('\n')

def generate_version_link(family: str, patch: int, repo: str, tag: str) -> str:
    version = family
    if patch != 0:
        version += '.' + str(patch)
    return f'[{version}](https://github.com/{repo}/releases/download/{tag}/spigot-{version}.jar)'

if __name__ == '__main__':
    repo = os.sys.argv[1]
    tag = os.sys.argv[2]
    versions = get_version_map()
    output = os.sys.argv[3]
    f = open(output, 'w')
    generate_table(versions, repo, tag, f)
    f.close()
