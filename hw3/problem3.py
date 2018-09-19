import numpy as np
import math
#-------------------------------------------------------------------------
'''
    Problem 3: optimization-based recommender systems (collaborative filtering)
    In this problem, you will implement a version of the recommender system using optimization-based method.
    You could test the correctness of your code by typing `nosetests test3.py` in the terminal.
'''

#--------------------------
def update_U(R, V, U, beta=.001, mu=1.):
    '''
        Update the matrix U (movie factors) by fixing matrix V using gradient descent.
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If the rating is unknown, the number is 0.
            V: the user factor matrix, a numpy float matrix of shape k X n. Here n is the number of users.
            U: the current item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
            beta: step parameter for gradient descent, a float scalar
            mu: the parameter for regularization term, a float scalar
        Output:
            U: the updated item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
    '''

    #########################################
    ## INSERT YOUR CODE HERE

    # compute a binary matrix, representing the elements with known ratings
    binarize = np.vectorize(lambda x: 1 if x>0 else 0)
    B = binarize(R)

    L = np.multiply((np.subtract(R, np.matmul(U, V))), B)

    # compute the gradient of matrix U
    delta_U = -2 * np.matmul(L, np.transpose(V)) + 2 * mu * U


    # compute the updated matrix U
    U = np.subtract(U, beta * delta_U)

    #########################################
    return U

#--------------------------
def update_V(R, U, V, beta=.001, mu=1.):
    '''
        Update the matrix V (user factors) by fixing matrix U using gradient descent.
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If the rating is unknown, the number is 0.
            U: the item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
            V: the current user factor matrix, a numpy float matrix of shape k X n. Here n is the number of users.
            beta: step parameter for gradient descent, a float scalar
            mu: the parameter for regularization term, a float scalar
        Output:
            V: the updated item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
    '''
    #########################################
    ## INSERT YOUR CODE HERE

    # compute a binary matrix, representing the elements with known ratings
    binarize = np.vectorize(lambda x: 1 if x>0 else 0)
    B = binarize(R)

    L = np.multiply((np.subtract(R, np.matmul(U, V))), B)

    # compute the gradient of matrix V
    delta_V = -2 * np.matmul(np.transpose(U), L) + 2 * mu * V

    # compute the updated matrix U
    V = np.subtract(V, beta * delta_V)

    #########################################
    return V


#--------------------------
def matrix_decoposition(R, k=5, max_steps=1000000, beta=.01, mu=.01):
    '''
        Compute the matrix decomposition for optimization-based recommender system.
        Input:
            R: the rating matrix, a float numpy matrix of shape m by n. Here m is the number of movies, n is the number of users.
                If the rating is unknown, the number is 0.
            k: the number of latent factors for users and items.
            max_steps: the maximium number of steps for gradient descent.
            beta: step parameter for gradient descent, a float scalar
        Output:
            U: the item (movie) factor matrix, a numpy float matrix of shape m X k. Here m is the number of movies (items).
            V: the user factor matrix, a numpy float matrix of shape k X n. Here n is the number of users.
    '''

    # initialize U and V with random values
    n_movies, n_users = R.shape
    U = np.random.rand(n_movies, k)
    V = np.random.rand(k, n_users)

    #########################################
    ## INSERT YOUR CODE HERE
    # gradient descent

    for i in range(max_steps):
        # fix U, update V
        V = update_V(R, U, V, beta, mu)
        # fix V, update U
        U = update_U(R, V, U, beta, mu)

        if np.allclose(np.dot(U, V), R, atol=0.1):
            break


    #########################################
    return U, V

