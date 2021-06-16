def diff(s: str, varsym: str) -> str:
    '''This function throws exceptions.'''

    n = len(s)
    i = i0 = 0

    ans = []
    for term in s.split('+'):
        term = term.strip()
        
        i = term.find(varsym)
        if i != -1: # Otherwise, input term was a constant.

            coeff = 1
            if i != 0:
                coeff = int(term[:i])
            deg = 1
            if i != len(term)-1:
                deg = int(term[i+2:])
            
            pfx = str(coeff * deg)

            if deg == 1:
                sfx = ''
            elif deg == 2:
                sfx = 'x'
            else:
                sfx = 'x^' + str(deg-1)
            
            ans.append(pfx + sfx)

    return ' + '.join(ans)

def __test():
    samples = [
        ("3 + 1x + 2x^2", "1 + 4x"),
        ("17x + 1x^2", "17 + 2x"),
        ("1 + 2x + -3x^2 + 17x^17 + -1x^107", "2 + -6x + 289x^16 + -107x^106"),
    ]
    for input, exp in samples:
        out = diff(input, 'x')
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
