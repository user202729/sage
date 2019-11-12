r"""
Characteristic Classes

Let `E \to M` be some topological vector bundle over a topological manifold `M`
and `R` be some ring.
A *characteristic class* `c(E)` is an element of the cohomology ring
`H^{*}(M, R)` such that for any continuous map `f: M \to N` the *naturality
condition* is satisfied:

.. MATH::

    c(f^*E) = f^*c(E) .

Roughly speaking, characteristic classes measure the non-triviality of the
vector bundle `E`.

One way to obtain and compute characteristic classes in the de Rham cohomology
with coefficients in the ring `\CC` is via the so-called *Chern-Weil theory*
using the curvature of a differentiable vector bundle. This approach is used for
computation in SAGE.

For that let `\nabla` be a connection on `E`, `e` a local frame on
`E` and `\Omega` be the corresponding curvature matrix
(see: :meth:`~sage.manifolds.differentiable.bundle_connection.BundleConnection.curvature_form`).

Namely, if `P: \mathfrak{g} \to \CC` is an invariant polynomial, the object

.. MATH::

    \left[ P \left( \Omega \right) \right] \in H^{2*}_{\mathrm{dR}}(M, \CC)

is well-defined, independent of the choice of `\nabla` (the proof can be
found in [Roe1988]_ pp. 31) and fulfills the naturality condition.
This is the foundation of the Chern-Weil theory and therefore the following
definitions.

.. NOTE::

    This documentation is rich of examples, but sparse in explanations. Please
    consult the references for more details.

AUTHORS:

- Michael Jung (2019) : initial version

REFERENCES:

- [Mil1974]_
- [Roe1988]_

Contents
--------

We consider the following three types of classes:

- :ref:`additive`
- :ref:`multiplicative`
- :ref:`Pfaffian`

.. _additive:

Additive Classes
----------------

In the **complex** case, let `f` be a holomorphic function around zero. Then
we call

.. MATH::

    \left[\mathrm{tr}\left( f\left( \frac{\Omega}{2 \pi i} \right)
        \right)\right] \in H^{2*}_{\mathrm{dR}}(M, \CC)

the *additive Chern f-genus*.

Important and predefined additive Chern genera are:

- *Chern Character* with `f(x) = \exp(x)`

In the **real** case, let `g` be a holomorphic function around zero. Then we
call

.. MATH::

    \left[\mathrm{tr}\left( \frac{1}{2} g\left( -\frac{\Omega^2}{4 \pi^2}
        \right) \right)\right] \in H^{4*}_{\mathrm{dR}}(M, \CC)

the *additive Pontryagin g-genus*.

EXAMPLES:

Consider the **Chern character** on some 2-dimensional spacetime::

    sage: M = Manifold(2, 'M', structure='Lorentzian')
    sage: X.<t,x> = M.chart()
    sage: E = M.vector_bundle(1, 'E', field='complex'); E
    Differentiable complex vector bundle E -> M of rank 1 over the base space
     2-dimensional Lorentzian manifold M
    sage: e = E.local_frame('e')

Let us define the connection `\nabla^E` in terms of an electro-magnetic
potential `A(t)`::

    sage: nab = E.bundle_connection('nabla^E', latex_name=r'\nabla^E')
    sage: omega = M.one_form(name='omega')
    sage: A = function('A')
    sage: omega[1] = I*A(t)
    sage: omega.display()
    omega = I*A(t) dx
    sage: nab.set_connection_form(0, 0, omega)

The Chern character is then given by::

    sage: ch = E.char_class('ChernChar'); ch
    Characteristic class ch of additive type associated to e^x on the
     Differentiable complex vector bundle E -> M of rank 1 over the base space
     2-dimensional Lorentzian manifold M
    sage: ch_form = ch.get_form(nab); ch_form.display_expansion()
    ch(E, nabla^E) = [1] + [0] + [1/2*d(A)/dt/pi dt/\dx]

.. _multiplicative:

Multiplicative Classes
----------------------

In the **complex** case, let `f` be a holomorphic function around zero.
Then we call

.. MATH::

    \left[\det\left( f\left( \frac{\Omega}{2 \pi i} \right)
        \right)\right] \in H^{2*}_{\mathrm{dR}}(M, \CC)

the *multiplicative Chern f-genus*.

Important and predefined multiplicative Chern genera are:

- *Chern class* with `f(x) = 1+x`
- *Todd class* with `f(x) = \frac{x}{1-\exp(-x)}`

In the **real** case, let `g` be a holomorphic function around zero with
`g(0)=1`. Then we call

.. MATH::

    \left[\det\left( \sqrt{ g \left( -\frac{\Omega^2}{4 \pi^2} \right) } \right) \right] \in H^{4*}_{\mathrm{dR}}(M, \CC)

the *multiplicative Pontryagin g-genus*.

Important and predefined multiplicative Pontryagin genera are:

- *Pontryagin class* with `g(x) = 1+x`
- `\hat{A}` *class* with `g(x) = \frac{\sqrt{x}/2}{\sinh(\sqrt{x}/2)}`
- *Hirzebruch class* with `g(x) = \frac{\sqrt{x}}{\tanh(\sqrt{x})}`

EXAMPLES:

We consider the **Chern class** of the tautological line bundle `\gamma^1` over
`\CC\mathbf{P}^1`::

    sage: M = Manifold(2, 'CP^1', start_index=1)
    sage: U = M.open_subset('U')
    sage: c_cart.<x,y> = U.chart() # homogeneous coordinates in real terms
    sage: c_comp.<z, zbar> = U.chart(r'z:z zbar:\bar{z}') # complexification
    sage: cart_to_comp = c_cart.transition_map(c_comp, (x+I*y, x-I*y))
    sage: comp_to_cart = cart_to_comp.inverse()
    sage: E = M.vector_bundle(1, 'gamma^1', field='complex')
    sage: e = E.local_frame('e', domain=U)

To apply the Chern-Weil approach, we need a bundle connection in terms of a
connection one form. To achieve this, we take the connection induced from the
hermitian metric on the trivial bundle
`\CC^2 \times \CC\mathbf{P}^1 \supset \gamma^1`. In this the frame `e`
corresponds to the section `[z:1] \mapsto (z,1)` and its magnitude-squared
is given by `1+|z|^2`::

    sage: nab = E.bundle_connection('nabla')
    sage: omega = U.one_form(name='omega')
    sage: omega[c_comp.frame(),1,c_comp] = zbar/(1+z*zbar)
    sage: nab.set_connection_form(1, 1, omega, frame=e)

Now, the Chern class can be constructed::

    sage: c = E.char_class('Chern'); c
    Characteristic class c of multiplicative type associated to x + 1 on the
     Differentiable complex vector bundle gamma^1 -> CP^1 of rank 1 over the
     base space 2-dimensional differentiable manifold CP^1
    sage: c_form = c.get_form(nab)
    sage: c_form.display_expansion(c_comp.frame(), chart=c_comp)
    c(gamma^1, nabla) = [1] + [0] + [1/2*I/(pi + pi*z^2*zbar^2 + 2*pi*z*zbar) dz/\dzbar]

Since `U` and `\CC\mathbf{P}^1` differ only by a point and therefore a null
set, it is enough to integrate the top form over the domain `U`::

    sage: integrate(integrate(c_form[2][[1,2]].expr(c_cart), x, -infinity, infinity).full_simplify(),
    ....:           y, -infinity, infinity)
    1

The result shows that `c_1(\gamma^1)` generates the second integer
cohomology of `\CC\mathbf{P}^1`.

.. _Pfaffian:

Pfaffian Classes
----------------

Usually, there is no such thing as "Pfaffian classes" in literature. However,
using the matrix' Pfaffian and inspired by the aforementioned definitions,
such classes can be defined as follows.

Let `E` be a real vector bundle of rank `2n` and `f` an odd real function
being analytic at zero. Furthermore, let `\Omega` be skew-symmetric, which
certainly will be true if `\nabla` is metric and `e` is orthonormal. Then
we call

.. MATH::

    \left[\mathrm{Pf}\left( f\left( \frac{\Omega}{2 \pi} \right) \right)\right]
        \in H^{2n*}(M,\RR)

the *Pfaffian class associated to f*.

The most important Pfaffian class is the *Euler class* which is simply given by
`f(x)=x`.

EXAMPLES:

We consider the **Euler class** of `S^2`::

    sage: M = Manifold(2, name='S2', latex_name=r'S^2', start_index=1)
    sage: U = M.open_subset('U') ; V = M.open_subset('V')
    sage: M.declare_union(U,V)   # M is the union of U and V
    sage: c_xy.<x,y> = U.chart() ; c_uv.<u,v> = V.chart()
    sage: xy_to_uv = c_xy.transition_map(c_uv,
    ....:                                (x/(x^2+y^2), y/(x^2+y^2)),
    ....:                               intersection_name='W',
    ....:                               restrictions1= x^2+y^2!=0,
    ....:                               restrictions2= u^2+v^2!=0)
    sage: uv_to_xy = xy_to_uv.inverse()
    sage: eU = c_xy.frame() ; eV = c_uv.frame()
    sage: TM = M.tangent_bundle()
    sage: e_class = TM.char_class('Euler'); e_class
    Characteristic class e of Pfaffian type associated to x on the Tangent
     bundle TS2 over the 2-dimensional differentiable manifold S2

To compute a particular representative of the Euler class, we need to determine
a connection::

    sage: g = M.metric('g') # standard metric on S2
    sage: g[eU,1,1], g[eU,2,2] = 4/(1+x^2+y^2)^2, 4/(1+x^2+y^2)^2
    sage: g[eV,1,1], g[eV,2,2] = 4/(1+u^2+v^2)^2, 4/(1+u^2+v^2)^2
    sage: nab = g.connection()

In case of the the Euler class, skew-symmetric curvature matrices are needed
for the Pfaffian. For this, we need to define the curvature matrices by
hand::

    sage: cmatrix_U = [[nab.curvature_form(i,j,eU) for j in TM.irange()]
    ....:               for i in TM.irange()]
    sage: cmatrix_V = [[nab.curvature_form(i,j,eV) for j in TM.irange()]
    ....:               for i in TM.irange()]

Fortunately, both curvature matrices are already skew-symmetric::

    sage: for i in range(TM.rank()):
    ....:    for j in range(TM.rank()):
    ....:        print(cmatrix_U[i][j].display())
    curvature (1,1) of connection nabla_g w.r.t. Coordinate frame
     (U, (d/dx,d/dy)) = 0
    curvature (1,2) of connection nabla_g w.r.t. Coordinate frame
     (U, (d/dx,d/dy)) = 4/(x^4 + y^4 + 2*(x^2 + 1)*y^2 + 2*x^2 + 1) dx/\dy
    curvature (2,1) of connection nabla_g w.r.t. Coordinate frame
     (U, (d/dx,d/dy)) = -4/(x^4 + y^4 + 2*(x^2 + 1)*y^2 + 2*x^2 + 1) dx/\dy
    curvature (2,2) of connection nabla_g w.r.t. Coordinate frame
     (U, (d/dx,d/dy)) = 0
    sage: for i in range(TM.rank()):
    ....:    for j in range(TM.rank()):
    ....:        print(cmatrix_V[i][j].display())
    curvature (1,1) of connection nabla_g w.r.t. Coordinate frame
     (V, (d/du,d/dv)) = 0
    curvature (1,2) of connection nabla_g w.r.t. Coordinate frame
     (V, (d/du,d/dv)) = 4/(u^4 + v^4 + 2*(u^2 + 1)*v^2 + 2*u^2 + 1) du/\dv
    curvature (2,1) of connection nabla_g w.r.t. Coordinate frame
     (V, (d/du,d/dv)) = -4/(u^4 + v^4 + 2*(u^2 + 1)*v^2 + 2*u^2 + 1) du/\dv
    curvature (2,2) of connection nabla_g w.r.t. Coordinate frame
     (V, (d/du,d/dv)) = 0

Now the representative of the Euler class with respect to the connection
`\nabla_g` induced by the standard metric can be computed::

    sage: cmatrices = {eU: cmatrix_U, eV: cmatrix_V}
    sage: e_class_form = e_class.get_form(nab, cmatrices)
    sage: e_class_form.display_expansion()
    e(TS2, nabla_g) = [0] + [0] + [2/(pi + pi*x^4 + pi*y^4 + 2*pi*x^2 +
     2*(pi + pi*x^2)*y^2) dx/\dy]

Let us check whether this form represents the Euler class correctly::

    sage: integrate(integrate(e_class_form[2][[1,2]].expr(), x, -infinity, infinity).simplify_full(),
    ....:           y, -infinity, infinity)
    2

As we can see, the integral coincides with the Euler characteristic of `S^2` so
that our form actually represents the Euler class appropriately.

.. _documentation:

Class Documentation
-------------------
"""

#******************************************************************************
#       Copyright (C) 2019 Michael Jung <micjung@uni-potsdam.de>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
#******************************************************************************

from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.sage_object import SageObject

################################################################################
## Static methods

def _get_predefined_class(arg):
    r"""
    Return the signature of the predefined class given by the string `arg`.

    The signature is given by a tuple following the syntax
    (base field, class type, name, LaTeX name, function).

    Modify this method to add new predefined characteristic classes.

    TESTS::

        sage: from sage.manifolds.differentiable.char_class import _get_predefined_class
        sage: _get_predefined_class('Chern')
        ('complex', 'multiplicative', 'c', 'c', x + 1)
        sage: _get_predefined_class('Pontryagin')
        ('real', 'multiplicative', 'p', 'p', x + 1)
        sage: _get_predefined_class('Euler')
        ('real', 'Pfaffian', 'e', 'e', x)

    """
    if not isinstance(arg, str):
        raise TypeError("argument 'arg' must be string")

    from sage.symbolic.ring import SR
    # Define variable:
    x = SR.symbol('x')
    # Define dictionary. The syntax is as follows:
    # (field_type, class_type, name, latex_name, func)
    c_dict = {}
    c_dict['ChernChar'] = ('complex', 'additive', 'ch', r'\mathrm{ch}', x.exp())
    c_dict['Todd'] = ('complex', 'additive', 'Td', r'\mathrm{Td}',
                      x / (1 - (-x).exp()))
    c_dict['Chern'] = ('complex', 'multiplicative', 'c', 'c', 1 + x)
    c_dict['Pontryagin'] = ('real', 'multiplicative', 'p', 'p', 1 + x)
    c_dict['AHat'] = ('real', 'multiplicative', 'A^', r'\hat{A}',
                      x.sqrt() / (2 * (x.sqrt() / 2).sinh()))
    c_dict['Hirzebruch'] = ('real', 'multiplicative', 'L', 'L',
                            (x.sqrt() / x.sqrt().tanh()))
    c_dict['Euler'] = ('real', 'Pfaffian', 'e', 'e', x)
    # Get class from arg
    try:
        res = c_dict[arg]
    except KeyError:
        raise ValueError("the characteristic class '{}' is ".format(arg) +
                         "not predefined yet.")
    return res

################################################################################
## Classes

class CharClass(SageObject, UniqueRepresentation):
    r"""
    An instance of this class represents a characteristic class on some
    differentiable vector bundle over the field `\RR` or `\CC`.

    INPUT:

    - vbundle -- vector bundle on which the characteristic class should be
      defined
    - func -- symbolic expression representing the function to which ``self``
      should be associated to
    - class_type -- (default: ``'multiplicative'``) class type of the
      characteristic class; at this stage, the following options are possible:

      - ``'multiplicative'`` -- returns a class of multiplicative type,
        using the determinant
      - ``'additive'`` -- returns a class of additive type, using the trace
      - ``'Pfaffian'`` -- returns a class of Pfaffian type, using the
        Pfaffian

    - ``name`` -- string representation given to the characteristic class
    - ``latex_name`` -- (default: ``None``) LaTeX name given to the
      characteristic class

    EXAMPLES:

    Get characteristic classes using predefined ones::

        sage: M = Manifold(4, 'M')
        sage: TM = M.tangent_bundle()
        sage: TM.char_class('Pontryagin')
        Characteristic class p of multiplicative type associated to x + 1 on the
         Tangent bundle TM over the 4-dimensional differentiable manifold M
        sage: TM.char_class('Hirzebruch')
        Characteristic class L of multiplicative type associated to
         sqrt(x)/tanh(sqrt(x)) on the Tangent bundle TM over the 4-dimensional
         differentiable manifold M
        sage: TM.char_class('AHat')
        Characteristic class A^ of multiplicative type associated to
         1/2*sqrt(x)/sinh(1/2*sqrt(x)) on the Tangent bundle TM over the
         4-dimensional differentiable manifold M

    The vector bundle's base field and definition domain of the characteristic
    class must fit together, otherwise an error message occurs::

        sage: TM.char_class('Chern')
        Traceback (most recent call last):
        ...
        ValueError: base field must be complex for class 'Chern'

    If your favourite class is not predefined yet, the associated function can
    be put manually::

        sage: cl = TM.char_class(1+x^2, name='cl'); cl
        Characteristic class cl of multiplicative type associated to x^2 + 1 on
         the Tangent bundle TM over the 4-dimensional differentiable manifold M

    """
    def __init__(self, vbundle, func, class_type='multiplicative', name=None,
                 latex_name=None):
        r"""
        Construct a characteristic class.

        TESTS::

            sage: M = Manifold(3, 'M')
            sage: TM = M.tangent_bundle()
            sage: from sage.manifolds.differentiable.char_class import CharClass
            sage: c = CharClass(TM, 1+x, name='c'); c
            Characteristic class c of multiplicative type associated to x + 1 on
             the Tangent bundle TM over the 3-dimensional differentiable
             manifold M
            sage: TestSuite(c).run()

        """
        if vbundle._field_type == 'neither_real_nor_complex':
            raise ValueError("the vector bundle must either be real or complex")
        if class_type not in ['additive', 'multiplicative', 'Pfaffian']:
            raise ValueError("the argument 'class_type' must either be "
                             "'additive', 'multiplicative' or 'Pfaffian'")
        if class_type == 'Pfaffian':
            if vbundle._field_type != 'real' or vbundle._rank % 2 != 0:
                raise ValueError("Pfaffian classes can only be defined for real"
                                 " vector bundles of even rank")
        self._name = name
        if latex_name is None:
            self._latex_name = name
        else:
            self._latex_name = latex_name
        self._func = func
        self._class_type = class_type
        self._vbundle = vbundle
        self._base_space = vbundle._base_space
        self._rank = vbundle._rank
        self._coeff_list = self._get_coeff_list()
        self._init_derived()

    def _get_coeff_list(self):
        r"""
        Return the list of coefficients of the Taylor expansion at zero of the
        function.

        TESTS::

            sage: M = Manifold(2, 'M')
            sage: E = M.vector_bundle(1, 'E', field='complex')
            sage: c = E.char_class(1+x)
            sage: c._get_coeff_list()
            [1, 1]

        """
        pow_range = (self._base_space._dim / 2).floor()
        from sage.symbolic.ring import SR
        def_var = self._func.default_variable()
        # Use a complex variable without affecting the old one:
        new_var = SR.symbol('x_char_class_', domain='complex')
        if self._vbundle._field_type == 'real':
            if self._class_type == 'additive':
                func = self._func.subs({def_var: new_var ** 2}) / 2
            elif self._class_type == 'multiplicative':
                # This could case problems in the real domain, where sqrt(x^2)
                # is simplified to |x|. However, the variable must be complex
                # anyway.
                func = self._func.subs({def_var : new_var**2}).sqrt()
            elif self._class_type == 'Pfaffian':
                # There are no canonical Pfaffian classes, however, consider the
                # projection onto the odd part of the function to keep the
                # matrices skew:
                func = (self._func.subs({def_var: new_var}) -
                        self._func.subs({def_var: -new_var})) / 2
        else:
            func = self._func.subs({def_var: new_var})
        coef = func.taylor(new_var, 0, pow_range).coefficients(sparse=False)

        return coef

    def _init_derived(self):
        r"""
        Initialize the derived quantities.

        TESTS::

            sage: M = Manifold(2, 'M')
            sage: TM = M.tangent_bundle()
            sage: c = TM.char_class(1+x)
            sage: c._init_derived()

        """
        self._mixed_forms = {}  # dict. of mixed forms corresponding this
                                # characteristic class
                                # (key: bundle connection)

    def _del_derived(self):
        r"""
        Delete the derived quantities.

        TESTS::

            sage: M = Manifold(2, 'M')
            sage: TM = M.tangent_bundle()
            sage: c = TM.char_class(1+x)
            sage: c._del_derived()

        """
        self._mixed_forms.clear()

    def _repr_(self):
        r"""
        String representation of the object.

        TESTS::

            sage: M = Manifold(2, 'M')
            sage: TM = M.tangent_bundle()
            sage: c = TM.char_class(1+x, name='c')
            sage: c # indirect doctest
            Characteristic class c of multiplicative type associated to x + 1 on
             the Tangent bundle TM over the 2-dimensional differentiable
             manifold M
            sage: repr(c) # indirect doctest
            'Characteristic class c of multiplicative type associated to x + 1
             on the Tangent bundle TM over the 2-dimensional differentiable
             manifold M'
            sage: c._repr_()
            'Characteristic class c of multiplicative type associated to x + 1
             on the Tangent bundle TM over the 2-dimensional differentiable
             manifold M'

        """
        desc = "Characteristic class "
        if self._name is not None:
            desc += self._name + " "
        desc += "of {} type ".format(self._class_type)
        desc += "associated to {} on the {}".format(self._func, self._vbundle)
        return desc

    def _latex_(self):
        r"""
        LaTeX representation of the object.

        TESTS::

            sage: M = Manifold(2, 'M')
            sage: TM = M.tangent_bundle()
            sage: ch = TM.char_class(exp(x), class_type='additive',  name='ch',
            ....:                    latex_name=r'\mathrm{ch}')
            sage: ch._latex_()
            '\\mathrm{ch}(TM)'

        """
        return self._latex_name + "(" + self._vbundle._latex_name + ")"

    def class_type(self):
        r"""
        Return the class type of ``self``.

        EXAMPLES::

            sage: M = Manifold(2, 'M')
            sage: TM = M.tangent_bundle()
            sage: ch = TM.char_class(exp(x), class_type='additive',  name='ch',
            ....:                    latex_name=r'\mathrm{ch}')
            sage: ch.class_type()
            'additive'

        """
        return self._class_type

    def function(self):
        r"""
        Return the function corresponding to this characteristic class.

        EXAMPLES::

            sage: M = Manifold(2, 'M')
            sage: TM = M.tangent_bundle()
            sage: e_class = TM.char_class('Euler')
            sage: e_class.function()
            x
            sage: AHat = TM.char_class('AHat')
            sage: AHat.function()
            1/2*sqrt(x)/sinh(1/2*sqrt(x))
            sage: c = TM.char_class(1+x, name='c')
            sage: c.function()
            x + 1

        """
        return self._func

    def get_form(self, con, cmatrices=None):
        r"""
        Return the form representing ``self`` with respect to the given
        connection ``con``.

        INPUT:

        - ``con`` -- connection to which the form should be associated to; this
          can be either a bundle connection as an instance of
          :class:`~sage.manifolds.differentiable.bundle_connection.BundleConnection`
          or, in case of the tensor bundle, an affine connection as an instance
          of :class:`~sage.manifolds.differentiable.affine_connection.AffineConnection`
        - ``cmatrices`` -- (default: ``None``) a dictionary of curvature
          matrices with local frames as keys and curvature matrices as items; if
          ``None``, SAGE tries to get the curvature matrices from the connection

        OUTPUT:

        - mixed form as an instance of
          :class:`~sage.manifolds.differentiable.mixed_form.MixedForm`
          representing the total characteristic class

        .. NOTE::

            Be aware that depending on the characteristic class and complexity
            of the manifold, computation times may vary a lot. In addition, if
            not done before, the curvature form is computed from the connection,
            here. If this behaviour is not wanted and the curvature form is
            already known, please use the argument ``cmatrices``.

        EXAMPLES:

        Again, consider the Chern character on some 2-dimensional spacetime::

            sage: M = Manifold(2, 'M', structure='Lorentzian')
            sage: X.<t,x> = M.chart()
            sage: E = M.vector_bundle(1, 'E', field='complex'); E
            Differentiable complex vector bundle E -> M of rank 1 over the base space
             2-dimensional Lorentzian manifold M
            sage: e = E.local_frame('e')

        And again, we define the connection `\nabla^E` in terms of an
        electro-magnetic potential `A(t)`::

            sage: nab = E.bundle_connection('nabla^E', latex_name=r'\nabla^E')
            sage: omega = M.one_form(name='omega')
            sage: A = function('A')
            sage: omega[1] = I*A(t)
            sage: omega.display()
            omega = I*A(t) dx
            sage: nab.set_connection_form(0, 0, omega)

        The Chern character is then given by::

            sage: ch = E.char_class('ChernChar'); ch
            Characteristic class ch of additive type associated to e^x on the
             Differentiable complex vector bundle E -> M of rank 1 over the base space
             2-dimensional Lorentzian manifold M

        Inserting the connection, the result is a mixed differential form with
        a priori non-zero components in even degrees::

            sage: ch_form = ch.get_form(nab); ch_form
            Mixed differential form ch(E, nabla^E) on the 2-dimensional
             Lorentzian manifold M
            sage: ch_form.display()
            ch(E, nabla^E) = ch_0(E, nabla^E) + zero + ch_1(E, nabla^E)
            sage: ch_form.display_expansion()
            ch(E, nabla^E) = [1] + [0] + [1/2*d(A)/dt/pi dt/\dx]

        Due to long computation times, the form is saved::

            sage: ch_form is ch.get_form(nab)
            True

        """
        from .bundle_connection import BundleConnection
        from .affine_connection import AffineConnection
        if not isinstance(con, (AffineConnection, BundleConnection)):
            raise TypeError("argument must be an affine connection on the "
                            "manifold or bundle connection on the vector "
                            "bundle")
        if con not in self._mixed_forms:
            if cmatrices is None:
                if self._class_type == 'Pfaffian':
                    raise NotImplementedError(
                        "At this stage, Pfaffian forms cannot be derived from "
                        "(metric) connections. Please use the argument "
                        "'cmatrices' to insert a dictionary of skew-symmetric "
                        "curvature matrices by hand, instead.")
                cmatrices = {}
                for frame in self._get_min_frames(con._coefficients.keys()):
                    cmatrix = [[con.curvature_form(i, j, frame)
                                    for j in self._vbundle.irange()]
                                        for i in self._vbundle.irange()]
                    cmatrices[frame] = cmatrix
            # Prepare mixed form:
            name, latex_name = self._name, self._latex_name
            if name is not None and con._name is not None:
                name += "(" + self._vbundle._name + ", " + con._name + ")"
            if latex_name is not None and con._latex_name is not None:
                latex_name += "(" + self._vbundle._latex_name + ", " + \
                              con._latex_name + ")"
            res = self._base_space.mixed_form(name=name, latex_name=latex_name)
            # Set name of homogeneous components:
            #
            # Only even (or in the real case, by four divisible) degrees are
            # non-zero:
            if self._class_type == 'Pfaffian':
                deg_dist = self._rank
            elif self._vbundle._field_type == 'real':
                deg_dist = 4
            elif self._vbundle._field_type == 'complex':
                deg_dist = 2
            else:
            # You never know...
                deg_dist = 1
            # Now, define the name for each form:
            for k in res.irange():
                if k % deg_dist != 0 or (self._class_type == 'Pfaffian' and
                                         k == 0):
                    res[k].set_name(name="zero", latex_name="0")
                    res[k]._is_zero = True
                else:
                    if self._name is not None:
                        name = self._name + "_" + str(k / deg_dist) + \
                               "(" + self._vbundle._name
                        if con._name is not None:
                            name += ", " + con._name
                        name += ")"
                    # LaTeX name:
                    if self._latex_name is not None:
                        latex_name = self._latex_name + \
                                     r"_{" + str(k / deg_dist) + r"}" + \
                                     r"(" + self._vbundle._latex_name
                        if con._latex_name is not None:
                            latex_name += r", " + con._latex_name
                        latex_name += r")"
                    # Set name:
                    res[k].set_name(name=name, latex_name=latex_name)
                    res[k]._is_zero = False # a priori
            # Begin computation:
            from sage.matrix.matrix_space import MatrixSpace
            for frame, cmatrix in cmatrices.items():
                # Define matrix space:
                dom = frame._domain
                alg = dom.mixed_form_algebra()
                mspace = MatrixSpace(alg, self._rank)
                # Insert "normalized" curvature matrix into polynomial:
                cmatrix = mspace(cmatrix)  # convert curvature matrix
                ncmatrix = self._normalize_matrix(cmatrix)
                rmatrix = self._insert_in_polynomial(ncmatrix)
                # Compute classes:
                if self._class_type == 'additive':
                    rst = rmatrix.trace()  # mixed form
                elif self._class_type == 'multiplicative':
                    rst = rmatrix.det()  # mixed form
                elif self._class_type == 'Pfaffian':
                    rst = rmatrix.pfaffian()  # mixed form
                # Set restriction:
                res.set_restriction(rst)

            self._mixed_forms[con] = res

        return self._mixed_forms[con]

    def _insert_in_polynomial(self, cmatrix):
        r"""
        Return the matrix after inserting `cmatrix` into the polynomial given by
        the taylor expansion of `self._func`.

        TESTS::

            sage: M = Manifold(4, 'M')
            sage: c = M.tangent_bundle().char_class('Pontryagin')
            sage: c._insert_in_polynomial(x)
            1/2*x^2 + 1

        """
        mspace = cmatrix.parent()
        # Compute matrix powers:
        power_list = [mspace.one()]
        for pow in range(len(self._coeff_list) - 1):
            power_list.append(cmatrix * power_list[pow])
        # Put things together:
        rmatrix = sum(self._coeff_list[k] * power_list[k]
                      for k in range(len(self._coeff_list)))

        return rmatrix

    def _normalize_matrix(self, cmatrix):
        r"""
        Return the curvature matrix "normalized" with `i/(2 \pi)` or `1/(2 \pi)`
        respectively.

        INPUT:

        - ``cmatrix`` curvature matrix

        OUTPUT:

        - ``I/(2*pi)*cmatrix``

        TESTS::

            sage: M = Manifold(2, 'M')
            sage: TM = M.tangent_bundle()
            sage: c = TM.char_class(1+x)
            sage: c._normalize_matrix(x)
            -1/2*I*x/pi

        """
        from sage.symbolic.constants import pi
        fac = 1 / (2 * pi)
        if self._class_type != 'Pfaffian':
            from sage.libs.pynac.pynac import I
            fac = fac / I
        return fac * cmatrix

    def _get_min_frames(self, frame_list):
        r"""
        Return the minimal amount of frames necessary to cover the union of all
        frame's domains.

        INPUT:

        - list of frames

        OUTPUT:

        - set of frames

        TESTS::

            sage: M = Manifold(2, 'M')
            sage: U = M.open_subset('U'); V = M.open_subset('V')
            sage: e = U.vector_frame('e'); f = V.vector_frame('f')
            sage: g = M.vector_frame('g')
            sage: c = M.tangent_bundle().char_class('Pontryagin')
            sage: c._get_min_frames([e, f, g])
            {Vector frame (M, (g_0,g_1))}

        """
        min_frame_set = set()
        for frame in frame_list:
            redund_frame_set = set()
            for oframe in min_frame_set:
                if frame._domain.is_subset(oframe._domain):
                    break
                elif oframe._domain.is_subset(frame._domain):
                    redund_frame_set.add(oframe)
            else:
                min_frame_set.add(frame)
            min_frame_set.difference_update(redund_frame_set)
        return min_frame_set
