import os
import re
from typing import TextIO

def get_version_map() -> dict[int, dict[int, str]]:
    files = os.listdir()
    version_map = {}
    pattern = re.compile(r'^spigot-1\.(\d{1,2})(?:\.(\d{1,2}))?.jar$')
    for file in files:
        version = pattern.match(file)
        if version is None:
            continue
        major = int(version.group(1))
        minor = int(version.group(2) or 0)
        if major in version_map:
            version_map[major][minor] = file
        else:
            version_map[major] = {minor: file}
    version_map = dict(sorted(version_map.items(), reverse=True))
    for version in version_map:
        version_map[version] = dict(sorted(version_map[version].items()))
    return version_map

def generate_table(versions: dict[int, dict[int, str]], repo: str, tag: str, file: TextIO) -> None:
    longest = max(len(versions[v]) for v in versions) if versions else 0

    file.write(f'| Version Family |')
    for _ in range(longest):
        file.write(' |')
    file.write('\n|:---:|')
    for _ in range(longest):
        file.write('---|')
    file.write('\n')

    for version in versions:
        file.write(f'| 1.{version} |')
        for minor in versions[version]:
            file.write(f' {generate_version_link(version, minor, repo, tag)} |')
        for _ in range(longest - len(versions[version])):
            file.write(' |')
        file.write('\n')

def generate_version_link(major: int, minor: int, repo: str, tag: str) -> str:
    version = '1.' + str(major)
    if minor != 0:
        version += '.' + str(minor)
    return f'[{version}](https://github.com/{repo}/releases/download/{tag}/spigot-{version}.jar)'

if __name__ == '__main__':
    repo = os.sys.argv[1]
    tag = os.sys.argv[2]
    versions = get_version_map()
    output = os.sys.argv[3]
    f = open(output, 'w')
    generate_table(versions, repo, tag, f)
    f.close()
