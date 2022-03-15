#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create an ensemble of function for huffman code
@author: TOUMI Anouar
"""

# Import
from node import NodeTree


def huffman_code_tree(node, left=True, binstring=''):
    """

    @param node:
    @param left: Boolean
    @param binstring: str
    @return: dictionary
    """
    if type(node) is str:
        return {node: binstring}
    (left, right) = node.children()
    huffman_dict = dict()
    huffman_dict.update(huffman_code_tree(left, True, binstring + '0'))
    huffman_dict.update(huffman_code_tree(right, False, binstring + '1'))
    return huffman_dict


def create_dico_frequence(sequence):
    """

    @param sequence:
    @return: List
    """
    dico_freq = {}
    sequence = sequence.replace("\n", "")
    for character in sequence:
        if character in dico_freq:
            dico_freq[character] += 1
        else:
            dico_freq[character] = 1
    list_freq = sorted(dico_freq.items(), key=lambda x: x[1], reverse=True)
    return list_freq


def create_huffman_code(list_freq):
    """

    @param list_freq:
    @return:
    """
    while len(list_freq) > 1:
        (key1, value1) = list_freq[-1]
        (key2, value2) = list_freq[-2]
        list_freq = list_freq[:-2]
        node = NodeTree(key1, key2)
        list_freq.append((node, value1 + value2))
        list_freq = sorted(list_freq, key=lambda x: x[1], reverse=True)
    huffman_code = huffman_code_tree(list_freq[0][0])
    return huffman_code


def print_code_huffman(huffman_code_dico):
    """

    @param huffman_code_dico:
    @return:
    """
    print(' Char|Huffman code ')
    print(' -----------------')
    for nucleotid, binary in huffman_code_dico.items():
        print(' %3s |%5s' % (nucleotid, huffman_code_dico[nucleotid]))


def from_seq_to_binary(sequence_str, huffman_code_dico):
    """

    @param sequence_str:
    @param huffman_code_dico:
    @return:
    """
    binary_seq = ""
    sequence_str = sequence_str.replace("\n", "")
    for nucleotid in sequence_str:
        if huffman_code_dico[nucleotid]:
            binary_seq += huffman_code_dico[nucleotid]
        else:
            print("error : character in proposed sequence not in huffman code")
    return [binary_seq, huffman_code_dico]


def from_binary_to_seq(binary_seq, huffman_code_dico):
    """

    @param binary_seq:
    @param huffman_code_dico:
    @return:
    """
    sequence_str = ''
    binary_number = ''
    for binary in binary_seq:
        binary_number = binary_number + binary
        if binary_number in huffman_code_dico.values():
            sequence_str += list(huffman_code_dico.keys())[list(huffman_code_dico.values()).index(binary_number)]
            binary_number = ""
    return [sequence_str, huffman_code_dico]


def from_binary_to_ascii(sequence_binary):
    """

    @param sequence_binary: List
    @return: List
    """
    dico = sequence_binary[1]
    sequence_binary = sequence_binary[0]
    temp = str(sequence_binary)
    intial_len = len(sequence_binary)
    final_len = 0
    asci = ""
    while len(temp) > 1:
        temp = temp[1:]
        if temp.startswith("0") is False:
            if len(temp) < 12:
                if int(temp, 2) < 93:
                    final_len += len(temp)
                    asci = str(chr(int(temp, 2) + 33)) + asci
                    sequence_binary = sequence_binary[:-len(temp)]
                    temp = str(sequence_binary)
        if len(temp) == 1 and temp.startswith("0"):
            final_len += len(temp)
            asci = "~" + asci
            sequence_binary = sequence_binary[:-len(temp)]
            temp = str(sequence_binary)

        if len(temp) == 1 and temp.startswith("1"):
            final_len += len(temp)
            asci = str(chr(int(temp, 2) + 33)) + asci
            sequence_binary = sequence_binary[:-len(temp)]
            temp = str(sequence_binary)

    intial_len -= final_len
    if intial_len > 0:
        asci = ("~" * intial_len) + asci
    return [asci, dico]


def from_ascii_to_binary(encoded_sequence):
    """
    Translate ASCII code into binary
    @param encoded_sequence: List
    @return: List
    """
    dico = encoded_sequence[0]
    encoded_sequence = encoded_sequence[1]
    decoded_sequence = ""
    for char in encoded_sequence:
        if char == "~":
            decoded_sequence += "0"
        else:
            decoded_sequence += str(bin(ord(char) - 33))[2:]
    return [decoded_sequence, dico]


def encode(data):
    """
    Use multiples functions created before to produced ascii code from a sequence
    @param data: List
    @return: List
    """
    return from_binary_to_ascii(from_seq_to_binary(data, create_huffman_code(create_dico_frequence(data))))


def decode(data):
    """
    Use multiples functions created before to produced the initial sequence from ascci code
    @param data:
    @return: List
    """
    return from_binary_to_seq(*from_ascii_to_binary([data[0], data[1]]))
