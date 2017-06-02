"""
Absolute values on Holographic Slotcoding
"""
import math
import numpy as np
class AbsolutHolographicSlotcoding:
    
    target = ""
    prime = ""
    num_pos = 0
    num_let = 0
    num_cases = 0
    set_of_letters = []
    adjusted = True
    vectors = []
    similarity = 0
    
    def __init__(self, trgt, prm):
        self.target = trgt
        self.prime = prm
        self.num_pos = max(len(trgt), len(prm))
        self.num_let = len(set(self.target+self.prime))
        self.num_cases = self.num_let+self.num_pos
        self.vectors = self.make_vectors()
        self.set_of_letters = list(set(trgt+prm))
        self.similarity = self.compare(self.make_vector(prm), self.make_vector(trgt))
        

    def make_vector(self, p):
        total_vector = []
        for i in range(len(self.target)):
            f_layer_vector = []
            for j in range(len(self.target)):
                lp = self.find_letter_position(self.target[i])
                vlet = self.vectors[lp]
                rel_pos_t_w = self.gaussian(i-j)
                rel_pos_c_w = self.gaussian(self.rel(self.target[i], j, p))
                f_layer_vector.append(self.bind(lp, j, rel_pos_t_w*rel_pos_c_w))
            f_layer_vector = self.chunk(f_layer_vector)
            total_vector.append(f_layer_vector)
        return self.chunk(total_vector)

    def rel(self, letter, position, word):
        closest = 99
        for i, l in enumerate(word):
            if l==letter:
                if abs(i-position)< closest:
                    closest = abs(i-position)
        return closest
    
    def find_letter_position(self, let):
        return self.set_of_letters.index(let) + self.num_pos

    def bind(self, l, pos, w):
        bound = []
        v1 = self.vectors[l]
        v2 = self.vectors[pos]
        for i,j in zip(v1, v2):
            bound.append(w*(1.0-abs(i-j)))
        return bound

    def chunk(self, vectors):
        chunked = []
        for i in range(len(vectors[0])):
            summed = 0
            for j in vectors:
                summed = summed + j[i] - 0.5
            if summed > 0:
                chunked.append(1)
            if summed < 0:
                chunked.append(0)
            if summed == 0:
                chunked.append(0.5)
        return chunked

    def compare(self, v1, v2):
        total = 0
        for i,j in zip(v1, v2):
            if i==j:
                if i==0.5:
                    total = total - 0.5 # adjust for ties
                total = total + 1.0
            else:
                if abs(i-j)==0.5:
                    total = total + 0.5
        return total / self.num_cases

    def make_vectors(self):
        size = 1000
        vectors = []
        for i in range(self.num_cases):
            halfsize = size / 2
            halfsizeodd = size / 2 + size % 2
            vector = np.array([0] * halfsize + [1] * halfsizeodd)
            np.random.shuffle(vector)
            vectors.append(vector)
        return vectors

    def gaussian(self, pos):
        sigma = 10.0
        power = -1.0* ((pos/sigma)**2)
        return math.exp(power)

c = ["12345", "1245", "123345", "123d45", "12dd5", "1d345",
     "12d456", "12d4d6", "d2345", "12d45", "1234d", "12435",
     "21436587", "125436", "13d45", "12345", "34567", "13457",
     "123267", "123567", "12dd45", "12de45", "12345345", "1346", "1436"]

t = ["12345", "12345", "12345", "12345", "12345", "12345",
     "123456", "123456", "12345", "12345", "12345", "12345",
     "12345678", "123456", "12345", "1234567", "1234567", "1234567",
     "1232567", "1232567", "123345", "123345", "12345", "123456", "123456"]

for i in range(len(t)):
    sum = 0
    for s in range(100):
        ahs = AbsolutHolographicSlotcoding(t[i], c[i])
        sum = sum + ahs.similarity
    print t[i], c[i], sum/100.0
