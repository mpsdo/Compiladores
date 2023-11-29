from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, COMMA, SEMICOLON, LBRACKET, RBRACKET, LPAREN, RPAREN, TRANSP, INVERSE}
    ignore = ' \t'
    ignore_newline = r'\n+'

    # Regular expression rules for tokens
    PLUS = r'\+'
    MINUS = r'-'
    COMMA = r','
    SEMICOLON = r';'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LPAREN = r'\('
    RPAREN = r'\)'
    TRANSP = r't'
    INVERSE = r'i'

    @_(r'-?\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ('left', PLUS, MINUS),
        ('left', TRANSP, INVERSE),
        ('left', LPAREN, RPAREN),
    )

    @_('S PLUS S')
    def S(self, p):
        print('\n--- S soma ---')
        result = (
            p.S0[0] + p.S1[0],
            p.S0[1] + p.S1[1],
            p.S0[2] + p.S1[2],
            p.S0[3] + p.S1[3]
        )
        print(f"S = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('S MINUS S')
    def S(self, p):
        print('\n--- S subtração ---')
        result = (
            p.S0[0] - p.S1[0],
            p.S0[1] - p.S1[1],
            p.S0[2] - p.S1[2],
            p.S0[3] - p.S1[3]
        )
        print(f"S = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('TRANSP S')
    def S(self, p):
        print('\n--- operação transposta ---')
        result = (p.S[0], p.S[2], p.S[1], p.S[3])
        print(f"S = t[{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('INVERSE S')
    def S(self, p):
        print('\n--- matriz inversa ---')
        print('\n--- operação de inversão ---')
        det = p.S[0] * p.S[3] - p.S[1] * p.S[2]
        if det == 0:
            print('Matriz não possui inversa')
            return None
        inv_det = 1 / det
        result = (
            inv_det * p.S[3],
            -inv_det * p.S[1],
            -inv_det * p.S[2],
            inv_det * p.S[0],
        )
        print(f"S = i[{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('LPAREN S RPAREN')
    def S(self, p):
        print('\n--- () ---')
        return p.S

    @_('LBRACKET NUMBER COMMA NUMBER SEMICOLON NUMBER COMMA NUMBER RBRACKET')
    def S(self, p):
        print('\n--- leitura de uma matriz ---')
        result = (p.NUMBER0, p.NUMBER1, p.NUMBER2, p.NUMBER3)
        print(f"S = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

if __name__ == '__main__':
    data = input('Digite a sua expressão:')
    lexer = CalcLexer()
    parser = CalcParser()
    result = parser.parse(lexer.tokenize(data))
    print('\n--- RESULTADO FINAL ---')
    print(result)
