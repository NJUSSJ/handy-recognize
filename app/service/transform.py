import sympy
from latex2sympy_custom4.process_latex import process_sympy


def transform(latex, transform_content):
    final_latex = None
    if '\\rightarrow' in transform_content or '\\longrightarrow' in transform_content:
        split_symbol = ' ' + ('\\rightarrow' if '\\rightarrow' in transform_content else '\\longrightarrow') + ' '
        symbol = transform_content.split(split_symbol)[0]
        transformed_symbol = transform_content.split(split_symbol)[1].replace(' ', '')
        sympy_expr = process_sympy(latex)
        sympy_expr = sympy_expr.subs(sympy.symbols(symbol), process_sympy(transformed_symbol))
        if symbol == 'y':
            sympy_expr = sympy.solve(sympy_expr, 'y')[0]
            final_latex = 'y = ' + sympy.latex(sympy_expr).replace('\\left[', '').replace('\\right]', '')
        else:
            final_latex = sympy.latex(sympy_expr)
        final_latex = final_latex.replace('\\left(', '(').replace('\\right)', ')')
        print(final_latex)
    return final_latex


if __name__ == '__main__':
    result = transform('y =  \\cos x', 'x \\rightarrow x - \\frac{\\pi}{2}')
    transform(result, 'x \\rightarrow 2 x')
