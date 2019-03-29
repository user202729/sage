## -*- encoding: utf-8 -*-
"""
This file (./sol/calculus_doctest.sage) was *autogenerated* from ./sol/calculus.tex,
with sagetex.sty version 2011/05/27 v2.3.1.
It contains the contents of all the sageexample environments from this file.
You should be able to doctest this file with:
sage -t ./sol/calculus_doctest.sage
It is always safe to delete this file; it is not used in typesetting your
document.

Sage example in ./sol/calculus.tex, line 3::

  sage: reset()

Sage example in ./sol/calculus.tex, line 10::

  sage: n = var('n'); pmax = 4; s = [n + 1]
  sage: for p in [1..pmax]:
  ....:     s += [factor(((n+1)^(p+1) - sum(binomial(p+1, j) * s[j]
  ....:           for j in [0..p-1])) / (p+1))]
  sage: s
  [n + 1,
   1/2*(n + 1)*n,
   1/6*(2*n + 1)*(n + 1)*n,
   1/4*(n + 1)^2*n^2,
   1/30*(3*n^2 + 3*n - 1)*(2*n + 1)*(n + 1)*n]

Sage example in ./sol/calculus.tex, line 42::

  sage: x, h, a = var('x, h, a'); f = function('f')
  sage: g(x) = taylor(f(x), x, a, 3)
  sage: phi(h) = (g(a+3*h) - 3*g(a+2*h) + 3*g(a+h) - g(a)) / h^3; phi(h)
  diff(f(a), a, a, a)

Sage example in ./sol/calculus.tex, line 75::

  sage: n = 7; x, h, a = var('x h a'); f = function('f')
  sage: g(x) = taylor(f(x), x, a, n)
  sage: sum((-1)^(n-k) * binomial(n,k) * g(a+k*h) for k in (0..n)) / h^n
  diff(f(a), a, a, a, a, a, a, a)

Sage example in ./sol/calculus.tex, line 100::

  sage: theta = 12*arctan(1/38) + 20*arctan(1/57) \
  ....:       + 7*arctan(1/239) + 24*arctan(1/268)
  sage: tan(theta).trig_expand().trig_simplify()
  1

Sage example in ./sol/calculus.tex, line 110::

  sage: 12*(1/38) + 20*(1/57) + 7*(1/239) + 24*(1/268)
  37735/48039

Sage example in ./sol/calculus.tex, line 135::

  sage: x = var('x'); f(x) = taylor(arctan(x), x, 0, 21)
  sage: approx = 4 * (12 * f(1/38) + 20 * f(1/57)
  ....:           + 7 * f(1/239) + 24 * f(1/268))
  sage: approx.n(digits = 50); pi.n(digits = 50)
  3.1415926535897932384626433832795028851616168852864
  3.1415926535897932384626433832795028841971693993751
  sage: approx.n(digits = 50) - pi.n(digits = 50)
  9.6444748591132486785420917537404705292978817080880e-37

Sage example in ./sol/calculus.tex, line 182::

  sage: n = var('n'); phi = lambda x: n*pi + pi/2 - arctan(1/x)
  sage: x = n*pi
  sage: for i in range(4):
  ....:    x = taylor(phi(x), n, infinity, 2*i); x
  1/2*pi + pi*n
  1/2*pi + pi*n - 1/(pi*n) + 1/2/(pi*n^2)
  1/2*pi + pi*n - 1/(pi*n) + 1/2/(pi*n^2)
    - 1/12*(3*pi^2 + 8)/(pi^3*n^3) + 1/8*(pi^2 + 8)/(pi^3*n^4)
  1/2*pi + pi*n - 1/(pi*n) + 1/2/(pi*n^2)
    - 1/12*(3*pi^2 + 8)/(pi^3*n^3) + 1/8*(pi^2 + 8)/(pi^3*n^4)
    - 1/240*(15*pi^4 + 240*pi^2 + 208)/(pi^5*n^5)
    + 1/96*(3*pi^4 + 80*pi^2 + 208)/(pi^5*n^6)

Sage example in ./sol/calculus.tex, line 239::

  sage: h = var('h'); f(x, y) = x * y * (x^2 - y^2) / (x^2 + y^2)
  sage: D1f(x, y) = diff(f(x,y), x); limit((D1f(0,h) - 0) / h, h=0)
  -1
  sage: D2f(x, y) = diff(f(x,y), y); limit((D2f(h,0) - 0) / h, h=0)
  1
  sage: g = plot3d(f(x, y), (x, -3, 3), (y, -3, 3))

Sage example in ./sol/calculus.tex, line 285::

  sage: n, t = var('n, t')
  sage: v(n) = (4/(8*n+1)-2/(8*n+4)-1/(8*n+5)-1/(8*n+6))*1/16^n
  sage: assume(8*n+1>0)
  sage: f(t) = 4*sqrt(2)-8*t^3-4*sqrt(2)*t^4-8*t^5
  sage: u(n) = integrate(f(t) * t^(8*n), t, 0, 1/sqrt(2))
  sage: (u(n)-v(n)).canonicalize_radical()
  0

Sage example in ./sol/calculus.tex, line 317::

  sage: t = var('t'); J = integrate(f(t) / (1-t^8), t, 0, 1/sqrt(2))
  sage: J.canonicalize_radical()
  pi + 2*log(sqrt(2) + 1) + 2*log(sqrt(2) - 1)

Sage example in ./sol/calculus.tex, line 325::

  sage: J.simplify_log().canonicalize_radical()
  pi

Sage example in ./sol/calculus.tex, line 337::

  sage: l = sum(v(n) for n in (0..40)); l.n(digits=60)
  3.14159265358979323846264338327950288419716939937510581474759
  sage: pi.n(digits=60)
  3.14159265358979323846264338327950288419716939937510582097494
  sage: print("%e" % (l-pi).n(digits=60))
  -6.227358e-54

Sage example in ./sol/calculus.tex, line 369::

  sage: x = var('x'); ps = lambda f, g : integral(f * g, x, -pi, pi)
  sage: n = 5; a = var('a0, a1, a2, a3, a4, a5')
  sage: P = sum(a[k] * x^k for k in (0..n))
  sage: equ = [ps(P - sin(x), x^k) for k in (0..n)]
  sage: sol = solve(equ, a)
  sage: P = sum(sol[0][k].rhs() * x^k for k in (0..n)); P
  105/8*(pi^4 - 153*pi^2 + 1485)*x/pi^6 - 315/4*(pi^4 - 125*pi^2 +
  1155)*x^3/pi^8 + 693/8*(pi^4 - 105*pi^2 + 945)*x^5/pi^10
  sage: g = plot(P,x,-6,6,color='red') + plot(sin(x),x,-6,6,color='blue')
  sage: g.show(ymin = -1.5, ymax = 1.5)

Sage example in ./sol/calculus.tex, line 430::

  sage: p, e = var('p, e')
  sage: theta1, theta2, theta3 = var('theta1, theta2, theta3')
  sage: r(theta) = p / (1 - e * cos(theta))
  sage: r1 = r(theta1); r2 = r(theta2); r3 = r(theta3)
  sage: R1 = vector([r1 * cos(theta1), r1 * sin(theta1), 0])
  sage: R2 = vector([r2 * cos(theta2), r2 * sin(theta2), 0])
  sage: R3 = vector([r3 * cos(theta3), r3 * sin(theta3), 0])

Sage example in ./sol/calculus.tex, line 446::

  sage: D = R1.cross_product(R2)+R2.cross_product(R3)+R3.cross_product(R1)
  sage: S = (r1 - r3) * R2 + (r3 - r2) * R1 + (r2 - r1) * R3
  sage: i = vector([1, 0, 0]); V =  S + e * i.cross_product(D)
  sage: V.simplify_full()
  (0, 0, 0)

Sage example in ./sol/calculus.tex, line 466::

  sage: S.cross_product(D).simplify_full()[1:3]
  (0, 0)

Sage example in ./sol/calculus.tex, line 479::

  sage: N = r3 * R1.cross_product(R2) + r1 * R2.cross_product(R3)\
  ....:   + r2 * R3.cross_product(R1)
  sage: W = p * S + e * i.cross_product(N)
  sage: W.simplify_full()
  (0, 0, 0)

Sage example in ./sol/calculus.tex, line 504::

  sage: R1=vector([0,1,0]); R2=vector([2,2,0]); R3=vector([3.5,0,0])
  sage: r1 = R1.norm(); r2 = R2.norm(); r3 = R3.norm()
  sage: D = R1.cross_product(R2) + R2.cross_product(R3) \
  ....:   + R3.cross_product(R1)
  sage: S = (r1 - r3) * R2 + (r3 - r2) * R1 + (r2 - r1) * R3
  sage: N = r3 * R1.cross_product(R2) + r1 * R2.cross_product(R3) \
  ....:   + r2 * R3.cross_product(R1)
  sage: e = S.norm() / D.norm(); p = N.norm() / D.norm()
  sage: a = p/(1-e^2); c = a * e; b = sqrt(a^2 - c^2)
  sage: X = S.cross_product(D); i = X / X.norm()
  sage: phi = atan2(i[1], i[0]) * 180 / pi.n()
  sage: print("%.3f %.3f %.3f %.3f %.3f %.3f" % (a, b, c, e, p, phi))
  2.360 1.326 1.952 0.827 0.746 17.917

Sage example in ./sol/calculus.tex, line 544::

  sage: A = matrix(QQ, [[ 2,  -3,   2, -12, 33],
  ....:                 [ 6,   1,  26, -16, 69],
  ....:                 [10, -29, -18, -53, 32],
  ....:                 [ 2,   0,   8, -18, 84]])
  sage: A.right_kernel()
  Vector space of degree 5 and dimension 2 over Rational Field
  Basis matrix:
  [     1      0  -7/34   5/17   1/17]
  [     0      1  -3/34 -10/17  -2/17]

Sage example in ./sol/calculus.tex, line 571::

  sage: H = A.echelon_form(); H
  [ 1  0  4  0 -3]
  [ 0  1  2  0  7]
  [ 0  0  0  1 -5]
  [ 0  0  0  0  0]

Sage example in ./sol/calculus.tex, line 608::

  sage: A.column_space()
  Vector space of degree 4 and dimension 3 over Rational Field
  Basis matrix:
  [       1        0        0 1139/350]
  [       0        1        0    -9/50]
  [       0        0        1   -12/35]

Sage example in ./sol/calculus.tex, line 624::

  sage: S.<x, y, z, t> = QQ[]
  sage: C = matrix(S, 4, 1, [x, y, z, t])
  sage: B = block_matrix([A, C], ncols=2)
  sage: C = B.echelon_form()
  sage: C[3,5]*350
  -1139*x + 63*y + 120*z + 350*t

Sage example in ./sol/calculus.tex, line 643::

  sage: K = A.left_kernel(); K
  Vector space of degree 4 and dimension 1 over Rational Field
  Basis matrix:
  [        1  -63/1139 -120/1139 -350/1139]

Sage example in ./sol/calculus.tex, line 653::

  sage: matrix(K.0).right_kernel()
  Vector space of degree 4 and dimension 3 over Rational Field
  Basis matrix:
  [       1        0        0 1139/350]
  [       0        1        0    -9/50]
  [       0        0        1   -12/35]

Sage example in ./sol/calculus.tex, line 668::

  sage: A = matrix(QQ, [[-2, 1, 1], [8, 1, -5], [4, 3, -3]])
  sage: C = matrix(QQ, [[1, 2, -1], [2, -1, -1], [-5, 0, 3]])

Sage example in ./sol/calculus.tex, line 680::

  sage: B = C.solve_left(A); B
  [ 0 -1  0]
  [ 2  3  0]
  [ 2  1  0]

Sage example in ./sol/calculus.tex, line 691::

  sage: C.left_kernel()
  Vector space of degree 3 and dimension 1 over Rational Field
  Basis matrix:
  [1 2 1]

Sage example in ./sol/calculus.tex, line 699::

  sage: x, y, z = var('x, y, z'); v = matrix([[1, 2, 1]])
  sage: B = B + (x*v).stack(y*v).stack(z*v); B
  [      x 2*x - 1       x]
  [  y + 2 2*y + 3       y]
  [  z + 2 2*z + 1       z]

Sage example in ./sol/calculus.tex, line 708::

  sage: A == B*C
  True

"""

