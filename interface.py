#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create an ensemble of functions for a tkinter interface and widgets.
@author: TOUMI Anouar
"""

# List of import
import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
import webbrowser
from functools import partial
import BWT as bwt
import huffman_code as hc
from datetime import datetime
import ast


def set_filepath(seq_or_path):
    """
    Fetch a file from local machine and set it in seq_or_path StringVar
    @param seq_or_path:
    @return:
    """
    # open a tkinter filedialog popup to ask for a file from the local machine repository
    file = tk.filedialog.askopenfilename(filetypes=[("", ".fasta, .txt")])
    # setting the value on seq_or_path StringVar by .set() method
    seq_or_path.set(file)
    return file


def save(title, data, huffman=False):
    """
    Save function creating a unique .txt file containing only the result if the huffman is True or the dictionary
    and result if huffman is True
    @param title: str
    @param data: str or List
    @param huffman: Boolean
    @return: None
    """
    # Create a unique (if not used multiple time at the exact same seconde) title using datetime
    title += "_" + datetime.now().strftime("%m%d%Y%H%M%S")
    # Creating a file in write mode and replacing space in title by underscore
    save_file = open(str(title.replace(" ", "_")) + ".txt", "w")
    #  if Huffman is False, we just write the result data in the file
    if huffman is False:
        save_file.write(data)
    else:
        # if Huffman is True we have to write in the first line the dictonary from huffman code and in the second
        # line the data
        save_file.write(str(data[1]) + '\n')
        save_file.write(data[0])
    # Close the file
    save_file.close()


def show_result(title, result, huffman=False):
    """
    Function to create a new windows and display the result
    @param title: str
    @param result: str or List
    @param huffman: Boolean
    @return: None
    """
    # Creating tkinter window and it's characteristic
    new_window = tk.Tk()
    new_window.title(title)
    new_window.geometry("500x280")

    # Creating a tkinter widgets when it's not for a huffman function
    if huffman is False:
        # Message widgets containing the result and grid it
        tk.Message(new_window, text=result, font="Arial", bg="white", padx=5, pady=5,
                   width=200).grid(row=1, column=0, columnspan=1)
        # Button using the save function to crate a file containing the result on the same repository
        tk.Button(new_window, text="Enregistrer", command=lambda: save(title, result),
                  padx=5, pady=5).grid(row=0, column=0)

    else:
        # Here we are only changing the argument of save functin and also the result to display when huffman is True
        tk.Message(new_window, text=result[0], font="Arial", bg="white",
                   padx=5, pady=5, width=200).grid(row=1, column=0, columnspan=1)
        tk.Button(new_window, text="Enregistrer", command=lambda: save(title, result, True),
                  padx=5, pady=5).grid(row=0, column=0)

    tk.Button(new_window, text="Fermer", command=new_window.destroy, padx=5, pady=5).grid(row=0, column=1)
    # Running the tkinter window
    new_window.mainloop()


def show_result_step(title, result):
    """
    A clone function of show_result to print each step of a function in a Listbox widgets
    @param title: str
    @param result: List
    @return: None
    """
    # Creating tkinter window and it's characteristic
    new_window = tk.Tk()
    new_window.title(title)
    new_window.geometry("700x500")

    # Creating tkinter Listbox and Scrollbar
    result_listbox = tk.Listbox(new_window, width=50, height=200)
    # Filling the Listbox with the eahc element from result List
    for element in result:
        result_listbox.insert(tk.END, str(element))
    # Parametring variable around the Listbox and Scrollbar
    result_listbox.pack(side=tk.LEFT, fill="y", expand=True)
    scroll_y = tk.Scrollbar(new_window)
    scroll_x = tk.Scrollbar(new_window, orient="horizontal")
    result_listbox.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.pack(side=tk.RIGHT, fill="y")
    scroll_y.config(command=result_listbox.yview)
    scroll_x.pack(side=tk.BOTTOM, fill="x")
    scroll_x.config(command=result_listbox.xview)

    # Adding a save and quit button and placing it
    tk.Button(new_window, text="Enregistrer", command=lambda: save(title, result), padx=3).pack(side=tk.LEFT,
                                                                                                anchor="n", padx=10,
                                                                                                pady=5)
    tk.Button(new_window, text="Fermer", command=new_window.destroy, padx=3).pack(side=tk.LEFT, anchor="n", padx=10,
                                                                                  pady=5)
    # Running the tkinter window
    new_window.mainloop()


def open_help_page():
    """
    Function to open a webpage to my GitHub page with the Readme at the bottom
    @return: None
    """
    # Using webbrowser library to open the webpage
    webbrowser.open("https://github.com/AuranoO/Projet-Algo-M1")


def check_file(to_check, huffman=False):
    """
    Check the StringVar from the entrybox if it's a path to a file then we will read and take sequence
    from the file and return it.
    If not we will return a string from StringVar.
    If huffman is True then we read the file differently and return a list containing the dictionary from huffman code
    and content from our huffman function.
    @param to_check: StringVar
    @param huffman: Boolean
    @return: str or list
    """
    # Initialize the content variable
    content = ""
    if huffman is False:
        # We are checking if the to_check StringVar is a path to a file
        if os.path.isfile(to_check.get()):
            # Opening and reading the file
            f = open(str(to_check.get()), 'r')
            f = f.readlines()
            for line in f:
                # Passing if the line begin by a >
                if line.startswith(">"):
                    pass
                else:
                    # Add in content the value of each line from file
                    content += line.replace("\n", "")
        else:
            # If to_check is juste a sequence we are just taking it
            content = to_check.get()
        return content
    # if huffman is True, we are doing similar things
    if os.path.isfile(to_check.get()):
        f = open(str(to_check.get()), 'r')
        f = f.readlines()
        headline = True
        for line in f:
            if headline is True:
                # Using ast library to create a dictionary from line in file
                dict_huff = ast.literal_eval(line)
                headline = False
            else:
                # Add in content the value of each line from file
                content += line
        # return  a list of huffman dictionary and content
        return [dict_huff, content]


def display_bwt(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq)
    show_result("Transformée de BWT", bwt.bwt_transformation(seq))


def display_huffman(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq)
    show_result("Compression de Huffman", hc.encode(seq), True)


def display_binary(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq)
    show_result("Sequence vers Binaire",
                hc.from_seq_to_binary(seq, hc.create_huffman_code(hc.create_dico_frequence(seq))), True)


def display_bwt_step(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq)
    show_result_step("Transformée de BWT étape par étape", bwt.realignement_sequence(bwt.add_dollars(seq)))


def display_reverse_huffman(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq, True)
    show_result("Décompression de Huffman", hc.decode([seq[0], seq[1]]), True)


def display_ascii(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq, True)
    show_result("Binaire vers ASCII", hc.from_binary_to_ascii([seq[1], seq[0]]), True)


def display_reverse_bwt(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq)
    show_result("Détransformée de BWT", bwt.get_sequence_rebuild(bwt.get_matrix(seq)))


def display_binary_seq(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq, True)
    show_result("Binaire vers sequence", hc.from_binary_to_seq(seq[1], seq[0]), True)


def display_ascii_binary(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq, True)
    show_result("ASCII vers binaire", hc.from_ascii_to_binary(seq), True)


def reverse_bwt_step(seq):
    """
    Use the show_result function to display the data obtain from the respective function
    @param seq: StringVar
    @return: None
    """
    seq = check_file(seq)
    show_result_step("Détransformée de BWT étape par étape", bwt.get_matrix(seq, True))


def main_interface():
    """
    main interface function create the first tkinter window divided by 3 frames
    each of them comporting different widgets
    @return: None
    """
    # création de la fenetre
    win = tk.Tk()
    # taille de la fenetre
    win.geometry('650x350')
    # titre de la fenêtre
    win.title("BWT et Huffman Compression")
    seq_or_path = tk.StringVar()
    # délimite la fenetre tkinter en plusieurs cadre placer par la methode grid
    top_frame = tk.Frame(win, width=520, pady=3)
    mid_frame = tk.Frame(win, width=520, pady=20)
    bottom_frame = tk.Frame(win, width=520)

    top_frame.grid(row=0)
    mid_frame.grid(row=1)
    bottom_frame.grid(row=3)

    # Créer les widgets du cadre supérieur de la fenetre placer par la methode grid
    label_file = tk.Label(top_frame, text="Entrée une séquence ou sélectionner un fichier", font='Arial 11 bold')
    entry_seq = tk.Entry(top_frame, textvariable=seq_or_path, width=55)
    file_button = tk.Button(top_frame, text="Parcourir", command=lambda: set_filepath(seq_or_path))

    label_file.grid(row=0, columnspan=1, pady=3, padx=40)
    entry_seq.grid(row=1, column=0)
    file_button.grid(row=1, column=1)

    # Creation de deux liste qui permettrons associés 10 boutons à leurs fonctions
    list_button_mid_frame = ['Sequence vers BWT', 'Sequence vers Huffman', "Sequence vers binaire",
                             'Sequence vers BWT étape par étape', 'Huffman vers sequence',
                             "Binaire vers ASCII", 'BWT vers sequence', "Binaire vers sequence",
                             "ASCII vers binaire", "BWT vers sequence étape par étape"]
    list_function = [display_bwt, display_huffman, display_binary,
                     display_bwt_step, display_reverse_huffman,
                     display_ascii, display_reverse_bwt, display_binary_seq, display_ascii_binary, reverse_bwt_step]

    # Compteur qui permettrons de suivre la ligne et la colonne pour les boutons du cadre du mileu
    index_row = 0
    index_column = 0

    # Boucle qui créer les boutons et les placent à l'aide des variables créer ci-dessus
    for i in range(0, len(list_button_mid_frame)):
        index_column += 1
        tk.Button(mid_frame, text=list_button_mid_frame[i], command=partial(list_function[i], seq_or_path)).grid(
            row=index_row, column=index_column, padx=2, pady=10)
        if index_column == 3:
            index_row += 1
            index_column = 0

    # Créer les widgets du cadre inférieure de la fenetre placer par la methode grid
    help_button = tk.Button(bottom_frame, text="Aide", command=open_help_page)
    close_button = tk.Button(bottom_frame, text="Fermer", command=win.destroy)
    void_label = tk.Label(bottom_frame, text="                                                                        ")

    help_button.grid(row=0, column=0, sticky="w")
    void_label.grid(row=0, column=1)
    close_button.grid(row=0, column=2, sticky="e")

    # Running the tkinter window
    win.mainloop()


if __name__ == "__main__":
    main_interface()
