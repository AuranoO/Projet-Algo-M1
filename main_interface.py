#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main algorithm: to create Tkinter interface and connect the differents algorithm
@author: TOUMI Anouar
"""

# ============Import libraries and functions============
# to read line from file as object (for a dictionary)
import ast
# import os command (to create directory)
import os
# to create the window and the widgets from tkinter (GUI)
from tkinter import Tk, Button, filedialog
# for the treatments that will be carried out on the selected sequence and file.txt
from function_tool import transform_to_list, save_to_file, read_file
# for the BWT encoding
from BWT import add_dollars, realignement_sequence, get_bwt, get_matrix, get_sequence_rebuild
# for the huffman encoding
from huffman_code import create_huffman_code, create_dico_frequence, from_seq_to_binary, \
    from_binary_to_seq, from_binary_to_ascii, from_ascii_to_binary


def launch_bwt():
    """
    Function to launch BWT transformation for the button "from sequence to BWT"
        Parameters :
        ----------
        None

        Return :
        ----------
        None
    """
    # get the sequence from a file.txt
    sequence_example = read_file()
    # open a save file to save the new data
    save_file = open(FOLDER_SELECTED + "/output_XeraBioTool/BWT.txt", "w")
    # get BWT and write it in save file.
    bwt = get_bwt(realignement_sequence(add_dollars(sequence_example)))
    save_file.write("BWT :")
    save_to_file(save_file, bwt.replace("\n", ""))
    # close the save data
    save_file.close()


def launch_huffman():
    """
    Function to launch Huffman encoding for the button "from sequence to huffman"
        Parameters :
        ----------
        None

        Return :
        ----------
        None
    """
    # get the sequence from a file.txt
    sequence_example = read_file()
    # open a save file to save the new data
    save_file = open(FOLDER_SELECTED + "/output_XeraBioTool/huffman.txt", "w")
    # create a huffman code and save it to the save file
    huffman_code = create_huffman_code(create_dico_frequence(sequence_example))
    save_file.write("huffmanCode :")
    save_to_file(save_file, huffman_code)
    # compress nucleotid sequence into characters and save it to save file
    encoded_sequence = from_binary_to_ascii(from_seq_to_binary(sequence_example, huffman_code))
    save_file.write("sequence encoded :")
    save_to_file(save_file, encoded_sequence)


def launch_rebuild_huffman():
    """
    Function to launch Huffman rebuilding for the button "from huffman to sequence"
        Parameters :
        ----------
        None

        Return :
        ----------
        None
    """
    # ask the user to select file (to get huffman code & an encoded sequence)
    file_path = filedialog.askopenfilename()
    file = open(file_path, "r")
    # initialise dictionary and list to append huffman code and sequence from file
    huffman_code_dico = dict()
    sequence_encoded = list()
    # =============append huffman code and sequence from file===================
    # initialise an index to select line containing encoded_sequence
    compt_seq_encoded = 0  # (off)
    for line in file:
        # get the huffmancode dictionary from the file
        if "huffmanCode" in line:
            temp = line.split(":", 1)
            huffman_str = temp[1]
            huffman_code_dico = ast.literal_eval(huffman_str)
        # if encoded sequence is on several line, add all the line
        if compt_seq_encoded > 0:
            line = transform_to_list(line)
            sequence_encoded[0] += line
        # get sequence encoded from the file
        if "sequence encoded" in line:
            compt_seq_encoded += 1  # (on)
            temp = line.split(":", 1)
            sequence = temp[1]
            sequence_encoded = transform_to_list(sequence)

    # close the selected file
    file.close()
    # open a new save file to write the decoded sequence
    save_file = open(FOLDER_SELECTED + "/output_XeraBioTool/seq_rebuilded_by_Huffman.txt", "w")
    save_file.write("sequence_decoded :")
    sequence_encoded = sequence_encoded[0].replace("\n", "")
    sequence_in_binary = from_ascii_to_binary(sequence_encoded)
    save_to_file(save_file, from_binary_to_seq(sequence_in_binary, huffman_code_dico))
    # close the save file
    save_file.close()


def launch_rebuild_bwt():
    """
    Function to launch BWT rebuild for the button "from BWT to sequence"
        Parameters :
        ----------
        None

        Return :
        ----------
        None
    """
    # get the sequence from a file.txt
    sequence_example = read_file()
    # split the selected BWT sequence to remove "BWT:"
    sequence_example = sequence_example.split(":")
    # open a save file to save the new data
    save_file = open(FOLDER_SELECTED + "/output_XeraBioTool/seq_rebuilded_by_BWT.txt", "w")

    # write in save file the BWT and the rebuilded sequence
    sequence_rebuilded = get_sequence_rebuild(get_matrix(sequence_example[1].replace("\n", "")))
    save_file.write("rebuilded sequence :")
    save_to_file(save_file, sequence_rebuilded)
    # close the save file
    save_file.close()


def launch_from_seq_bwt_huffman():
    """
    Function to launch the modification sequence into BWT then Huffman compression
        Parameters :
        ----------
        None

        Return :
        ----------
        None
    """
    # get the sequence from a file.txt
    sequence_example = read_file()
    # open a save file to save the new data
    save_file = open(FOLDER_SELECTED + "/output_XeraBioTool/BWT_Huffman.txt", "w")

    # write in save file the BWT and the rebuilded sequence
    bwt = get_bwt(realignement_sequence(add_dollars(sequence_example)))
    # create a huffman code from BWT sequence and save it to the save file
    huffman_code = create_huffman_code(create_dico_frequence(bwt))
    save_file.write("huffmanCode :")
    save_to_file(save_file, huffman_code)

    # transform BWT sequence into characters and save it to save file
    encoded_sequence = from_binary_to_ascii(from_seq_to_binary(bwt, huffman_code))
    save_file.write("sequence encoded :")
    save_to_file(save_file, encoded_sequence)
    # close the save file
    save_file.close()


def launch_from_bwt_huff_to_seq():
    """
    Function to launch the decompression of the sequence encoded in
    Huffman then rebuild the sequence
    by BWT method.
        Parameters :
        ----------
        None

        Return :
        ----------
        None
    """
    # ask the user to select file (to get huffman code & an encoded sequence)
    file_path = filedialog.askopenfilename()
    file = open(file_path, "r")

    # initialise dictionary and list to append huffman code and sequence from file
    huffman_code_dico = dict()
    sequence_encoded = list()

    # append huffman code and sequence from file
    compt_seq_encoded = 0  # (off)
    for line in file:
        # get the huffmancode from the file
        if "huffmanCode" in line:
            temp = line.split(":", 1)
            huffman_str = temp[1]
            huffman_code_dico = ast.literal_eval(huffman_str)

        # if encoded sequence is on several line, add all the line
        if compt_seq_encoded > 0:
            line = transform_to_list(line)
            sequence_encoded[0] += line

        # get sequence encoded from the file
        if "sequence encoded" in line:
            compt_seq_encoded += 1  # (on)
            temp = line.split(":", 1)
            sequence = temp[1]
            sequence_encoded = transform_to_list(sequence)
    # close the save file
    file.close()
    # get back the BWT from encoded sequence
    bwt = from_binary_to_seq(from_ascii_to_binary(sequence_encoded[0]), huffman_code_dico)
    # get back the initale sequence (sequence_decoded)
    sequence_decoded = get_sequence_rebuild(get_matrix(bwt))
    # open a new save file to write the decoded sequence
    save_file = open(FOLDER_SELECTED + "/output_XeraBioTool/seq_rebuilded_by_BWT_Huffman.txt", "w")
    save_file.write("sequence_decoded :")
    save_to_file(save_file, sequence_decoded)


if __name__ == "__main__":
    # execute only if run as a script

    # ask path way to work
    TEMP_ROOT = Tk()
    TEMP_ROOT.withdraw()
    FOLDER_SELECTED = filedialog.askdirectory()
    # create the folder to add result
    # try:
    #     os.mkdir(FOLDER_SELECTED + "/output_XeraBioTool")
    # except:
    #     pass

    # Interface Tkinter (GUI)
    WINDOW = Tk()
    WINDOW.title("XeraBioTool : BWT & Huffman ")
    WINDOW.geometry("500x150")

    # =====button Launch and Quit for BWT and huffman encoding and decoding=======
    # initialise button list and function list to create widgets in tkinter
    BUTTON_LIST = ['from sequence to BWT',
                   'from sequence to Huffman',
                   'from BWT to sequence',
                   'from Huffman to sequence',
                   "compress sequence to BWT/Huffman",
                   "decompress BWT/Huffman",
                   'CLOSE']
    FUNCTION_LIST = [launch_bwt, launch_huffman,
                     launch_rebuild_bwt,
                     launch_rebuild_huffman,
                     launch_from_seq_bwt_huffman,
                     launch_from_bwt_huff_to_seq,
                     WINDOW.destroy]
    # initialise row, column and function index for the localisation and functions of each buttons
    ROW_INDEX = 1
    COLUMN_INDEX = 0
    FUNCTION_INDEX = 0
    # create the differents buttons
    for button in BUTTON_LIST:
        COLUMN_INDEX += 1
        Button(WINDOW, text=str(button), command=FUNCTION_LIST[FUNCTION_INDEX]).grid(row=ROW_INDEX, column=COLUMN_INDEX)
        if COLUMN_INDEX == 2:
            ROW_INDEX += 1
            COLUMN_INDEX = 0
        FUNCTION_INDEX += 1

    WINDOW.mainloop()
