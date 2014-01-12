from ini import INISyntaxError, parse, to_json

if __name__ == '__main__':
    source = """
key=value
key1 = value1

[section1]
key1=value1
; Comments
; key3=value3
key2=this=works right?
"""

    expected = {
        '': {
            'key': 'value',
            'key1': 'value1',
        },

        'section1': {
            'key1': 'value1',
            'key2': 'this=works right?',
        },
    }

    try:
        actual = parse(source)

    except INISyntaxError as e:
        print('Syntax Error on line {0}, {1}'.format(e.num, e.line))

    else:
        assert expected == actual, ('Expected {0}, got {1}'
                                    .format(expected, actual))

    syntax_error = """
this should give an error.
    """

    try:
        actual = parse(syntax_error)

    except INISyntaxError as e:
        assert e.num == 1 and e.line == 'this should give an error.'

    else:
        raise Exception('That should have given an error')

    print('Tests passed!')
    print(to_json(source))
