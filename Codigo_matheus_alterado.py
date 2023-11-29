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
        ('left', TRANSP),
        ('left', LPAREN, RPAREN),
    )

    @_('S PLUS M')
    def S(self, p):
        print('\n--- S soma ---')
        return (p.S[0] + p.M[0], p.S[1] + p.M[1], p.S[2] + p.M[2], p.S[3] + p.M[3])

    @_('S MINUS M')
    def S(self, p):
        print('\n--- S subtração ---')
        return (p.S[0] - p.M[0], p.S[1] - p.M[1], p.S[2] - p.M[2], p.S[3] - p.M[3])

    @_('matrix')
    def M(self, p):
        print('\n--- M ---')
        return p.matrix

    @_('M TIMES matrix')
    def M(self, p):
        print('\n--- M vezes ---')
        return ((p.M[0] * p.matrix[0] + p.M[1] * p.matrix[2]), 
                (p.M[0] * p.matrix[1] + p.M[1] * p.matrix[3]), 
                (p.M[2] * p.matrix[0] + p.M[3] * p.matrix[2]), 
                (p.M[2] * p.matrix[1] + p.M[3] * p.matrix[3]))

    @_('TRANSP matrix')
    def matrix(self, p):
        print('\n--- operação transposta ---')
        return (p.matrix[0], p.matrix[2], p.matrix[1], p.matrix[3])

    @_('INVERSE matrix')
    def matrix(self, p):
        print('\n--- operação de inversão ---')
        det = p.matrix[0] * p.matrix[3] - p.matrix[1] * p.matrix[2]
        if det == 0:
            print('Matriz não possui inversa')
            return None
        inv_det = 1 / det
        inverted_matrix = (inv_det * p.matrix[3], -inv_det * p.matrix[1], -inv_det * p.matrix[2], inv_det * p.matrix[0])
        print('Matriz inversa:', inverted_matrix)
        return inverted_matrix

    @_('LPAREN S RPAREN')
    def matrix(self, p):
        print('\n--- () ---')
        return p.S

    @_('LBRACKET NUMBER COMMA NUMBER SEMICOLON NUMBER COMMA NUMBER RBRACKET')
    def matrix(self, p):
        print('\n--- leitura de uma matrix ---')
        return (p.NUMBER0, p.NUMBER1, p.NUMBER2, p.NUMBER3)

    @_('M')
    def S(self, p):
        print('\n--- S ---')
        return p.M

if __name__ == '__main__':
    data = input('Digite a sua expressão:')
    lexer = CalcLexer()
    parser = CalcParser()
    result = parser.parse(lexer.tokenize(data))
    print('\n--- RESULTADO FINAL ---')
    print(result)
