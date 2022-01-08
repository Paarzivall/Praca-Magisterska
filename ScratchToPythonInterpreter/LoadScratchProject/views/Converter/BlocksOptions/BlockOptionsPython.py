val_of_blocks = {
        'event_whenflagclicked': {
            'code': 'if is_clicked():',
            'additional_code': ['def if_clicked():', '[Ciało funkcji - w tym wypadku powinno zwrócić "True" albo "False"]'],
            'style': '',
        },
        'data_setvariableto': {
            'code': 'var = val',
            'additional_code': None,
            'style': '',
        },
        'control_repeat_until': {
            'code': 'while',
            'additional_code': None,
            'style': '',
        },
        'motion_turnright': {
            'code': 'turn_right(',
            'additional_code': ['def turn_right(degree):', '[Ciało funkcji służącej do obracania stworka]'],
            'style': '',
        },
        'operator_gt': {
            'code': '[var] < [val]',
            'additional_code': None,
            'style': '',
        },
        'operator_lt': {
            'code': '[var] > [val]',
            'additional_code': None,
            'style': '',
        },
        'data_changevariableby': {
            'code': 'var = val',
            'additional_code': None,
            'style': '',
        },
        'data_showvariable': {
            'code': 'print',
            'additional_code': None,
            'style': '',
        },
        'control_if': {
            'code': 'if',
            'additional_code': None,
            'style': '',
        },
    }