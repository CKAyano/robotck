import copy

'''
    Pure Python/Numpy implementation of the Nelder-Mead algorithm.
    Reference: https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method
'''


def simplex(f, x_start,
            step=0.1, no_improve_thr=10e-6,
            no_improv_break=10, max_iter=0,
            alpha=1., beta=2., gamma=-0.5, delta=0.5,
            log_opt=False, print_opt=True):
    '''
        @param f (function): function to optimize, must return a scalar score
            and operate over a numpy array of the same dimensions as x_start
        @param x_start (numpy array): initial position
        @param step (float): look-around radius in initial step
        @no_improv_thr,  no_improv_break (float, int): break after no_improv_break iterations with
            an improvement lower than no_improv_thr
        @max_iter (int): always break after this number of iterations.
            Set it to 0 to loop indefinitely.
        @alpha, gamma, rho, sigma (floats): parameters of the algorithm.
            (see Wikipedia page for reference)
        @log_opt, is an option to choose whether to record the process as a list.
        return: tuple (best parameter array, best score, process log)
    '''

    # init
    dim = len(x_start)
    prev_best = f(x_start)
    no_improv = 0
    res = [[x_start, prev_best]]
    iter_log = []

    for i in range(dim):
        x = copy.copy(x_start)
        x[i] = x[i] + step
        score = f(x)
        res.append([x, score])

    # simplex iter
    iters = 0
    while 1:
        # order
        res.sort(key=lambda x: x[1])
        best = res[0][1]

        # record and print current result
        if iters > 0 and log_opt is True:
            iter_log.append(best)

        if print_opt is False:
            pass
        elif best != prev_best or iters in [1, max_iter]:
            print('Iteration', iters, '...best:', best)

        # break after max_iter
        if iters >= max_iter and log_opt is True:
            res[0].append(iter_log)
            return res[0]
        elif iters >= max_iter and log_opt is False:
            return res[0]

        iters += 1

        # break after no_improv_break iterations with no improvement
        if best <= prev_best - no_improve_thr:
            no_improv = 0
            prev_best = best
        else:
            no_improv += 1

        if no_improv >= no_improv_break and log_opt is True:
            res[0].append(iter_log)
            return res[0]
        elif no_improv >= no_improv_break and log_opt is False:
            return res[0]

        # centroid
        x0 = [0.] * dim
        for tup in res[:-1]:
            for i, c in enumerate(tup[0]):
                x0[i] += c / (len(res)-1)

        # reflection
        xr = x0 + alpha*(x0 - res[-1][0])
        rscore = f(xr)
        if res[0][1] <= rscore < res[-2][1]:
            res[-1] = [xr, rscore]
            continue

        # expansion
        if rscore < res[0][1]:
            xe = x0 + beta*(x0 - res[-1][0])
            escore = f(xe)
            if escore < rscore:
                res[-1] = [xe, escore]
                continue
            else:
                res[-1] = [xr, rscore]
                continue

        # contraction
        if rscore < res[-1][1]:
            xc = x0 + gamma*(xr - x0)  # outside
            cscore = f(xc)
            if cscore < res[-1][1]:
                res[-1] = [xc, cscore]
                continue
        else:
            xc = x0 - gamma*(xr - x0)  # inside
            cscore = f(xc)
            if cscore < res[-1][1]:
                res[-1] = [xc, cscore]
                continue

        # shrink
        x1 = res[0][0]
        nres = []
        for tup in res:
            redx = x1 + delta*(tup[0] - x1)
            score = f(redx)
            nres.append([redx, score])
        res = nres


if __name__ == "__main__":
    # test
    import math
    import numpy as np

    def f(x):
        return math.sin(x[0]) * math.cos(x[1]) * (1. / (abs(x[2]) + 1))

    print(simplex(f, np.array([0., 0., 0.])))
