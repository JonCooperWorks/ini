"""Simple INI file parser."""

import json
import re
import sys

section_regex = re.compile('^\[(.*)\]$')
property_regex = re.compile('^([^=]+)=(.*)$')

COMMENT_CHARS = ';', '#'


class INISyntaxError(Exception):
    def __init__(self, num, line):
        self.num = num
        self.line = line


def parse(source):
    section = ''
    ini_file = {section: {}}
    lines = map(lambda s: s.strip(), source.split('\n'))

    for number, line in enumerate(lines):
        # Ignore empty lines and comments
        if len(line) == 0 or line[0] in COMMENT_CHARS:
            continue

        property_match = property_regex.match(line)
        section_match = section_regex.match(line)

        if property_match is not None:
            key, value = map(lambda s: s.strip(), property_match.groups())
            ini_file[section][key] = value

        elif section_match is not None:
            section = section_match.group(1).strip()

            if not section in ini_file:
                ini_file[section] = {}

        else:
            raise INISyntaxError(number, line)

    return ini_file


def to_json(source):
    return json.dumps(parse(source))


if __name__ == '__main__':
    _, ini_filename, json_filename = sys.argv

    with open(ini_filename) as ini_file, open(json_filename, 'w') as json_file:
        try:
            json_file.write(to_json(ini_file.read()))

        except INISyntaxError as e:
            print('Syntax Error on line {0}: {1}'.format(e.num, e.line))

        except IOError as e:
            print('IOError: {1}'.format(e))
