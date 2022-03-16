#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create an ensemble of function for huffman code.
@author: TOUMI Anouar
"""

# Import
from node import NodeTree


def huffman_code_tree(node, left=True, binstring=''):
    """
    Function using Node class to create binary values linked for each character in a string
    @param node: int
    @param left: Boolean
    @param binstring: str
    @return: Dictionary
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
    Create a dictionary of frequency for each character from a string and return a List made from the dictionary
    @param sequence: str
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
     Create a dictionary of frequency for each character from a list of frequence create before
     and return this dictionary
    @param list_freq: List
    @return: dictionary
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


def from_seq_to_binary(sequence_str, huffman_code_dico):
    """
    Function translate a string into binary thanks to the huffman code dictionary created before
    @param sequence_str: str
    @param huffman_code_dico: dictionary
    @return: List
    """
    # initialize binary_seq variable
    binary_seq = ""
    sequence_str = sequence_str.replace("\n", "")
    for nucleotide in sequence_str:
        # append into binary_seq binary value for each character from the dictionary
        if huffman_code_dico[nucleotide]:
            binary_seq += huffman_code_dico[nucleotide]
        else:
            print("error : character in proposed sequence not in huffman code")
    return [binary_seq, huffman_code_dico]


def from_binary_to_seq(binary_seq, huffman_code_dico):
    """
    Function translate a binary into string thanks to the huffman code dictionary created before
    @param binary_seq: str
    @param huffman_code_dico: Dictionary
    @return: List
    """
    # Initialize variables
    sequence_str = ''
    binary_number = ''

    for binary in binary_seq:
        # append into binary_seq character associated to binary value from the huffman dictionary
        binary_number = binary_number + binary
        if binary_number in huffman_code_dico.values():
            sequence_str += list(huffman_code_dico.keys())[list(huffman_code_dico.values()).index(binary_number)]
            binary_number = ""
    return [sequence_str, huffman_code_dico]


def from_binary_to_ascii(sequence_binary):
    """
    Function translate a binary into ASCII thanks to the huffman code dictionary created before.
    We are only using visible ASCII character bewteen 33 to 126.
    In this function we are starting from the end of binary sequence to transform it into ASCII.
    @param sequence_binary: List
    @return: List
    """
    # Defining variables from sequence_binary and initilize some other variables.
    dico = sequence_binary[1]
    sequence_binary = sequence_binary[0]
    temp = str(sequence_binary)
    intial_len = len(sequence_binary)
    final_len = 0
    asci = ""
    while len(temp) > 1:
        # Transform binary sequence into ASCII character between 0 and 93
        temp = temp[1:]
        if temp.startswith("0") is False:
            if len(temp) < 12:
                if int(temp, 2) < 93:
                    # Save the ASCII character corresponding to the value + 33 (in the visible ASCII character interval)
                    final_len += len(temp)
                    asci = str(chr(int(temp, 2) + 33)) + asci
                    sequence_binary = sequence_binary[:-len(temp)]
                    temp = str(sequence_binary)
        # Special case when the last character is 0
        if len(temp) == 1 and temp.startswith("0"):
            final_len += len(temp)
            asci = "~" + asci
            sequence_binary = sequence_binary[:-len(temp)]
            temp = str(sequence_binary)
        # Special case when the last character is 1
        if len(temp) == 1 and temp.startswith("1"):
            final_len += len(temp)
            asci = str(chr(int(temp, 2) + 33)) + asci
            sequence_binary = sequence_binary[:-len(temp)]
            temp = str(sequence_binary)
    # if the two lengths are different we add "~" for the missing numbers
    intial_len -= final_len
    if intial_len > 0:
        asci = ("~" * intial_len) + asci
    return [asci, dico]


def from_ascii_to_binary(encoded_sequence):
    """
    Translate ASCII character into binary
    @param encoded_sequence: List
    @return: List
    """
    # Defining variables from sequence_binary and initilize some other variables.
    dico = encoded_sequence[0]
    encoded_sequence = encoded_sequence[1]
    decoded_sequence = ""

    for char in encoded_sequence:
        # Translating "~" into 0
        if char == "~":
            decoded_sequence += "0"
        else:
            # decoding ASCII character into Binary
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

