import pytest
import math
import optimization as op

# testing grid search

def f1_test(x: list) -> float:
    x, y = (x[0], x[1])
    return x - y

# def test_gridsearch():

    # assert math.isclose(op.gridsearch([0, 0], [10, 10], 0.1, f1_test)[0][1], 10, rel_tol = 0.01)

    # assert math.isclose(op.gridsearch([-10, -10], [0, 0], 0.01, f1_test)[0][0], -10, rel_tol = 0.01)

test_vec = [0, 1, 2, 3, 1 , 1]

def test_norm():

    assert op.norm(test_vec) == 4


test_mat1 = [1, 1, 1, 1]

test_mat2 = [1, 2, 3, 4]

def test_matrix_inv():
    
    assert op.matrix_inv(test_mat1) == "matrix not invertible"

    assert op.matrix_inv(test_mat2) == [-2, 1, (3 / 2), -(1 / 2)]


test_vec1 = [1, 1]

def test_matrix_mult():

    assert op.matrix_mult(test_mat1, test_vec1) == [2, 2]


def f_test(x: list) -> list: 

    return x[0] ** 2 - x[1] ** 2

def second_f1_test(x: list) -> list:
    return [2 * x[0], -2 * x[1]]

def f2_test(x: list) -> list:
    return [2, 0, 0, -2]

# Function definition
def f_test2(x: list) -> float:
    return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2

# Gradient
def second_f1_test2(x: list) -> list:
    return [-2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0] ** 2),
            200 * (x[1] - x[0] ** 2)]

# Hessian
def f2_test2(x: list) -> list:
    return [
        1200 * x[0] ** 2 - 400 * x[1] + 2, -400 * x[0],
        -400 * x[0], 200
    ]


def test_newton():

    assert math.isclose(op.newton([-5, 10], 0.001, f_test, second_f1_test, f2_test)[0][0], 0, rel_tol = 0.01)

    assert math.isclose(op.newton([10, 5], 0.001, f_test, second_f1_test, f2_test)[0][1], 0, rel_tol = 0.01)

    print(op.newton([10, 10], 0.001, f_test, second_f1_test, f2_test))

    assert math.isclose(op.newton([10, -10], 0.001, f_test2, second_f1_test2, f2_test2)[0][0], 1, rel_tol = 0.01)

    assert math.isclose(op.newton([-10, 10], 0.001, f_test2, second_f1_test2, f2_test2)[0][1], 1, rel_tol = 0.01)

