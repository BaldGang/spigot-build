import os
import re

def get_version_map():
    files = os.listdir()
    version_map = {}
    for file in files:
        version = re.match(r'^spigot-1\.(\d{1,2})(?:\.(\d))?.jar$', file)
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

def generate_table(versions, tag):
    longest = 0
    for version in versions:
        length = len(versions[version])
        if length > longest:
            longest = length

    print('|Version Family|', end='')
    for _ in range(longest):
        print(' |', end='')
    print('\n|:---:|', end='')
    for _ in range(longest):
        print('---|', end='')
    print()

    for version in versions:
        print('|', version, '|', end='')
        for minor in versions[version]:
            print('', generate_version_link(version, minor, tag), '|', end='')
        for _ in range(longest - len(versions[version])):
            print(' |', end='')
        print()

def generate_version_link(major, minor, tag):
    version = '1.' + str(major)
    if minor != 0:
        version += '.' + str(minor)
    return f'[{version}](https://github.com/BaldGang/spigot-build/releases/download/{tag}/spigot-{version}.jar)'

if __name__ == '__main__':
    tag = os.sys.argv[1]
    versions = get_version_map()
    generate_table(versions, tag)
