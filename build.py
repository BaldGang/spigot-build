import os
import sys
import yaml

def build(version):
    os.system("java -Xmx6G -Xms6G -jar BuildTools.jar --rev %s --output-dir output --disable-java-check" % version)

if __name__ == '__main__':
    with open('version.yml', 'r') as f:
        config = yaml.safe_load(f)
    for version in config[sys.argv[1]]:
        build(version)