import random
import sys


class CounterSketch:
    """CounterSketch"""
    def __init__(self, num_of_flows, num_of_counter_arr,
                 num_of_counters_each_arr):
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

    def read_file(self):
        """
        read file
        :return:
        """
        file = open("../project3input.txt", 'r')
        for line in file:
            line = line.split()
            self.data.append(line)
        self.data = self.data[1:]
        file.close()

        for i in range(self.num_of_flows):
            self.actual.append(int(self.data[i][1]))

    def generate_hashcode(self):
        """
        encode IP address
        :return:
        """
        for i in range(self.num_of_flows):
            self.hashcode.append(hash(self.data[i][0]))

    def generate_k_hash_functions(self):
        """
        s[] will do XOR with encoded flow_id()
        :return:
        """
        for i in range(len(self.s)):
            self.s[i] = random.randint(0,10000000000)

    def record_all(self):
        """
        record encoded flow_id into counters
        :return:
        """
        for i in range(self.num_of_flows):
            for j in range(len(self.s)):
                hash_result = self.hashcode[i] ^ self.s[j]
                hash_index = hash_result % self.num_of_counters_each_arr
                str = bin(hash_result)
                if str[0] == '0':
                    self.counters[j][abs(hash_index)] += self.actual[i]
                else:
                    self.counters[j][abs(hash_index)] -= self.actual[i]

    def query(self):
        """
        query for flow size of one flow_id
        :return:
        """
        for i in range(self.num_of_flows):
            est_temp = []
            for j in range(len(self.s)):
                hash_result = self.hashcode[i] ^ self.s[j]
                hash_index = hash_result % self.num_of_counters_each_arr
                str = bin(hash_result)
                if str[0] == '0':
                    est_temp.append(self.counters[j][abs(hash_index)])
                else:
                    est_temp.append(-self.counters[j][abs(hash_index)])

            est_temp = sorted(est_temp)
            if len(est_temp) % 2 == 0:
                mean = int((est_temp[int(len(est_temp)/2)]
                            + est_temp[int(len(est_temp)/2 - 1)]) / 2)
                self.estimated.append(mean)
            else:
                med = est_temp[int(len(est_temp)/2)]
                self.estimated.append(med)
            # print(est_temp)

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


if __name__ == "__main__":
    # print(bin(hash('23.96.219.115')))
    # print(   bin(hash('23.96.219.115'))[-1]   )
    # print(type(bin(hash('23.96.219.115'))[-1]))

    Cs = CounterSketch(10000, 3, 3000)
    Cs.read_file()
    Cs.generate_hashcode()
    Cs.generate_k_hash_functions()
    Cs.record_all()
    Cs.query()
    Cs.compute_error()
    Cs.generate_final_result()
    Cs.final_result = sorted(Cs.final_result, key=lambda list: list[1], reverse=True)

    doc = open("output2.txt", 'w')
    print("The average error among all flows: " + str(Cs.average))
    print("The average error among all flows: " + str(Cs.average), file=doc)

    # ip address - estimated flow size - actual flow size
    for i in range(100):
        print(Cs.final_result[i])
        print(Cs.final_result[i], file=doc)