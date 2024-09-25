# sage_setup: distribution = sagemath-categories
"""
Rings

This module provides the abstract base class :class:`Ring` from which
all rings in Sage (used to) derive, as well as a selection of more
specific base classes.

.. WARNING::

    Those classes, except maybe for the lowest ones like
    :class:`CommutativeRing` and :class:`Field`,
    are being progressively deprecated in favor of the corresponding
    categories. which are more flexible, in particular with respect to multiple
    inheritance.

The class inheritance hierarchy is:

- :class:`Ring` (to be deprecated)

  - :class:`Algebra` (deprecated and essentially removed)
  - :class:`CommutativeRing`

    - :class:`NoetherianRing` (deprecated and essentially removed)
    - :class:`CommutativeAlgebra` (deprecated and essentially removed)
    - :class:`IntegralDomain` (deprecated)

      - :class:`DedekindDomain` (deprecated and essentially removed)
      - :class:`PrincipalIdealDomain` (deprecated and essentially removed)

Subclasses of :class:`CommutativeRing` are

- :class:`Field`

  - :class:`~sage.rings.finite_rings.finite_field_base.FiniteField`

Some aspects of this structure may seem strange, but this is an unfortunate
consequence of the fact that Cython classes do not support multiple
inheritance.

(A distinct but equally awkward issue is that sometimes we may not know *in
advance* whether or not a ring belongs in one of these classes; e.g. some
orders in number fields are Dedekind domains, but others are not, and we still
want to offer a unified interface, so orders are never instances of the
deprecated :class:`DedekindDomain` class.)

AUTHORS:

- David Harvey (2006-10-16): changed :class:`CommutativeAlgebra` to derive from
  :class:`CommutativeRing` instead of from :class:`Algebra`.
- David Loeffler (2009-07-09): documentation fixes, added to reference manual.
- Simon King (2011-03-29): Proper use of the category framework for rings.
- Simon King (2011-05-20): Modify multiplication and _ideal_class_ to support
  ideals of non-commutative rings.

TESTS:

This is to test a deprecation::

    sage: from sage.rings.ring import DedekindDomain
    sage: class No(DedekindDomain):
    ....:     pass
    sage: F = No(QQ)
    ...:
    DeprecationWarning: use the category DedekindDomains
    See https://github.com/sagemath/sage/issues/37234 for details.
    sage: F.category()
    Category of Dedekind domains

    sage: from sage.rings.ring import CommutativeAlgebra
    sage: class Nein(CommutativeAlgebra):
    ....:     pass
    sage: F = Nein(QQ)
    ...:
    DeprecationWarning: use the category CommutativeAlgebras
    See https://github.com/sagemath/sage/issues/37999 for details.
    sage: F.category()
    Category of commutative algebras over Rational Field

    sage: from sage.rings.ring import PrincipalIdealDomain
    sage: class Non(PrincipalIdealDomain):
    ....:     pass
    sage: F = Non(QQ)
    ...:
    DeprecationWarning: use the category PrincipalIdealDomains
    See https://github.com/sagemath/sage/issues/37719 for details.
    sage: F.category()
    Category of principal ideal domains

    sage: from sage.rings.ring import Algebra
    sage: class Nichts(Algebra):
    ....:     pass
    sage: F = Nichts(QQ)
    ...:
    DeprecationWarning: use the category Algebras
    See https://github.com/sagemath/sage/issues/38502 for details.
    sage: F.category()
    Category of algebras over Rational Field

"""

# ****************************************************************************
#       Copyright (C) 2005, 2007 William Stein <wstein@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

from sage.misc.cachefunc import cached_method
from sage.misc.superseded import deprecation

from sage.structure.coerce cimport coercion_model
from sage.structure.parent cimport Parent
from sage.structure.category_object cimport check_default_category
from sage.misc.prandom import randint
from sage.categories.rings import Rings
from sage.categories.algebras import Algebras
from sage.categories.commutative_algebras import CommutativeAlgebras
from sage.categories.commutative_rings import CommutativeRings
from sage.categories.integral_domains import IntegralDomains
from sage.categories.dedekind_domains import DedekindDomains
from sage.categories.principal_ideal_domains import PrincipalIdealDomains
from sage.categories.noetherian_rings import NoetherianRings

_Rings = Rings()
_CommutativeRings = CommutativeRings()

cdef class Ring(ParentWithGens):
    """
    Generic ring class.

    TESTS:

    This is to test against the bug fixed in :issue:`9138`::

        sage: R.<x> = QQ[]
        sage: R.sum([x,x])
        2*x
        sage: R.<x,y> = ZZ[]
        sage: R.sum([x,y])
        x + y
        sage: TestSuite(QQ['x']).run(verbose=True)
        running ._test_additive_associativity() . . . pass
        running ._test_an_element() . . . pass
        running ._test_associativity() . . . pass
        running ._test_cardinality() . . . pass
        running ._test_category() . . . pass
        running ._test_characteristic() . . . pass
        running ._test_construction() . . . pass
        running ._test_distributivity() . . . pass
        running ._test_divides() . . . pass
        running ._test_elements() . . .
          Running the test suite of self.an_element()
          running ._test_category() . . . pass
          running ._test_eq() . . . pass
          running ._test_new() . . . pass
          running ._test_nonzero_equal() . . . pass
          running ._test_not_implemented_methods() . . . pass
          running ._test_pickling() . . . pass
          pass
        running ._test_elements_eq_reflexive() . . . pass
        running ._test_elements_eq_symmetric() . . . pass
        running ._test_elements_eq_transitive() . . . pass
        running ._test_elements_neq() . . . pass
        running ._test_eq() . . . pass
        running ._test_euclidean_degree() . . . pass
        running ._test_fraction_field() . . . pass
        running ._test_gcd_vs_xgcd() . . . pass
        running ._test_new() . . . pass
        running ._test_not_implemented_methods() . . . pass
        running ._test_one() . . . pass
        running ._test_pickling() . . . pass
        running ._test_prod() . . . pass
        running ._test_quo_rem() . . . pass
        running ._test_some_elements() . . . pass
        running ._test_zero() . . . pass
        running ._test_zero_divisors() . . . pass
        sage: TestSuite(QQ['x','y']).run(skip='_test_elements')                         # needs sage.libs.singular
        sage: TestSuite(ZZ['x','y']).run(skip='_test_elements')                         # needs sage.libs.singular
        sage: TestSuite(ZZ['x','y']['t']).run()

    Test against another bug fixed in :issue:`9944`::

        sage: QQ['x'].category()
        Join of Category of euclidean domains and Category of commutative algebras over
         (number fields and quotient fields and metric spaces) and Category of infinite sets
        sage: QQ['x','y'].category()
        Join of Category of unique factorization domains
            and Category of commutative algebras
                over (number fields and quotient fields and metric spaces)
            and Category of infinite sets
        sage: PolynomialRing(MatrixSpace(QQ, 2),'x').category()                         # needs sage.modules
        Category of infinite algebras over (finite dimensional algebras with basis over
         (number fields and quotient fields and metric spaces) and infinite sets)
        sage: PolynomialRing(SteenrodAlgebra(2),'x').category()                         # needs sage.combinat sage.modules
        Category of infinite algebras over (super Hopf algebras with basis
         over Finite Field of size 2 and supercocommutative super coalgebras
         over Finite Field of size 2)

    TESTS::

        sage: Zp(7)._repr_option('element_is_atomic')                                   # needs sage.rings.padics
        False
        sage: QQ._repr_option('element_is_atomic')
        True
        sage: CDF._repr_option('element_is_atomic')                                     # needs sage.rings.complex_double
        False

    Check that categories correctly implement `is_finite` and `cardinality`::

        sage: QQ.is_finite()
        False
        sage: GF(2^10, 'a').is_finite()                                                 # needs sage.rings.finite_rings
        True
        sage: R.<x> = GF(7)[]
        sage: R.is_finite()
        False
        sage: S.<y> = R.quo(x^2 + 1)                                                    # needs sage.rings.finite_rings
        sage: S.is_finite()                                                             # needs sage.rings.finite_rings
        True

        sage: Integers(7).cardinality()
        7
        sage: QQ.cardinality()
        +Infinity
     """
    def __init__(self, base, names=None, normalize=True, category=None):
        """
        Initialize ``self``.

        EXAMPLES::

            sage: ZZ
            Integer Ring
            sage: R.<x,y> = QQ[]
            sage: R
            Multivariate Polynomial Ring in x, y over Rational Field
        """
        # Unfortunately, ParentWithGens inherits from sage.structure.parent_old.Parent.
        # Its __init__ method does *not* call Parent.__init__, since this would somehow
        # yield an infinite recursion. But when we call it from here, it works.
        # This is done in order to ensure that __init_extra__ is called.
        #
        # ParentWithGens.__init__(self, base, names=names, normalize=normalize)
        #
        # This is a low-level class. For performance, we trust that the category
        # is fine, if it is provided. If it isn't, we use the category of rings.
        if category is None:
            category = check_default_category(_Rings, category)
        Parent.__init__(self, base=base, names=names, normalize=normalize,
                        category=category)

    def __iter__(self):
        r"""
        Return an iterator through the elements of ``self``.
        Not implemented in general.

        EXAMPLES::

            sage: sage.rings.ring.Ring.__iter__(ZZ)
            Traceback (most recent call last):
            ...
            NotImplementedError: object does not support iteration
        """
        raise NotImplementedError("object does not support iteration")

    def __len__(self):
        r"""
        Return the cardinality of this ring if it is finite, else raise
        a :exc:`NotImplementedError`.

        EXAMPLES::

            sage: len(Integers(24))
            24
            sage: len(RR)
            Traceback (most recent call last):
            ...
            NotImplementedError: len() of an infinite set
        """
        if self.is_finite():
            return self.cardinality()
        raise NotImplementedError('len() of an infinite set')

    def __xor__(self, n):
        r"""
        Trap the operation ``^``.

        EXAMPLES::

            sage: eval('RR^3')
            Traceback (most recent call last):
            ...
            RuntimeError: use ** for exponentiation, not '^', which means xor in Python, and has the wrong precedence
        """
        raise RuntimeError("use ** for exponentiation, not '^', which means xor "
              "in Python, and has the wrong precedence")

    def base_extend(self, R):
        """
        EXAMPLES::

            sage: QQ.base_extend(GF(7))
            Traceback (most recent call last):
            ...
            TypeError: no base extension defined
            sage: ZZ.base_extend(GF(7))
            Finite Field of size 7
        """
        if R.has_coerce_map_from(self):
            return R
        raise TypeError('no base extension defined')

    def category(self):
        """
        Return the category to which this ring belongs.

        .. NOTE::

            This method exists because sometimes a ring is its own base ring.
            During initialisation of a ring `R`, it may be checked whether the
            base ring (hence, the ring itself) is a ring. Hence, it is
            necessary that ``R.category()`` tells that ``R`` is a ring, even
            *before* its category is properly initialised.

        EXAMPLES::

            sage: FreeAlgebra(QQ, 3, 'x').category()  # todo: use a ring which is not an algebra!   # needs sage.combinat sage.modules
            Category of algebras with basis over Rational Field

        Since a quotient of the integers is its own base ring, and during
        initialisation of a ring it is tested whether the base ring belongs
        to the category of rings, the following is an indirect test that the
        ``category()`` method of rings returns the category of rings
        even before the initialisation was successful::

            sage: I = Integers(15)
            sage: I.base_ring() is I
            True
            sage: I.category()
            Join of Category of finite commutative rings
                and Category of subquotients of monoids
                and Category of quotients of semigroups
                and Category of finite enumerated sets
        """
        # Defining a category method is deprecated for parents.
        # For rings, however, it is strictly needed that self.category()
        # returns (a sub-category of) the category of rings before
        # initialisation has finished.
        return self._category or _Rings

    def ideal(self, *args, **kwds):
        """
        Return the ideal defined by ``x``, i.e., generated by ``x``.

        INPUT:

        - ``*x`` -- list or tuple of generators (or several input arguments)

        - ``coerce`` -- boolean (default: ``True``); this must be a keyword
          argument. Only set it to ``False`` if you are certain that each
          generator is already in the ring.

        - ``ideal_class`` -- callable (default: ``self._ideal_class_()``);
          this must be a keyword argument. A constructor for ideals, taking
          the ring as the first argument and then the generators.
          Usually a subclass of :class:`~sage.rings.ideal.Ideal_generic` or
          :class:`~sage.rings.noncommutative_ideals.Ideal_nc`.

        - Further named arguments (such as ``side`` in the case of
          non-commutative rings) are forwarded to the ideal class.

        EXAMPLES::

            sage: R.<x,y> = QQ[]
            sage: R.ideal(x,y)
            Ideal (x, y) of Multivariate Polynomial Ring in x, y over Rational Field
            sage: R.ideal(x+y^2)
            Ideal (y^2 + x) of Multivariate Polynomial Ring in x, y over Rational Field
            sage: R.ideal( [x^3,y^3+x^3] )
            Ideal (x^3, x^3 + y^3) of Multivariate Polynomial Ring in x, y over Rational Field

        Here is an example over a non-commutative ring::

            sage: A = SteenrodAlgebra(2)                                                # needs sage.combinat sage.modules
            sage: A.ideal(A.1, A.2^2)                                                   # needs sage.combinat sage.modules
            Twosided Ideal (Sq(2), Sq(2,2)) of mod 2 Steenrod algebra, milnor basis
            sage: A.ideal(A.1, A.2^2, side='left')                                      # needs sage.combinat sage.modules
            Left Ideal (Sq(2), Sq(2,2)) of mod 2 Steenrod algebra, milnor basis

        TESTS:

        Make sure that :issue:`11139` is fixed::

            sage: R.<x> = QQ[]
            sage: R.ideal([])
            Principal ideal (0) of Univariate Polynomial Ring in x over Rational Field
            sage: R.ideal(())
            Principal ideal (0) of Univariate Polynomial Ring in x over Rational Field
            sage: R.ideal()
            Principal ideal (0) of Univariate Polynomial Ring in x over Rational Field
        """
        if 'coerce' in kwds:
            coerce = kwds['coerce']
            del kwds['coerce']
        else:
            coerce = True

        from sage.rings.ideal import Ideal_generic
        from sage.structure.parent import Parent
        gens = args
        while isinstance(gens, (list, tuple)) and len(gens) == 1:
            first = gens[0]
            if isinstance(first, Ideal_generic):
                R = first.ring()
                m = self.convert_map_from(R)
                if m is not None:
                    gens = [m(g) for g in first.gens()]
                    coerce = False
                else:
                    m = R.convert_map_from(self)
                    if m is not None:
                        raise NotImplementedError
                    else:
                        raise TypeError
                break
            elif isinstance(first, (list, tuple)):
                gens = first
            elif isinstance(first, Parent) and self.has_coerce_map_from(first):
                gens = first.gens()  # we have a ring as argument
            else:
                break

        if len(gens) == 0:
            gens = [self.zero()]

        if coerce:
            gens = [self(g) for g in gens]
        if self in PrincipalIdealDomains():
            # Use GCD algorithm to obtain a principal ideal
            g = gens[0]
            if len(gens) == 1:
                try:
                    # note: we set g = gcd(g, g) to "canonicalize" the generator: make polynomials monic, etc.
                    g = g.gcd(g)
                except (AttributeError, NotImplementedError, IndexError):
                    pass
            else:
                for h in gens[1:]:
                    g = g.gcd(h)
            gens = [g]
        if 'ideal_class' in kwds:
            C = kwds['ideal_class']
            del kwds['ideal_class']
        else:
            C = self._ideal_class_(len(gens))
        if len(gens) == 1 and isinstance(gens[0], (list, tuple)):
            gens = gens[0]
        return C(self, gens, **kwds)

    def __mul__(self, x):
        """
        Return the ideal ``x*R`` generated by ``x``, where ``x`` is either an
        element or tuple or list of elements.

        EXAMPLES::

            sage: R.<x,y,z> = GF(7)[]
            sage: (x + y) * R
            Ideal (x + y) of Multivariate Polynomial Ring in x, y, z
             over Finite Field of size 7
            sage: (x + y, z + y^3) * R
            Ideal (x + y, y^3 + z) of Multivariate Polynomial Ring in x, y, z
             over Finite Field of size 7

        The following was implemented in :issue:`7797`::

            sage: # needs sage.combinat sage.modules
            sage: A = SteenrodAlgebra(2)
            sage: A * [A.1 + A.2, A.1^2]
            Left Ideal (Sq(2) + Sq(4), Sq(1,1)) of mod 2 Steenrod algebra, milnor basis
            sage: [A.1 + A.2, A.1^2] * A
            Right Ideal (Sq(2) + Sq(4), Sq(1,1)) of mod 2 Steenrod algebra, milnor basis
            sage: A * [A.1 + A.2, A.1^2] * A
            Twosided Ideal (Sq(2) + Sq(4), Sq(1,1)) of mod 2 Steenrod algebra, milnor basis
        """
        if isinstance(self, Ring):
            if self.is_commutative():
                return self.ideal(x)
            try:
                side = x.side()
            except AttributeError:
                return self.ideal(x, side='left')
            # presumably x is an ideal...
            try:
                x = x.gens()
            except (AttributeError, NotImplementedError):
                pass # ... not an ideal
            if side in ['left','twosided']:
                return self.ideal(x,side=side)
            elif side=='right':
                return self.ideal(x,side='twosided')
            else: # duck typing failed
                raise TypeError("Don't know how to transform %s into an ideal of %s" % (x, self))
        else: # the sides are switched because this is a Cython / extension class
            if x.is_commutative():
                return x.ideal(self)
            try:
                side = self.side()
            except AttributeError:
                return x.ideal(self, side='right')
            # presumably self is an ideal...
            try:
                self = self.gens()
            except (AttributeError, NotImplementedError):
                pass # ... not an ideal
            if side in ['right','twosided']:
                return x.ideal(self,side='twosided')
            elif side=='left':
                return x.ideal(self,side='twosided')
            else:
                raise TypeError("Don't know how to transform %s into an ideal of %s" % (self, x))

    def zero(self):
        """
        Return the zero element of this ring (cached).

        EXAMPLES::

            sage: ZZ.zero()
            0
            sage: QQ.zero()
            0
            sage: QQ['x'].zero()
            0

        The result is cached::

            sage: ZZ.zero() is ZZ.zero()
            True
        """
        if self._zero_element is None:
            x = self(0)
            self._zero_element = x
            return x
        return self._zero_element

    def one(self):
        """
        Return the one element of this ring (cached), if it exists.

        EXAMPLES::

            sage: ZZ.one()
            1
            sage: QQ.one()
            1
            sage: QQ['x'].one()
            1

        The result is cached::

            sage: ZZ.one() is ZZ.one()
            True
        """
        if self._one_element is None:
            x = self(1)
            self._one_element = x
            return x
        return self._one_element

    def is_field(self, proof=True):
        """
        Return ``True`` if this ring is a field.

        INPUT:

        - ``proof`` -- boolean (default: ``True``); determines what to do in
          unknown cases

        ALGORITHM:

        If the parameter ``proof`` is set to ``True``, the returned value is
        correct but the method might throw an error.  Otherwise, if it is set
        to ``False``, the method returns ``True`` if it can establish that
        ``self`` is a field and ``False`` otherwise.

        EXAMPLES::

            sage: QQ.is_field()
            True
            sage: GF(9, 'a').is_field()                                                 # needs sage.rings.finite_rings
            True
            sage: ZZ.is_field()
            False
            sage: QQ['x'].is_field()
            False
            sage: Frac(QQ['x']).is_field()
            True

        This illustrates the use of the ``proof`` parameter::

            sage: R.<a,b> = QQ[]
            sage: S.<x,y> = R.quo((b^3))                                                # needs sage.libs.singular
            sage: S.is_field(proof=True)                                                # needs sage.libs.singular
            Traceback (most recent call last):
            ...
            NotImplementedError
            sage: S.is_field(proof=False)                                               # needs sage.libs.singular
            False
        """
        if self.is_zero():
            return False

        if proof:
            raise NotImplementedError("No way to prove that %s is an integral domain!" % self)
        else:
            return False

    cpdef bint is_exact(self) except -2:
        """
        Return ``True`` if elements of this ring are represented exactly, i.e.,
        there is no precision loss when doing arithmetic.

        .. NOTE::

            This defaults to ``True``, so even if it does return ``True`` you
            have no guarantee (unless the ring has properly overloaded this).

        EXAMPLES::

            sage: QQ.is_exact()    # indirect doctest
            True
            sage: ZZ.is_exact()
            True
            sage: Qp(7).is_exact()                                                      # needs sage.rings.padics
            False
            sage: Zp(7, type='capped-abs').is_exact()                                   # needs sage.rings.padics
            False
        """
        return True

    def is_subring(self, other):
        """
        Return ``True`` if the canonical map from ``self`` to ``other`` is
        injective.

        Raises a :exc:`NotImplementedError` if not known.

        EXAMPLES::

            sage: ZZ.is_subring(QQ)
            True
            sage: ZZ.is_subring(GF(19))
            False

        TESTS::

            sage: QQ.is_subring(QQ['x'])
            True
            sage: QQ.is_subring(GF(7))
            False
            sage: QQ.is_subring(CyclotomicField(7))                                     # needs sage.rings.number_field
            True
            sage: QQ.is_subring(ZZ)
            False

        Every ring is a subring of itself, :issue:`17287`::

            sage: QQbar.is_subring(QQbar)                                               # needs sage.rings.number_field
            True
            sage: RR.is_subring(RR)
            True
            sage: CC.is_subring(CC)                                                     # needs sage.rings.real_mpfr
            True
            sage: x = polygen(ZZ, 'x')
            sage: K.<a> = NumberField(x^3 - x + 1/10)                                   # needs sage.rings.number_field
            sage: K.is_subring(K)                                                       # needs sage.rings.number_field
            True
            sage: R.<x> = RR[]
            sage: R.is_subring(R)
            True
        """
        if self is other:
            return True
        try:
            return self.Hom(other).natural_map().is_injective()
        except (TypeError, AttributeError):
            return False

    def is_prime_field(self):
        r"""
        Return ``True`` if this ring is one of the prime fields `\QQ` or
        `\GF{p}`.

        EXAMPLES::

            sage: QQ.is_prime_field()
            True
            sage: GF(3).is_prime_field()
            True
            sage: GF(9, 'a').is_prime_field()                                           # needs sage.rings.finite_rings
            False
            sage: ZZ.is_prime_field()
            False
            sage: QQ['x'].is_prime_field()
            False
            sage: Qp(19).is_prime_field()                                               # needs sage.rings.padics
            False
        """
        return False

    def order(self):
        """
        The number of elements of ``self``.

        EXAMPLES::

            sage: GF(19).order()
            19
            sage: QQ.order()
            +Infinity
        """
        if self.is_zero():
            return 1
        raise NotImplementedError

    def zeta(self, n=2, all=False):
        """
        Return a primitive ``n``-th root of unity in ``self`` if there
        is one, or raise a :exc:`ValueError` otherwise.

        INPUT:

        - ``n`` -- positive integer

        - ``all`` -- boolean (default: ``False``); whether to return
          a list of all primitive `n`-th roots of unity. If ``True``, raise a
          :exc:`ValueError` if ``self`` is not an integral domain.

        OUTPUT: element of ``self`` of finite order

        EXAMPLES::

            sage: QQ.zeta()
            -1
            sage: QQ.zeta(1)
            1
            sage: CyclotomicField(6).zeta(6)                                            # needs sage.rings.number_field
            zeta6
            sage: CyclotomicField(3).zeta(3)                                            # needs sage.rings.number_field
            zeta3
            sage: CyclotomicField(3).zeta(3).multiplicative_order()                     # needs sage.rings.number_field
            3

            sage: # needs sage.rings.finite_rings
            sage: a = GF(7).zeta(); a
            3
            sage: a.multiplicative_order()
            6
            sage: a = GF(49,'z').zeta(); a
            z
            sage: a.multiplicative_order()
            48
            sage: a = GF(49,'z').zeta(2); a
            6
            sage: a.multiplicative_order()
            2

            sage: QQ.zeta(3)
            Traceback (most recent call last):
            ...
            ValueError: no n-th root of unity in rational field
            sage: Zp(7, prec=8).zeta()                                                  # needs sage.rings.padics
            3 + 4*7 + 6*7^2 + 3*7^3 + 2*7^5 + 6*7^6 + 2*7^7 + O(7^8)

        TESTS::

            sage: from sage.rings.ring import Ring
            sage: Ring.zeta(QQ, 1)
            1
            sage: Ring.zeta(QQ, 2)
            -1
            sage: Ring.zeta(QQ, 3)                                                      # needs sage.libs.pari
            Traceback (most recent call last):
            ...
            ValueError: no 3rd root of unity in Rational Field
            sage: IntegerModRing(8).zeta(2, all = True)
            Traceback (most recent call last):
            ...
            ValueError: ring is not an integral domain
        """
        if all and not self.is_integral_domain():
            raise ValueError("ring is not an integral domain")
        if n == 2:
            if all:
                return [self(-1)]
            else:
                return self(-1)
        elif n == 1:
            if all:
                return [self(1)]
            else:
                return self(1)
        else:
            f = self['x'].cyclotomic_polynomial(n)
            if all:
                return [-P[0] for P, e in f.factor() if P.degree() == 1]
            for P, e in f.factor():
                if P.degree() == 1:
                    return -P[0]
            from sage.rings.integer_ring import ZZ
            raise ValueError("no %s root of unity in %r" % (ZZ(n).ordinal_str(), self))

    def zeta_order(self):
        """
        Return the order of the distinguished root of unity in ``self``.

        EXAMPLES::

            sage: CyclotomicField(19).zeta_order()                                      # needs sage.rings.number_field
            38
            sage: GF(19).zeta_order()
            18
            sage: GF(5^3,'a').zeta_order()                                              # needs sage.rings.finite_rings
            124
            sage: Zp(7, prec=8).zeta_order()                                            # needs sage.rings.padics
            6
        """
        return self.zeta().multiplicative_order()

    def random_element(self, bound=2):
        """
        Return a random integer coerced into this ring, where the
        integer is chosen uniformly from the interval ``[-bound,bound]``.

        INPUT:

        - ``bound`` -- integer (default: 2)

        ALGORITHM:

        Uses Python's randint.

        TESTS:

        The following example returns a :exc:`NotImplementedError` since the
        generic ring class ``__call__`` function returns a
        :exc:`NotImplementedError`. Note that
        ``sage.rings.ring.Ring.random_element`` performs a call in the generic
        ring class by a random integer::

            sage: R = sage.rings.ring.Ring(ZZ); R
            <sage.rings.ring.Ring object at ...>
            sage: R.random_element()
            Traceback (most recent call last):
            ...
            NotImplementedError: cannot construct elements of <sage.rings.ring.Ring object at ...>
        """
        return self(randint(-bound,bound))

    @cached_method
    def epsilon(self):
        """
        Return the precision error of elements in this ring.

        EXAMPLES::

            sage: RDF.epsilon()
            2.220446049250313e-16
            sage: ComplexField(53).epsilon()                                            # needs sage.rings.real_mpfr
            2.22044604925031e-16
            sage: RealField(10).epsilon()                                               # needs sage.rings.real_mpfr
            0.0020

        For exact rings, zero is returned::

            sage: ZZ.epsilon()
            0

        This also works over derived rings::

            sage: RR['x'].epsilon()                                                     # needs sage.rings.real_mpfr
            2.22044604925031e-16
            sage: QQ['x'].epsilon()
            0

        For the symbolic ring, there is no reasonable answer::

            sage: SR.epsilon()                                                          # needs sage.symbolic
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        one = self.one()
        try:
            return one.ulp()
        except AttributeError:
            pass

        try:
            eps = one.real().ulp()
        except AttributeError:
            pass
        else:
            return self(eps)

        B = self._base
        if B is not None and B is not self:
            eps = self.base_ring().epsilon()
            return self(eps)
        if self.is_exact():
            return self.zero()
        raise NotImplementedError

cdef class CommutativeRing(Ring):
    """
    Generic commutative ring.
    """
    _default_category = _CommutativeRings

    def __init__(self, base_ring, names=None, normalize=True, category=None):
        """
        Initialize ``self``.

        EXAMPLES::

            sage: Integers(389)['x,y']
            Multivariate Polynomial Ring in x, y over Ring of integers modulo 389
        """
        try:
            if not base_ring.is_commutative():
                raise TypeError("base ring %s is no commutative ring" % base_ring)
        except AttributeError:
            raise TypeError("base ring %s is no commutative ring" % base_ring)
        # This is a low-level class. For performance, we trust that
        # the category is fine, if it is provided. If it isn't, we use
        # the category of commutative rings.
        category = check_default_category(self._default_category, category)
        Ring.__init__(self, base_ring, names=names, normalize=normalize,
                      category=category)

    def localization(self, additional_units, names=None, normalize=True, category=None):
        """
        Return the localization of ``self`` at the given additional units.

        EXAMPLES::

            sage: R.<x, y> = GF(3)[]
            sage: R.localization((x*y, x**2 + y**2))                                    # needs sage.rings.finite_rings
            Multivariate Polynomial Ring in x, y over Finite Field of size 3
             localized at (y, x, x^2 + y^2)
            sage: ~y in _                                                               # needs sage.rings.finite_rings
            True
        """
        if not self.is_integral_domain():
            raise TypeError("self must be an integral domain.")

        from sage.rings.localization import Localization
        return Localization(self, additional_units, names=names, normalize=normalize, category=category)

    def fraction_field(self):
        """
        Return the fraction field of ``self``.

        EXAMPLES::

            sage: R = Integers(389)['x,y']
            sage: Frac(R)
            Fraction Field of Multivariate Polynomial Ring in x, y over Ring of integers modulo 389
            sage: R.fraction_field()
            Fraction Field of Multivariate Polynomial Ring in x, y over Ring of integers modulo 389
        """
        try:
            if self.is_field():
                return self
        except NotImplementedError:
            pass

        if not self.is_integral_domain():
            raise TypeError("self must be an integral domain.")

        if self.__fraction_field is not None:
            return self.__fraction_field
        else:
            import sage.rings.fraction_field
            K = sage.rings.fraction_field.FractionField_generic(self)
            self.__fraction_field = K
        return self.__fraction_field

    def _pseudo_fraction_field(self):
        r"""
        This method is used by the coercion model to determine if `a / b`
        should be treated as `a * (1/b)`, for example when dividing an element
        of `\ZZ[x]` by an element of `\ZZ`.

        The default is to return the same value as ``self.fraction_field()``,
        but it may return some other domain in which division is usually
        defined (for example, ``\ZZ/n\ZZ`` for possibly composite `n`).

        EXAMPLES::

            sage: ZZ._pseudo_fraction_field()
            Rational Field
            sage: ZZ['x']._pseudo_fraction_field()
            Fraction Field of Univariate Polynomial Ring in x over Integer Ring
            sage: Integers(15)._pseudo_fraction_field()
            Ring of integers modulo 15
            sage: Integers(15).fraction_field()
            Traceback (most recent call last):
            ...
            TypeError: self must be an integral domain.
        """
        try:
            return self.fraction_field()
        except (NotImplementedError,TypeError):
            return coercion_model.division_parent(self)

    def is_commutative(self):
        """
        Return ``True``, since this ring is commutative.

        EXAMPLES::

            sage: QQ.is_commutative()
            True
            sage: ZpCA(7).is_commutative()                                              # needs sage.rings.padics
            True
            sage: A = QuaternionAlgebra(QQ, -1, -3, names=('i','j','k')); A             # needs sage.combinat sage.modules
            Quaternion Algebra (-1, -3) with base ring Rational Field
            sage: A.is_commutative()                                                    # needs sage.combinat sage.modules
            False
        """
        return True

    def krull_dimension(self):
        """
        Return the Krull dimension of this commutative ring.

        The Krull dimension is the length of the longest ascending chain
        of prime ideals.

        TESTS:

        ``krull_dimension`` is not implemented for generic commutative
        rings. Fields and PIDs, with Krull dimension equal to 0 and 1,
        respectively, have naive implementations of ``krull_dimension``.
        Orders in number fields also have Krull dimension 1::

            sage: R = CommutativeRing(ZZ)
            sage: R.krull_dimension()
            Traceback (most recent call last):
            ...
            NotImplementedError
            sage: QQ.krull_dimension()
            0
            sage: ZZ.krull_dimension()
            1
            sage: type(R); type(QQ); type(ZZ)
            <class 'sage.rings.ring.CommutativeRing'>
            <class 'sage.rings.rational_field.RationalField_with_category'>
            <class 'sage.rings.integer_ring.IntegerRing_class'>

        All orders in number fields have Krull dimension 1, including
        non-maximal orders::

            sage: # needs sage.rings.number_field
            sage: K.<i> = QuadraticField(-1)
            sage: R = K.maximal_order(); R
            Gaussian Integers generated by i in Number Field in i
             with defining polynomial x^2 + 1 with i = 1*I
            sage: R.krull_dimension()
            1
            sage: R = K.order(2*i); R
            Order of conductor 2 generated by 2*i in Number Field in i
             with defining polynomial x^2 + 1 with i = 1*I
            sage: R.is_maximal()
            False
            sage: R.krull_dimension()
            1
        """
        raise NotImplementedError

    def extension(self, poly, name=None, names=None, **kwds):
        """
        Algebraically extend ``self`` by taking the quotient
        ``self[x] / (f(x))``.

        INPUT:

        - ``poly`` -- a polynomial whose coefficients are coercible into
          ``self``

        - ``name`` -- (optional) name for the root of `f`

        .. NOTE::

            Using this method on an algebraically complete field does *not*
            return this field; the construction ``self[x] / (f(x))`` is done
            anyway.

        EXAMPLES::

            sage: R = QQ['x']
            sage: y = polygen(R)
            sage: R.extension(y^2 - 5, 'a')                                             # needs sage.libs.pari
            Univariate Quotient Polynomial Ring in a over
             Univariate Polynomial Ring in x over Rational Field with modulus a^2 - 5

        ::

            sage: # needs sage.rings.finite_rings
            sage: P.<x> = PolynomialRing(GF(5))
            sage: F.<a> = GF(5).extension(x^2 - 2)
            sage: P.<t> = F[]
            sage: R.<b> = F.extension(t^2 - a); R
            Univariate Quotient Polynomial Ring in b over
             Finite Field in a of size 5^2 with modulus b^2 + 4*a
        """
        from sage.rings.polynomial.polynomial_element import Polynomial
        if not isinstance(poly, Polynomial):
            try:
                poly = poly.polynomial(self)
            except (AttributeError, TypeError):
                raise TypeError("polynomial (=%s) must be a polynomial." % repr(poly))
        if names is not None:
            name = names
        if isinstance(name, tuple):
            name = name[0]
        if name is None:
            name = str(poly.parent().gen(0))
        for key, val in kwds.items():
            if key not in ['structure', 'implementation', 'prec', 'embedding', 'latex_name', 'latex_names']:
                raise TypeError("extension() got an unexpected keyword argument '%s'" % key)
            if not (val is None or isinstance(val, list) and all(c is None for c in val)):
                raise NotImplementedError("ring extension with prescribed %s is not implemented" % key)
        R = self[name]
        I = R.ideal(R(poly.list()))
        return R.quotient(I, name)


cdef class IntegralDomain(CommutativeRing):
    """
    Generic integral domain class.

    This class is deprecated. Please use the
    :class:`sage.categories.integral_domains.IntegralDomains`
    category instead.
    """
    _default_category = IntegralDomains()

    def __init__(self, base_ring, names=None, normalize=True, category=None):
        """
        Initialize ``self``.

        INPUT:

         - ``category`` -- (default: ``None``) a category, or ``None``

        This method is used by all the abstract subclasses of
        :class:`IntegralDomain`, like :class:`Field`, ... in order to
        avoid cascade calls Field.__init__ ->
        IntegralDomain.__init__ ->
        ...

        EXAMPLES::

            sage: F = IntegralDomain(QQ)
            sage: F.category()
            Category of integral domains

            sage: F = Field(QQ)
            sage: F.category()
            Category of fields

        The default value for the category is specified by the class
        attribute ``default_category``::

            sage: IntegralDomain._default_category
            Category of integral domains

            sage: Field._default_category
            Category of fields
        """
        CommutativeRing.__init__(self, base_ring, names=names, normalize=normalize,
                                 category=category)

    def is_integrally_closed(self):
        r"""
        Return ``True`` if this ring is integrally closed in its field of
        fractions; otherwise return ``False``.

        When no algorithm is implemented for this, then this
        function raises a :exc:`NotImplementedError`.

        Note that ``is_integrally_closed`` has a naive implementation
        in fields. For every field `F`, `F` is its own field of fractions,
        hence every element of `F` is integral over `F`.

        EXAMPLES::

            sage: ZZ.is_integrally_closed()
            True
            sage: QQ.is_integrally_closed()
            True
            sage: QQbar.is_integrally_closed()                                          # needs sage.rings.number_field
            True
            sage: GF(5).is_integrally_closed()
            True
            sage: Z5 = Integers(5); Z5
            Ring of integers modulo 5
            sage: Z5.is_integrally_closed()
            Traceback (most recent call last):
            ...
            AttributeError: 'IntegerModRing_generic_with_category' object has no attribute 'is_integrally_closed'...
        """
        raise NotImplementedError

    def is_field(self, proof=True):
        r"""
        Return ``True`` if this ring is a field.

        EXAMPLES::

            sage: GF(7).is_field()
            True

        The following examples have their own ``is_field`` implementations::

            sage: ZZ.is_field(); QQ.is_field()
            False
            True
            sage: R.<x> = PolynomialRing(QQ); R.is_field()
            False
        """
        if self.is_finite():
            return True
        if proof:
            raise NotImplementedError("unable to determine whether or not is a field.")
        else:
            return False

cdef class NoetherianRing(CommutativeRing):
    _default_category = NoetherianRings()

    def __init__(self, *args, **kwds):
        deprecation(37234, "use the category NoetherianRings")
        super().__init__(*args, **kwds)


cdef class DedekindDomain(CommutativeRing):
    _default_category = DedekindDomains()

    def __init__(self, *args, **kwds):
        deprecation(37234, "use the category DedekindDomains")
        super().__init__(*args, **kwds)


cdef class PrincipalIdealDomain(CommutativeRing):
    _default_category = PrincipalIdealDomains()

    def __init__(self, *args, **kwds):
        deprecation(37719, "use the category PrincipalIdealDomains")
        super().__init__(*args, **kwds)


cpdef bint _is_Field(x) except -2:
    """
    Return ``True`` if ``x`` is a field.

    EXAMPLES::

        sage: from sage.rings.ring import _is_Field
        sage: _is_Field(QQ)
        True
        sage: _is_Field(ZZ)
        False
        sage: _is_Field(pAdicField(2))                                                  # needs sage.rings.padics
        True
        sage: _is_Field(5)
        False

    NOTE:

    ``_is_Field(R)`` is of internal use. It is better (and faster) to
    use ``R in Fields()`` instead.
    """
    # The result is not immediately returned, since we want to refine
    # x's category, so that calling x in Fields() will be faster next time.
    try:
        result = isinstance(x, Field) or x.is_field()
    except AttributeError:
        result = False
    if result:
        x._refine_category_(_Fields)
    return result

from sage.categories.algebras import Algebras
from sage.categories.commutative_algebras import CommutativeAlgebras
from sage.categories.fields import Fields
_Fields = Fields()

cdef class Field(CommutativeRing):
    """
    Generic field

    TESTS::

        sage: QQ.is_noetherian()
        True
    """
    _default_category = _Fields

    def fraction_field(self):
        """
        Return the fraction field of ``self``.

        EXAMPLES:

        Since fields are their own field of fractions, we simply get the
        original field in return::

            sage: QQ.fraction_field()
            Rational Field
            sage: RR.fraction_field()                                                   # needs sage.rings.real_mpfr
            Real Field with 53 bits of precision
            sage: CC.fraction_field()                                                   # needs sage.rings.real_mpfr
            Complex Field with 53 bits of precision

            sage: x = polygen(ZZ, 'x')
            sage: F = NumberField(x^2 + 1, 'i')                                         # needs sage.rings.number_field
            sage: F.fraction_field()                                                    # needs sage.rings.number_field
            Number Field in i with defining polynomial x^2 + 1
        """
        return self

    def _pseudo_fraction_field(self):
        """
        The fraction field of ``self`` is always available as ``self``.

        EXAMPLES::

            sage: QQ._pseudo_fraction_field()
            Rational Field
            sage: K = GF(5)
            sage: K._pseudo_fraction_field()
            Finite Field of size 5
            sage: K._pseudo_fraction_field() is K
            True
        """
        return self

    def divides(self, x, y, coerce=True):
        """
        Return ``True`` if ``x`` divides ``y`` in this field (usually ``True``
        in a field!).  If ``coerce`` is ``True`` (the default), first coerce
        ``x`` and ``y`` into ``self``.

        EXAMPLES::

            sage: QQ.divides(2, 3/4)
            True
            sage: QQ.divides(0, 5)
            False
        """
        if coerce:
            x = self(x)
            y = self(y)
        if x.is_zero():
            return y.is_zero()
        return True

    def ideal(self, *gens, **kwds):
        """
        Return the ideal generated by gens.

        EXAMPLES::

            sage: QQ.ideal(2)
            Principal ideal (1) of Rational Field
            sage: QQ.ideal(0)
            Principal ideal (0) of Rational Field
        """
        if len(gens) == 1 and isinstance(gens[0], (list, tuple)):
            gens = gens[0]
        if not isinstance(gens, (list, tuple)):
            gens = [gens]
        for x in gens:
            if not self(x).is_zero():
                return self.unit_ideal()
        return self.zero_ideal()

    def integral_closure(self):
        """
        Return this field, since fields are integrally closed in their
        fraction field.

        EXAMPLES::

            sage: QQ.integral_closure()
            Rational Field
            sage: Frac(ZZ['x,y']).integral_closure()
            Fraction Field of Multivariate Polynomial Ring in x, y over Integer Ring
        """
        return self

    def is_field(self, proof = True):
        """
        Return ``True`` since this is a field.

        EXAMPLES::

            sage: Frac(ZZ['x,y']).is_field()
            True
        """
        return True

    def is_integrally_closed(self):
        """
        Return ``True`` since fields are trivially integrally closed in
        their fraction field (since they are their own fraction field).

        EXAMPLES::

            sage: Frac(ZZ['x,y']).is_integrally_closed()
            True
        """
        return True

    def krull_dimension(self):
        """
        Return the Krull dimension of this field, which is 0.

        EXAMPLES::

            sage: QQ.krull_dimension()
            0
            sage: Frac(QQ['x,y']).krull_dimension()
            0
        """
        return 0

    def prime_subfield(self):
        """
        Return the prime subfield of ``self``.

        EXAMPLES::

            sage: k = GF(9, 'a')                                                        # needs sage.rings.finite_rings
            sage: k.prime_subfield()                                                    # needs sage.rings.finite_rings
            Finite Field of size 3
        """
        if self.characteristic() == 0:
            import sage.rings.rational_field
            return sage.rings.rational_field.RationalField()
        else:
            from sage.rings.finite_rings.finite_field_constructor import GF
            return GF(self.characteristic())

    def algebraic_closure(self):
        """
        Return the algebraic closure of ``self``.

        .. NOTE::

           This is only implemented for certain classes of field.

        EXAMPLES::

            sage: K = PolynomialRing(QQ,'x').fraction_field(); K
            Fraction Field of Univariate Polynomial Ring in x over Rational Field
            sage: K.algebraic_closure()
            Traceback (most recent call last):
            ...
            NotImplementedError: Algebraic closures of general fields not implemented.
        """
        raise NotImplementedError("Algebraic closures of general fields not implemented.")


cdef class Algebra(Ring):
    def __init__(self, base_ring, *args, **kwds):
        if 'category' not in kwds:
            kwds['category'] = Algebras(base_ring)
        deprecation(38502, "use the category Algebras")
        super().__init__(base_ring, *args, **kwds)


cdef class CommutativeAlgebra(CommutativeRing):
    def __init__(self, base_ring, *args, **kwds):
        self._default_category = CommutativeAlgebras(base_ring)
        deprecation(37999, "use the category CommutativeAlgebras")
        super().__init__(base_ring, *args, **kwds)


def is_Ring(x):
    """
    Return ``True`` if ``x`` is a ring.

    EXAMPLES::

        sage: from sage.rings.ring import is_Ring
        sage: is_Ring(ZZ)
        doctest:warning...
        DeprecationWarning: The function is_Ring is deprecated; use '... in Rings()' instead
        See https://github.com/sagemath/sage/issues/38288 for details.
        True
        sage: MS = MatrixSpace(QQ, 2)                                                   # needs sage.modules
        sage: is_Ring(MS)                                                               # needs sage.modules
        True
    """
    from sage.misc.superseded import deprecation_cython
    deprecation_cython(38288,
                       "The function is_Ring is deprecated; "
                       "use '... in Rings()' instead")
    return x in _Rings
