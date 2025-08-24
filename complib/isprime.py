import math

class Tester():
    def __init__(self):
        self.num = 2
    def __iter__(self):
        while True:
            self.num += 1
            yield int(self.num)

tester = Tester()

def is_prime(n):

    if n <= 1:
        return False  # Numbers less than or equal to 1 are not prime
    sss = int(math.sqrt(n) + 1)
    for i in range(2, sss):
        if n % i == 0:
            return False  # Found a divisor, so it's not prime
    return True  # No divisors found, so it's prime

def is_prime2(n):
    if n <= 1:
        return False  # Numbers less than or equal to 1 are not prime
    sss = int(math.sqrt(n) + 1)
    nn = 2
    while True:
        if nn >= sss:
            break
            #return False
        if n % nn == 0:
            return False  # Found a divisor, so it's not prime
        nn += 1
    return True  # No divisors found, so it's prime

def is_prime3(n):

    #print("\ntest:", n)
    if n <= 1:
        return False  # Numbers less than or equal to 1 are not prime
    sss = int(math.sqrt(n) + 1)
    tester2 = Tester()
    for nn in iter(tester2):
        #print("iter:", nn, end = " ")
        if nn >= n:
            #break
            return False
        if n % nn == 0:
            return False  # Found a divisor, so it's not prime
    return True  # No divisors found, so it's prime

if __name__ == "__main__":

    for number in iter(tester):
        if number > 10:
            break
        if is_prime3(number):
            print(number, end = " ")
            pass

# EOF
