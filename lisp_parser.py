from typing import Any, List, Optional

def parse(s: str) -> Optional[List[Any]]:
    n = len(s)
    i = 0
    stack = [ [] ]  # stack[0] is a dummy.
    while i < n:
        if s[i] == '(':
            stack.append([])
            stack[-2].append(stack[-1])
            i += 1
        elif s[i] == ')':
            stack.pop()
            i += 1
        else:
            while i < n and s[i].isspace():
                i += 1
            i0 = i
            while i < n and (not s[i].isspace()) and (s[i] not in '()'):
                i += 1
            if i0 != i:
                item = s[i0:i]
                try:
                    item = int(item)
                except:
                    pass
                stack[-1].append(item)
    
    if stack[0]:
        return stack[0][0]
    # Else, i.e. if input str was empty, return None.

def __test():
    samples = [
        ( '', None ),
        ( '()', [] ),
        ( '(first (list 1 (+ 2 3) 9))', ["first", ["list", 1, ["+", 2, 3], 9]] ),
    ]
    for input, exp in samples:
        out = parse(input)
        assert out == exp
    print('Test Ok.')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('lisp')
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()

    ans = parse(args.lisp)
    print(ans)
    
    if args.test:
        __test()