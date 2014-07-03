#!/bin/python
# ---------------------------------------------------------------------------------------
# carry lookahead addition algorithm

import carry_look
import random
import argparse
from math import *

# ---------------------------------------------------------------------------------------
def expand( n ):
# Expand a number to the closer 2^k number
    return ([0] * (int(pow(2, ceil(log(len(n), 2))))-len(n)))+n

# ---------------------------------------------------------------------------------------
def subaddition(a, b):
#	The 1st phase of the carry look ahead algorithm.
#	(we assume that a and b have the same length).

    value = ['\0'] * len(a)			# create an empty list of size a

    # if the two bits are different assign 'p'. If not then just look
    # the bit of the 1st number. If it's 0 then both bits are 0, so assign 's'.
    # Otherwise, both bits are 1, so assign 'g'
    for i in range(len(a)) :
        value[i] = 'p' if a[i] != b[i] else 's' if a[i] == 0 else 'g'

    return value					# return the values

# ---------------------------------------------------------------------------------------
def producesum(a, b, value):
#	The 3rd phase of the carry look ahead algorithm.
#	(we assume that a and b have the same length).
    _sum = [0] * (len(a) + 1)		# create an empty list of size a

    _sum[0] = 0 if value[0] == 's' else 1

    for i in range(len(a)) :
        _sum[i+1] = (0 if value[i+1] == 's' else 1) ^ a[i] ^ b[i]

    return _sum						# return the values

# ---------------------------------------------------------------------------------------
def serial(a, b):
#	The serial addition algorithm.
    carry = 0;						# initially there's no carry
    _sum = [0] * (len(a) + 1)		# create an empty list of size a

    for i in range(len(a)-1, -1, -1) :
        _sum[i+1] = a[i] ^ b[i] ^ carry							# calc S
        carry = (a[i] and b[i]) or (carry and (a[i] ^ b[i]))	# calc C


    _sum[0] = carry					# result has N+1 bits, with carry be the MSbit

    return _sum						# return the sum

# ---------------------------------------------------------------------------------------
def test_sums(a, b):
    '''
        Returns the time (in steps) it took for the parallel lookahead tree
        to compute the sum
    '''
    val = subaddition(a, b)
    mytree = carry_look.lookahead_Tree()
    r = mytree.build_tree(val)
    (v, time) = mytree.run(r)
    s = producesum(a, b, v)						# find the sum of these numbers
    serial_result = serial(a, b)

    if not serial_result == s:
        raise Exception('Results are not the same')

    return time

def build_rand(n, iter):
    '''
        Returns a random list
        containing values from iter
    '''
    r = []
    for i in range(n):
        r.append(random.choice(iter))
    return r

def bench(ranges):

    pop = [0, 1]
    times = []
    for i in ranges:
        size = 2 ** i
        a = build_rand(size,pop)
        b = build_rand(size,pop)
        times.append(test_sums(a, b))
    return times

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--sum",metavar='N', type=str,nargs='+',
                    help="first binary number")

    group.add_argument('--bench', help='Show a bench (requires matplotlib)',
                        action="store_true")
    args = parser.parse_args()
    if args.bench:
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Matplotlib could not be imported, exiting!")
            exit()

        ranges = range(3,10);
        xx = [2 ** i for i in ranges]
        total_times = bench(ranges)
        print(total_times)
        plt.plot(xx,total_times)
        def_time = [n+1 for n in xx]
        plt.plot(xx, def_time)
        plt.legend(['Steps required','Steps for serial'])
        plt.ylim(0,100)
        plt.show()
    else:
        a = [int(c) for c in args.sum[0]]
        b = [int(c) for c in args.sum[1]]
        print('%d steps required for the computation' % test_sums(expand(a), expand(b)))
        print('Result = %s' % str(serial(a, b)))
