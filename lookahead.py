#!/bin/python
# ---------------------------------------------------------------------------------------
# carry lookahead addition algorithm

import carry_look

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
if __name__=="__main__":
    print("Carry Lookahead Addition Algorithm\n")

    #
    # 	phase 1
    #
    a = [0, 0, 0, 1, 1, 0, 1, 0]		# the 1st number
    b = [1, 1, 0, 0, 1, 1, 0, 1]		# the 2nd number to add

    value = subaddition(a, b)			# generate values

    print('number 1: ', a)
    print('number 2: ', b)
    print('values  : ', value)
    #
    # 	phase 2
    #

    mytree = carry_look.lookahead_Tree()
    r = mytree.build_tree(value)
    (v, time) = mytree.run(r)

    #
    # 	phase 3
    #
    #v = ['s','s','s','g','s','g','s','s','s']	# assume a random list of 's' and 'g'
    s = producesum(a, b, v)						# find the sum of these numbers

    #
    #	serial algorithm of O(N) steps
    #
    print('\nSerial Algorithm')

    print('Number 1:    ', a)
    print('NUmber 2:    ', b)
    print('Result  : ', serial(a, b))

    print('\nParallel Algorithm')
    print('Number 1:    ', a)
    print('NUmber 2:    ', b)
    print('Result  : ', s)
# ---------------------------------------------------------------------------------------

