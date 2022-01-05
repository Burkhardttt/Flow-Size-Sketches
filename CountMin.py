import random
import sys
import os
from numpy import array
import numpy as np
# import pylab as pl


class CountMin:
    """CountMin"""
    def __init__(self, num_of_flows,
                 num_of_counter_arr, num_of_counters_each_arr):
        self.num_of_flows = num_of_flows
        self.num_of_counter_arr = num_of_counter_arr
        self.num_of_counters_each_arr = num_of_counters_each_arr

        self.counters = [[0 for i in range(self.num_of_counters_each_arr)]
                         for i in range(self.num_of_counter_arr)]
        self.s = [0 for i in range(self.num_of_counter_arr)]

        self.data = []
        self.hashcode = []

        self.actual = []
        self.estimated = []
        self.error = []
        self.average = 0

        self.final_result = []
        self.p = 0.5

    def read_file(self):
        file = open("project3input.txt", 'r')
        for line in file:
            line = line.split()
            self.data.append(line)
        self.data = self.data[1:]
        file.close()

        for i in range(self.num_of_flows):
            self.actual.append(int(self.data[i][1]))

    def generate_hashcode(self):
        """
        因为python中hash()方法加入了混淆参数，相同输入会得到不同结果，所以为了保证该方法只执行一次
        对单次执行的结果进行保留，避免在多次调用hash()方法
        :return:
        """
        for i in range(int(self.num_of_flows)):
            self.hashcode.append(abs(hash(self.data[i][0])))

    def generate_k_hash_functions(self):
        """
        s[] will do XOR with flow_id
        :return:
        """
        for i in range(len(self.s)):
            self.s[i] = random.randint(0, 10000000000)

    def record_all(self):
        """
        put flow_id into the counter
        :return:
        """
        for i in range(self.num_of_flows):
            for j in range(len(self.s)):
                hash_index = (self.hashcode[i] ^ self.s[j]) % self.num_of_counters_each_arr
                for k in range(self.actual[i]):# 1/2的概率取样
                    rand = random.randint(1, 10000)
                    if rand <= 5000:
                        self.counters[j][hash_index] += 1

    def query(self):
        min = sys.maxsize
        for i in range(self.num_of_flows):
            for j in range(len(self.s)):
                hash_index = (self.hashcode[i] ^ self.s[j]) % self.num_of_counters_each_arr
                if min > self.counters[j][hash_index]:
                    min = self.counters[j][hash_index]
            self.estimated.append(min * (1 / self.p))
            min = sys.maxsize

    def compute_error(self):
        sum = 0
        for i in range(self.num_of_flows):
            self.error.append(abs(self.estimated[i] - self.actual[i]))
        for i in range(self.num_of_flows):
            sum += self.error[i]
        self.average = float(sum / self.num_of_flows)

    def generate_final_result(self):
        for i in range(self.num_of_flows):
            self.final_result.append([self.data[i][0], self.estimated[i], int(self.data[i][1])])

    # def draw_hist(self,lenths):
    #
    #     data = lenths
    #
    #     bins = np.linspace(min(data),10000,25)
    #
    #     pl.hist(data,bins)
    #
    #     pl.xlabel('Size of packet')
    #
    #     pl.ylabel('Number of occurences')
    #
    #     pl.title('Frequency distribution of size of packets')
    #
    #     pl.show()


if __name__ == "__main__":

    # hashcode = []
    # for i in range(int(num_of_flows)):
    #     hashcode.append(abs(hash(data[i][0])))

    Cm = CountMin(10000, 5, 3000)
    Cm.read_file()
    Cm.generate_hashcode()
    Cm.generate_k_hash_functions()
    Cm.record_all()
    Cm.query()
    Cm.compute_error()
    Cm.generate_final_result()
    Cm.final_result = sorted(Cm.final_result, key=lambda list:list[1], reverse=True)
    # Cm.draw_hist(Cm.actual)

    doc = open("output1.txt", 'w')
    print("The average error among all flows: " + str(Cm.average))
    print("The average error among all flows: " + str(Cm.average), file=doc)

    # ip address - estimated flow size - actual flow size
    for i in range(100):
        print(Cm.final_result[i])
        print(Cm.final_result[i],file=doc)













