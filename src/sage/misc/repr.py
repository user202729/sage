"""
Repr formatting support
"""

from typing import Any, Callable


def coeff_repr(c, is_latex: bool = False, *, no_space: bool = True,
               allow_parenthesize: bool = True):
    r"""
    String representing coefficients in a linear combination.

    INPUT:

    - ``c`` -- a coefficient (i.e., an element of a ring)

    OUTPUT: string

    EXAMPLES::

        sage: from sage.misc.repr import coeff_repr
        sage: coeff_repr(QQ(1/2))
        '1/2'
        sage: coeff_repr(-x^2)                                                          # needs sage.symbolic
        '(-x^2)'
        sage: coeff_repr(QQ(1/2), is_latex=True)
        '\\frac{1}{2}'
        sage: coeff_repr(-x^2, is_latex=True)                                           # needs sage.symbolic
        '\\left(-x^{2}\\right)'
        sage: R.<x> = QQ[]
        sage: coeff_repr(x^2 + 1, no_space=False)
        'x^2 + 1'
    """
    if not is_latex:
        try:
            return c._coeff_repr(no_space=no_space, allow_parenthesize=allow_parenthesize)
        except AttributeError:
            pass
    if isinstance(c, (int, float)):
        return str(c)
    if is_latex and hasattr(c, '_latex_'):
        s = c._latex_()
    else:
        s = str(c)
        if no_space:
            s = s.replace(' ', '')
    if ("+" in s or "-" in s) and allow_parenthesize:
        if is_latex:
            return "\\left(%s\\right)" % s
        else:
            return "(%s)" % s
    return s


def repr_lincomb(terms, is_latex: bool = False, scalar_mult: str = '*', strip_one: bool = False,
                 repr_monomial: Callable[[Any], str] | None = None,
                 latex_scalar_mult: str | None = None, *,
                 detect_negative_by_comparison: bool = True,
                 no_coeff_space: bool = True, keep_inexact_one_coeff: bool = True,
                 allow_lone_coeff_without_parentheses: bool = False) -> str:
    """
    Compute a string representation of a linear combination of some
    formal symbols.

    INPUT:

    - ``terms`` -- list of terms, as pairs (monomial, c) where ``c`` is a
      (scalar) coefficient
    - ``is_latex`` -- whether to produce latex (default: ``False``)
    - ``scalar_mult`` -- string representing the multiplication (default: ``'*'``)
    - ``strip_one`` -- if ``monomial`` has representation ``"1"``, represent
      ``c*monomial`` as just ``c``.

      Note that ``1*monomial`` is always represented as ``monomial``
    - ``repr_monomial`` -- function used to
    - ``latex_scalar_mult`` -- latex string representing the multiplication
      (default: a space if ``scalar_mult`` is ``'*'``; otherwise ``scalar_mult``)
    - ``detect_negative_by_comparison`` -- if ``True``, apart from checking whether the string
      representation of the coefficient starts with a minus sign, also detect negative
      coefficients by comparing it to zero.
    - ``no_coeff_space`` -- if ``True``, remove spaces from the string
      representation of the coefficient. Only applies if ``is_latex`` is ``False``.
    - ``keep_inexact_one_coeff`` -- if ``True``, keep ``1.0*x`` as is;
      otherwise, represent it as ``x``.

    EXAMPLES::

        sage: repr_lincomb([('a',1), ('b',-2), ('c',3)])
        'a - 2*b + 3*c'
        sage: repr_lincomb([('a',0), ('b',-2), ('c',3)])
        '-2*b + 3*c'
        sage: repr_lincomb([('a',0), ('b',2), ('c',3)])
        '2*b + 3*c'
        sage: repr_lincomb([('a',1), ('b',0), ('c',3)])
        'a + 3*c'
        sage: repr_lincomb([('a',-1), ('b','2+3*x'), ('c',3)])
        '-a + (2+3*x)*b + 3*c'
        sage: repr_lincomb([('a', '1+x^2'), ('b', '2+3*x'), ('c', 3)])
        '(1+x^2)*a + (2+3*x)*b + 3*c'
        sage: repr_lincomb([('a', '1+x^2'), ('b', '-2+3*x'), ('c', 3)])
        '(1+x^2)*a + (-2+3*x)*b + 3*c'
        sage: repr_lincomb([('a', 1), ('b', -2), ('c', -3)])
        'a - 2*b - 3*c'
        sage: t = PolynomialRing(RationalField(),'t').gen()
        sage: repr_lincomb([('a', -t), ('s', t - 2), ('', t^2 + 2)])
        '-t*a + (t-2)*s + (t^2+2)'

    Examples for ``scalar_mult``::

        sage: repr_lincomb([('a',1), ('b',2), ('c',3)], scalar_mult='*')
        'a + 2*b + 3*c'
        sage: repr_lincomb([('a',2), ('b',0), ('c',-3)], scalar_mult='**')
        '2**a - 3**c'
        sage: repr_lincomb([('a',-1), ('b',2), ('c',3)], scalar_mult='**')
        '-a + 2**b + 3**c'

    Examples for ``scalar_mult`` and ``is_latex``::

        sage: repr_lincomb([('a',-1), ('b',2), ('c',3)], is_latex=True)
        '-a + 2 b + 3 c'
        sage: repr_lincomb([('a',-1), ('b',-1), ('c',3)], is_latex=True, scalar_mult='*')
        '-a - b + 3 c'
        sage: repr_lincomb([('a',-1), ('b',2), ('c',-3)], is_latex=True, scalar_mult='**')
        '-a + 2**b - 3**c'
        sage: repr_lincomb([('a',-2), ('b',-1), ('c',-3)], is_latex=True, latex_scalar_mult='*')
        '-2*a - b - 3*c'
        sage: repr_lincomb([('a',-2), ('b',-1), ('c',-3)], is_latex=True, latex_scalar_mult='')
        '-2a - b - 3c'

    Examples for ``strip_one``::

        sage: repr_lincomb([ ('a',1), (1,-2), ('3',3) ])
        'a - 2*1 + 3*3'
        sage: repr_lincomb([ ('a',-1), (1,1), ('3',3) ])
        '-a + 1 + 3*3'
        sage: repr_lincomb([ ('a',1), (1,-2), ('3',3) ], strip_one = True)
        'a - 2 + 3*3'
        sage: repr_lincomb([ ('a',-1), (1,1), ('3',3) ], strip_one = True)
        '-a + 1 + 3*3'
        sage: repr_lincomb([ ('a',1), (1,-1), ('3',3) ], strip_one = True)
        'a - 1 + 3*3'

    Examples for ``repr_monomial``::

        sage: repr_lincomb([('a',1), ('b',2), ('c',3)], repr_monomial = lambda s: s+"1")
        'a1 + 2*b1 + 3*c1'

    TESTS:

    Verify that :issue:`31672` is fixed::

        sage: # needs sage.symbolic
        sage: alpha = var("alpha")
        sage: repr_lincomb([(x, alpha)], is_latex=True)
        '\\alpha x'
        sage: A.<psi> = PolynomialRing(QQ)
        sage: B.<t> = FreeAlgebra(A)                                                    # needs sage.combinat sage.modules
        sage: (psi * t)._latex_()                                                       # needs sage.combinat sage.modules
        '\\psi t'
    """
    # Setting scalar_mult: symbol used for scalar multiplication
    if is_latex:
        if latex_scalar_mult is not None:
            scalar_mult = latex_scalar_mult
        elif scalar_mult == "*":
            scalar_mult = " "

    if repr_monomial is None:
        if is_latex:

            def repr_monomial(monomial):
                return monomial._latex_() if hasattr(monomial, '_latex_') else str(monomial)
        else:
            repr_monomial = str

    s = ""
    first = True

    if scalar_mult is None:
        scalar_mult = "" if is_latex else "*"

    for (monomial, c) in terms:
        if c != 0:
            coeff = coeff_repr(c, is_latex, no_space=no_coeff_space)
            negative = False
            if not isinstance(c, str):
                # if c is already a string, we cannot obtain
                # representation of -c
                if coeff.startswith(("-", "(-", "\\left(-")):
                    negative = True
                elif detect_negative_by_comparison:
                    try:
                        if c < 0:
                            negative = True
                    except (NotImplementedError, TypeError):
                        # comparisons may not be implemented for some coefficients
                        pass
                if negative:
                    coeff = coeff_repr(-c, is_latex, no_space=no_coeff_space)
            if coeff == "1" or (not keep_inexact_one_coeff and coeff.rstrip("0") == "1."):
                coeff = ""
            if coeff != "0":
                if negative:
                    if first:
                        sign = "-"  # add trailing space?
                    else:
                        sign = " - "
                else:
                    if first:
                        sign = ""
                    else:
                        sign = " + "
                b = repr_monomial(monomial)
                if b:
                    if coeff != "":
                        if b == "1" and strip_one:
                            if len(terms) == 1 and allow_lone_coeff_without_parentheses:
                                return coeff_repr(c, is_latex, no_space=no_coeff_space, allow_parenthesize=False)
                            b = ""
                        else:
                            b = scalar_mult + b
                s += f"{sign}{coeff}{b}"
                first = False
    if first:
        return "0"
        # this can happen only if are only terms with coeff_repr(c) == "0"
    # elif s == "":
        # return "1"  # is empty string representation invalid?
    else:
        return s
