import heapq
import os
from functools import total_ordering
import sys

class Node:
	def __init__(self, key, freq):
		self.key = key
		self.freq = freq
		self.left = None
		self.right = None
	def __lt__(self, other):
		return self.freq < other.freq
	def __eq__(self, other):
		if(other == None):
			return False
		return self.freq == other.freq



def build_heap(freq):
    heap = []
    for k in freq:
        heapq.heappush(heap,Node(k,freq[k]))

    while(len(heap)>1):
        l1 = heapq.heappop(heap)
        l2 = heapq.heappop(heap)
        new_node = Node(None,l1.freq+l2.freq)
        new_node.left = l1
        new_node.right = l2
        heapq.heappush(heap,new_node)
    return heap
    

def make_codes_helper(root, current, codes, reverse_map):
    if(root == None):
        return
    if(root.key != None):
        codes[root.key] = current
        reverse_map[current] = root.key
        return
    make_codes_helper(root.left, current + "0", codes, reverse_map)
    make_codes_helper(root.right, current + "1", codes, reverse_map)


def make_codes(heap):
    root = heapq.heappop(heap)
    current_code = ""
    codes = {}
    reverse_map = {}
    make_codes_helper(root, current_code, codes, reverse_map)
    return codes, reverse_map


def get_encoded_text(self, text):
    encoded_text = ""
    for character in text:
        encoded_text += self.codes[character]
    return encoded_text


def pad_to_fit(data):
    e = 8 - len(data) % 8
    for i in range(e):
        data += "0"

    meta = "{0:08b}".format(e)
    data = meta + data
    return data

def bytesof(dat):
    arr = bytearray()
    for i in range(0, len(dat), 8):
        byte = dat[i:i+8]
        arr.append(int(byte, 2))
    return arr


def buildFreq_table(data):
    result = {}
    for c in data:
        if c not in result.keys():
            result[c] = 0
        result[c]+=1
    return result

def encodeNsave(input_path):
    a = input_path.split('.')
    filename, extension = a[0],a[1]
    output_path = filename + ".bin"

    if extension == 'txt' or extension == 'dat':
        with open(input_path, 'r+') as file:
            data = file.read()
            data = data.rstrip()
    f = buildFreq_table(data)
    h = build_heap(f)
    codes, reverse_map = make_codes(h)
    encoded_text = ""
    for i in range(len(data)):
        encoded_text+=codes[data[i]]
    encoded_text_afterpad = pad_to_fit(encoded_text)
    output = open(output_path, 'wb')
    b = bytesof(encoded_text_afterpad)
    output.write(bytes(b))
    print("Compressed")
    return output_path, reverse_map, extension


def decodeNsave(input_path, reverse_map, extension):
    with open(input_path, 'rb') as file:
        bit_string = ""
        byte = file.read(1)
        while(len(byte) > 0):
            byte = ord(byte)
            bits = bin(byte)[2:].rjust(8, '0')
            bit_string += bits
            byte = file.read(1)
        
        pad,bit_string = int(bit_string[:8], 2), bit_string[8:]
        encoded_stream = bit_string[:-1*pad]

        if extension == 'txt' or extension == 'dat':
            #Decoding
            current = ""
            decoded_stream = ""
            for i in range(len(encoded_stream)):
                current+=encoded_stream[i]
                if current in reverse_map:
                    decoded_stream+=reverse_map[current]
                    current = ""
            filename = input_path.split('.')
            output_path = filename[0] + "_decompressed." + extension
            output = open(output_path, 'w')
            output.write(decoded_stream)
            output.close()
    print("Decompressed")
    return output_path

data_file_path = sys.argv[1]
# print(data_file_path.type)
output_path, rev_map, extension = encodeNsave(data_file_path)
print("File compressed @ " + output_path)
decom_path = decodeNsave(output_path, rev_map, extension)
print("File decompressed @ " + decom_path)