import sympy as sp
import numpy as np


class ExpressionHandler:
    @staticmethod
    def _round_expr(expr, num_digits):
        return sp.nsimplify(expr, tolerance=1 / (10 ** num_digits))

    @staticmethod
    def _convert_float_to_pi(expr):
        expr_c = expr
        n = 5
        pi_round_n = round(np.pi, n)
        for a in sp.preorder_traversal(expr):
            if isinstance(a, sp.Float):
                rounded_a = round(float(a), n)
                if abs(rounded_a - pi_round_n) < 0.00001:
                    expr_c = expr_c.subs(a, sp.pi)
                if abs(rounded_a + pi_round_n) < 0.00001:
                    expr_c = expr_c.subs(a, -sp.pi)
                if abs(rounded_a - pi_round_n / 2) < 0.00001:
                    expr_c = expr_c.subs(a, sp.pi / 2)
                if abs(rounded_a + pi_round_n / 2) < 0.00001:
                    expr_c = expr_c.subs(a, -sp.pi / 2)
        return expr_c

    @staticmethod
    def _solve(expr, symbol):
        solver = ExpressionHandler._nsolve_pass_when_error
        start_list = [0, np.pi / 2, np.pi, 3 * np.pi / 2]
        output = []
        for start in start_list:
            q = solver(expr, symbol, start)
            if q:
                output.append(q)
        return output

    @staticmethod
    def _nsolve_pass_when_error(expr, symbol, start):
        try:
            q = sp.nsolve(expr, symbol, start)
            return q
        except Exception:
            pass
