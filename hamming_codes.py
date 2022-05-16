
import numpy as np

from code_types import ErrorCorrectingCode

class HammingCode74(ErrorCorrectingCode):
    """Hamming Code[7,4] class. Encodes a 4 bit code using 3 parity bits.
    Decodes and corrects 7 bit codes.
    """

    def __init__(self):
        self.GT = np.array([
            [1,1,0,1],
            [1,0,1,1],
            [1,0,0,0],
            [0,1,1,1],
            [0,1,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ])
        self.H = np.array([
            [1,0,1,0,1,0,1],
            [0,1,1,0,0,1,1],
            [0,0,0,1,1,1,1]
        ])

        self.R = np.array([
            [0,0,1,0,0,0,0],
            [0,0,0,0,1,0,0],
            [0,0,0,0,0,1,0],
            [0,0,0,0,0,0,1]
        ])
    
    def encode(self, code: str):
        assert len(code) == 4

        for ch in code:
            assert ch == '0' or ch == '1'
            
        arr = np.array([int(ch) for ch in code])
        codearr = np.remainder(np.matmul(self.GT, arr), 2)

        encoding = ""
        for bit in codearr:
            if bit == 0:
                encoding = encoding + '0'
            else:
                encoding = encoding + '1'
        
        return encoding
    
    def decode(self, code: str):
        assert len(code) == 7

        for ch in code:
            assert ch == '0' or ch == '1'
        
        arr = np.array([int(ch) for ch in code])
        syndrome = np.remainder(np.matmul(self.H, arr), 2)
        correct = not np.any(syndrome)
        if correct:
            print('Code does not have any 1 bit errors.')
        else:
            pos = 0
            for bit in reversed(syndrome):
                pos = pos*2 + bit
            arr[pos - 1] = arr[pos - 1] ^ 1

            print(f'Found and fixed bit error at position {pos} in the 7 bit code.')
        ans = np.remainder(np.matmul(self.R, arr),2)
        
        decoding = ""
        for bit in ans:
            if bit == 0:
                decoding = decoding + '0'
            else:
                decoding = decoding + '1'
        
        return decoding