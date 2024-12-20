
"""
compares gridsearch and newton's method efficiency in locating a functions local min
"""

name = ['jebucher@calpoly.edu']

# f(x) takes a list of length two, where both elements are flotes
    # computes f: R2 -> R1
# f1(x) computes the gradients of f for the value x
    # returns two floats
# f2(x) computes the second derivative. List of length four with
    # [f11, f12, f21, f22]

def gridsearch(xmin: list, xmax: list, p,f):

    """
    computes the x-value that leads to maximum of f on the interval
    xmin, xmax using gridsearch method

    """
    x = xmin[0]
    y = xmin[1]
    working_max = - float('inf')
    numf = 0

    # need to iterate over every value of y for each x (a grid)
    while x <= xmax[0]:

        while y <= xmax[1]:
            f_val = f([x, y])
            if f_val > working_max:
                working_max = f_val
                x_value = [x, y]
            y += p
            numf += 1

        y = xmin[1]
        x += p

    return x_value, numf


# define a norm function
def norm(lst: list) -> float:
    norm_sq = sum([x ** 2 for x in lst])
    return norm_sq ** 0.5


# matrix inverse for 2 x 2
def matrix_inv(hess: list) -> list:

    det = hess[0] * hess[3] - hess[1] * hess[2]

    # check for invertibility
    if det == 0:
        return "matrix not invertible"
        
    inverse = [hess[3], - hess[1], -hess[2], hess[0]]

    inverse = [(1 / det) * x for x in inverse]

    return inverse

# define matrix mult for for 2 x 2 and 1 x 2
def matrix_mult(mat: list, vec: list) -> list:

    ret_vec = [(mat[0] * vec[0] + mat[1] * vec[1]), 
                   (mat[2] * vec[0] + mat[3] * vec[1])]
        
    return ret_vec


def newton(xinit, e, f, f1, f2):

    x = xinit[0]
    y = xinit[1]
    numf = 0

    # continue until the norm of the hessian is equal to 0
    while norm(f1([x, y])) > e:

        # new guess = (old guess) - (H-1(old guess) * Grad(old guess))
        compute = matrix_mult(matrix_inv(f2([x, y])), f1([x, y]))
        x -= compute[0]
        y -= compute[1]

        # function f1 called twice, function f2 called once
        numf += 3
    
    x_value = [x, y]
    return x_value, numf
