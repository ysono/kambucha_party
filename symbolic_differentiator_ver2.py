from typing import Iterator, Tuple

def parse(s: str, varsym: str)-> Iterator[Tuple[int, int]]:
    '''
    num := [+- ]*\d+
    term_sfx := <varsym>(\^<num>)?
    term := (<num>|<term_sfx>|<num><term_sfx>)
    '''

    n = len(s)
    i = 0

    def num():
        nonlocal i

        sign = 1
        while i < n:
            if s[i].isspace() or s[i] == '+':
                pass
            elif s[i] == '-':
                sign *= -1
            else:
                break
            i += 1

        if i == n:
            return None

        i0 = i
        while i < n and s[i].isdigit():
            i += 1
        if i0 == i:
            val = 1
        else:
            val = int(s[i0:i])

        return sign * val

    def term():
        nonlocal i

        coeff = num()
        if coeff is None:
            return

        while i < n and s[i].isspace():
            i += 1
        deg = 0
        if i < n and s[i] == varsym:
            deg = 1

            i += 1
            while i < n and s[i].isspace():
                i += 1

            if i < n and s[i] == '^':
                i += 1
                deg = num()
        
        yield (coeff, deg)

    while i < n:
        yield from term()

def diff(s: str, varsym: str) -> str:
    items = []
    for coeff, deg in parse(s, varsym):
        coeff *= deg
        deg -= 1

        if coeff != 0:
            sign = '+' if coeff > 0 else '-'

            pfx = str(abs(coeff))
        
            if deg == 0:
                sfx = ''
            elif deg == 1:
                sfx = varsym
            else:
                sfx = f'{varsym}^{deg}'
        
            items += (sign, pfx + sfx)
    
    if items and items[0] == '+':
        return ' '.join(items[1:])
    return ' '.join(items)

def __test():
    samples = [
        ("3 + 1x + 2x^2", 'x', "1 + 4x"),
        ("3 + x-2x^2", 'x', "1 - 4x"),
        ("17 x + 1x^2", 'x', "17 + 2x"),
        ("1 + 2x + -3x^ 2 + 17x^17 + -1x^107", 'x', "2 - 6x + 289x^16 - 107x^106"),
        ("1 + 2x + - 3 x ^ - 2 + 17x^17 + - 1 x ^ + 107", 'x', "2 + 6x^-3 + 289x^16 - 107x^106"),
        ('1+2y+-3y^-2+17y^17+-1y^+107', 'y', "2 + 6y^-3 + 289y^16 - 107y^106"),
    ]
    for input, varsym, exp in samples:
        out = diff(input, varsym)
        assert out == exp
    print('Test Ok.')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('formula')
    parser.add_argument('--varsym', default='x')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    ans = diff(args.formula, args.varsym)
    print(ans)

    if args.test:
        __test()
