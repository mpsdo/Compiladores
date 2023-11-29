from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, MINUS, TIMES, COMMA, SEMICOLON, LBRACKET, RBRACKET, LPAREN, RPAREN, TRANSP, INVERSE}
    ignore = ' \t'
    ignore_newline = r'\n+'

    # Regular expression rules for tokens
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
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
        ('left', TIMES),
        ('left', TRANSP, INVERSE),
        ('left', LPAREN, RPAREN),
    )

    @_('S PLUS M')
    def S(self, p):
        print('\n--- S soma ---')
        result = (p.S[0] + p.M[0], p.S[1] + p.M[1], p.S[2] + p.M[2], p.S[3] + p.M[3])
        print(f"S = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('S MINUS M')
    def S(self, p):
        print('\n--- S subtração ---')
        result = (p.S[0] - p.M[0], p.S[1] - p.M[1], p.S[2] - p.M[2], p.S[3] - p.M[3])
        print(f"S = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('matrix')
    def M(self, p):
        print('\n--- M ---')
        print(f"M = [{p.matrix[0]},{p.matrix[1]};{p.matrix[2]},{p.matrix[3]}]")
        return p.matrix

    @_('M TIMES matrix')
    def M(self, p):
        print('\n--- M vezes ---')
        result = (
            (p.M[0] * p.matrix[0] + p.M[1] * p.matrix[2]),
            (p.M[0] * p.matrix[1] + p.M[1] * p.matrix[3]),
            (p.M[2] * p.matrix[0] + p.M[3] * p.matrix[2]),
            (p.M[2] * p.matrix[1] + p.M[3] * p.matrix[3]),
        )
        print(f"M = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('TRANSP matrix')
    def matrix(self, p):
        print('\n--- operação transposta ---')
        result = (p.matrix[0], p.matrix[2], p.matrix[1], p.matrix[3])
        print(f"M = t[{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('INVERSE matrix')
    def matrix(self, p):
        print('\n--- matriz inversa ---')
        print(f'M = i[{p.matrix[0]},{p.matrix[1]};{p.matrix[2]},{p.matrix[3]}]')
        print('\n--- operação de inversão ---')
        det = p.matrix[0] * p.matrix[3] - p.matrix[1] * p.matrix[2]
        if det == 0:
            print('Matriz não possui inversa')
            return None
        inv_det = 1 / det
        result = (
            inv_det * p.matrix[3],
            -inv_det * p.matrix[1],
            -inv_det * p.matrix[2],
            inv_det * p.matrix[0],
        )
        print(f'M = i[{result[0]},{result[1]};{result[2]},{result[3]}]')
        return result

    @_('LPAREN S RPAREN')
    def matrix(self, p):
        print('\n--- () ---')
        result = p.S
        print(f"M = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('LBRACKET NUMBER COMMA NUMBER SEMICOLON NUMBER COMMA NUMBER RBRACKET')
    def matrix(self, p):
        print('\n--- leitura de uma matriz ---')
        result = (p.NUMBER0, p.NUMBER1, p.NUMBER2, p.NUMBER3)
        print(f"M = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

    @_('M')
    def S(self, p):
        print('\n--- S ---')
        result = p.M
        print(f"S = [{result[0]},{result[1]};{result[2]},{result[3]}]")
        return result

if __name__ == '__main__':
    data = input('Digite a sua expressão:')
    lexer = CalcLexer()
    parser = CalcParser()
    result = parser.parse(lexer.tokenize(data))
    print('\n--- RESULTADO FINAL ---')
    print(result)
