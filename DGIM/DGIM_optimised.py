from random import randint
import math

class DGIM:
    def __init__(self, window_size):
        self.window_size = window_size
        self.max_key = int(math.log2(self.window_size)) + 1
        self.current_timestamp = -1
        self.bucket = {}
        self.current_max_bucket_size = -1
        for i in range(self.max_key):
            self.bucket[i] = []

    def update(self, bit, timestamp):
        timestamp = timestamp % self.window_size
        self.current_timestamp = timestamp

        if self.current_max_bucket_size >= 0 and self.bucket[self.current_max_bucket_size][0] == timestamp:
            del self.bucket[self.current_max_bucket_size][0]
            if len(self.bucket[self.current_max_bucket_size]) == 0:
                self.current_max_bucket_size -= 1

        if bit == 1:
            self.bucket[0].append(timestamp)
            self.current_max_bucket_size = max(0, self.current_max_bucket_size)
            for i in range(self.max_key):
                if len(self.bucket[i]) > 2:
                    self.bucket[i + 1].append(self.bucket[i][1])
                    self.bucket[i] = self.bucket[i][-1:]
                    self.current_max_bucket_size = max(i + 1, self.current_max_bucket_size)
                else:
                    break

    def ones_num(self, bit_range):
        assert self.current_timestamp >= 0 and bit_range <= self.window_size and bit_range >= 1
        bit_sum = 0
        for i in range(self.max_key):
            for j in range(len(self.bucket[i]) - 1, -1, -1):
                time=self.bucket[i][j]
                if (self.current_timestamp-time+1)%self.window_size>bit_range:
                    print('Zostało wyestymowane {}  jedynek w przedziale ostatnich {} bitów'.format(bit_sum, bit_range))
                    return bit_sum
                else:
                    if (self.current_timestamp-time)%self.window_size+2**i<=bit_range:
                        bit_sum+=2**i
                    else:
                        bit_sum+=min(2 ** (i-1), bit_range - (self.current_timestamp - time) % self.window_size) # Slight modification
                        print('Zostało wyestymowane {}  jedynek w przedziale ostatnich {} bitów'.format(bit_sum, bit_range))
                        return bit_sum
        print('Zostało wyestymowane {}  jedynek w przedziale ostatnich {} bitów'.format(bit_sum, bit_range))
        return bit_sum

def dgim_error(stream, bit_range, estimated_bit_num):
    true_bit_num = sum(stream[-bit_range:-1])
    print(f'Algorytm w przedziale {bit_range} pomylił się o {estimated_bit_num-true_bit_num} bity o wartości jeden,'
          f'błąd wyniósł {(estimated_bit_num-true_bit_num)/bit_range*100}%')

if __name__ == '__main__':
    dgim = DGIM(window_size=100)
    bit_range = 40
    stream = []
    [stream.append(randint(0, 1)) for i in range(100)]

    for timestamp, bit in enumerate(stream):
        dgim.update(bit, timestamp)

    estimated_bit_num = dgim.ones_num(bit_range)
    dgim_error(stream, bit_range, estimated_bit_num)


