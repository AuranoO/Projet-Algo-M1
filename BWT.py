#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Burrows-Wheeler algorithm to encode sequence by bwt method.
@author: TOUMI Anouar
"""

# import library numpy for matrix
import numpy as np


def add_dollars(sequence):
    """
    Add a "$" at the end of the sequence.
    @param sequence: str
    @return: str
    """
    # append "$" at end of the sequence
    sequence_dollar = sequence + "$"
    return sequence_dollar


def realignement_sequence(sequence):
    """
    Create all the possibility of dollar position in the sequence
    @param sequence: str
    @return: List
    """
    # initialise empty list for result
    list_sequence = []
    # initialise counter to get the sequence without the last element of the sequence
    seq_index_end = 1
    list_sequence.append(sequence)
    # for each element in the given sequence
    for nucleotide in sequence:
        if seq_index_end < len(sequence):
            # get the beginning and end to create a new sequence
            sequence_end = sequence[-seq_index_end:]
            sequence_except_end = sequence[0:len(sequence) - seq_index_end]
            # create a new sequence
            new_sequence = sequence_end + sequence_except_end
            # append the new sequence to the list
            list_sequence.append(new_sequence)
            # increase the index of the sequence_end
            seq_index_end += 1

    sorted_list = sorted(list_sequence)
    return sorted_list


def get_bwt(list_sequence):
    """
    From the list of list sorted, take the last element to build the bwt sequence.
    @param list_sequence: List
    @return: str
    """
    # initialise bwt variable
    bwt = ""
    # append the last character of each sequence to the bwt sequence
    for sequence in list_sequence:
        sequence_end = sequence[-1:]
        bwt += sequence_end
    bwt = bwt.replace(" ", "")
    return bwt


def get_matrix(sequence, verbose=False):
    """
    Take bwt sequence and build the detransformation matrix use to found the initiale sequence and return the matrix
    or a list of matrix ir verbose is True.
    @param sequence: str
    @param verbose: Boolean
    @return: np.matrix or List
    """
    # initialise an emptry matrix to store the sequence
    matrix = np.array([])
    # for each element (nucleotid) in the input sequence
    for nucleotide in sequence:
        # append the element as a list
        matrix = np.append(matrix, [nucleotide])
    # save this as the initiale matrix
    initiale_matrix = matrix
    # initialise a Boolean to check if the matrix contain only one column
    colunm_value = False
    # for each element in the sequence
    count_step = 1
    step_by_step_matrix = []
    for i in range(1, len(sequence), 1):
        # if matrix contain only one column
        if colunm_value is False:
            # sort the matrix as one dimension matrix
            matrix = sorted(matrix)
            step_by_step_matrix.append("Etape " + str(count_step))
            count_step += 1
            step_by_step_matrix.append(matrix)
        # if matrix contain more than one column
        else:
            # sort the matrix as multidimensional matrix
            matrix = (matrix[np.lexsort(np.fliplr(matrix).T)])
        # append the initiale matrix to the sorted matrix
        matrix = np.column_stack((initiale_matrix, matrix))
        step_by_step_matrix.append("Etape"+str(count_step))
        count_step += 1
        # Transform matrix into a list
        step_by_step_matrix.append(matrix.tolist())
        # the matrix is now a mutli-dimensional matrix
        colunm_value = True
    # return the matrix
    if verbose is False:
        return matrix
    list_matrix_step = []
    for i in range(0, len(step_by_step_matrix)):
        if i % 2 != 0:
            for element in step_by_step_matrix[i]:
                list_matrix_step.append(element)
        else:
            list_matrix_step.append(step_by_step_matrix[i])
    return list_matrix_step


def get_sequence_rebuild(matrix):
    """
    from the rebuild matrix return the initial sequence transformed by BWT
    @param matrix:
    @return: str
    """
    # for each line in the matrix
    seq_rebuild = ""
    for line in range(len(matrix)):
        # if the last element of the line is a "$"
        if matrix[line, -1] == "$":
            # get the line as the sequence rebuilded
            seq_rebuild = "".join(matrix[line])
            # remove the dollar at the end
            seq_rebuild = seq_rebuild[0:-1]
    return seq_rebuild


def bwt_transformation(sequence):
    """
    function to get the bwt sequence from a nucleic sequence.
    @param sequence: str
    @return: str
    """
    # from the sequence to the bwt
    bwt = get_bwt(realignement_sequence(add_dollars(sequence)))
    return bwt

