import random
from datetime import datetime

try:
    import tkinter as tk  # python 3
    from tkinter import font as tkfont  # python 3
except ImportError:
    import Tkinter as tk  # python 2
    import tkFont as tkfont  # python 2

from Flashcard import Flashcard

class StudyFrame(tk.Frame):

    NO_FLASHCARD_FOUND_TEXT = "Welcome to Flashcards!\n\nTo add some flashcards, click Flashcards in the Menu on the top of this window. Then click Add new flaschard button."
    NO_DECK_FOUND_FLASHCARD_TEXT = "Welcome to Flashcards!\n\nTo create a deck, click Decks in the Menu on the top of this window. Then click New Deck button."
    NO_DECK_FOUND_STATUS_TEXT = "Welcome to Flashcards!"

    def __init__(self, parent, controller):
        # Initialize super class
        tk.Frame.__init__(self, parent)

        # Assign passed controller attribute to the class attribute
        self.controller = controller

        # label = tk.Label(self, text="This is page 1", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Go to the start page",
        #                    command=lambda: controller.show_frame("StartPage"))
        # button.pack()

        # Holds the current deck's index in the decks list
        self.deck_index = int()

        # Holds the current flashcard's index in the flashcards list
        self.flashcard_index = int()

        # Holds displayed flashcard object
        self.flashcard = None

        # Holds if card is flipped
        self.flipped = False

        self.show_only_due_flashcards = True

        self.randomized_flashcards: [Flashcard] = None

        # # When object is initialized there is not any deck selected. Therefore deck index and flashcard index will be
        # # -1.
        # self.deck_index = -1
        # self.flashcard_index = -1

        # # self.decks holds the Deck list
        # self.decks = controller.database_manager.decks
        #
        # # self.deck holds the current deck. As the main window is now being initialized, there is no selected deck.
        # self.deck: Deck = None
        #
        # # self.flashcards will be a list holding the flashcards of the current deck.
        # self.flashcards = [Flashcard]
        #
        # # As there is not any selected Deck, current flashcard will be None.
        # self.flashcard: Flashcard = None

        # Create two frames, top and bottom
        self.top_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.status_frame = tk.Frame(self)

        self.top_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.bottom_frame.grid(row=1, column=0, pady=10, padx=10, sticky="new")
        self.status_frame.grid(row=2, column=0, pady=0, padx=10, sticky="new")

        self.index_card_image = tk.PhotoImage(master=self.top_frame, file='image/index_card.gif')
        self.flashcard_label = tk.Label(self.top_frame, text="", wraplength=350,
                                        font=("Arial", 14, "bold"),
                                        image=self.index_card_image, compound=tk.CENTER)
        self.flashcard_label.grid(row=0, column=0)

        # Create three buttons for the bottom frame
        self.very_hard_button = tk.ttk.Button(self.bottom_frame, text='Very Hard',
                                         command=self.very_hard_button_clicked)
        self.hard_button = tk.ttk.Button(self.bottom_frame, text='Hard',
                                         command=self.hard_button_clicked)
        self.normal_button = tk.ttk.Button(self.bottom_frame, text='Show Answer',
                                         command=self.flip)
        self.easy_button = tk.ttk.Button(self.bottom_frame, text='Easy',
                                         command=self.easy_button_clicked)
        self.super_easy_button = tk.ttk.Button(self.bottom_frame, text='Super Easy',
                                         command=self.super_easy_button_clicked)

        # self.left_button = tk.ttk.Button(self.bottom_frame, text='Previous',
        #                                  command=self.show_previous_flashcard)
        # self.show_hide_button = tk.ttk.Button(self.bottom_frame, text='Flip', command=self.flip)
        # self.right_button = tk.ttk.Button(self.bottom_frame, text='Next', command=self.show_next_flashcard)

        # self.show_hide_button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        # self.left_button.pack(side='left')
        self.very_hard_button.grid(row=0, column=1, padx=10, pady=5)
        self.hard_button.grid(row=0, column=2, padx=10, pady=5)
        self.normal_button.grid(row=0, column=3, padx=10, pady=5)
        self.easy_button.grid(row=0, column=4, padx=10, pady=5)
        self.super_easy_button.grid(row=0, column=5, padx=10, pady=5)

        # Center group of buttons horizontally by creating empty columns on the left and right side,
        # and giving them a weight so that they consume all extra space
        # https://stackoverflow.com/a/48934682/3780985
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(6, weight=1)

        # Create "Deck Table" as a TreeView
        # This object will be used to edit flashcards in the deck
        self.table = tk.ttk.Treeview(self, columns=["Question", "Answer"])

        # Define table columns
        self.deck_table_columns = ["Question", "Answer"]
        self.table.column("#0", width=120, minwidth=25)
        self.table.column("Question", anchor="w", width=120)
        self.table.column("Answer", anchor="e", width=120)

        # Define table column headings (headers?)
        self.table.heading("#0", text="Label", anchor="w")
        self.table.heading("Question", text="Question", anchor="w")
        self.table.heading("Answer", text="Answer", anchor="e")

        # Add a status bar
        status_bar_text = self.status_bar_text()
        print("status_bar_text: ", status_bar_text)
        self.status_bar = tk.ttk.Label(self.status_frame, text=status_bar_text, border=1, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X)
        # self.status_bar = tkinter.ttk.Label(self.status_frame, text=status_bar_text, border=1, relief=tkinter.SUNKEN)
        # self.status_bar.grid(row=1, column=0, columnspan=3)

        # DEBUG: Load deck
        # self.load_deck(0)
        self.prepare_view(show_only_due_flashcards=True)

    def load_flashcard(self):
        deck = self.controller.database_manager.deck
        print("load_flashcard")
        print("self.flashcard_index: ", self.flashcard_index)
        # self.flashcard = self.flashcards[self.flashcard_index]
        if deck is not None:
            if self.flashcard_index < len(self.randomized_flashcards):
                flashcard = self.randomized_flashcards[self.flashcard_index]
                self.flashcard = flashcard
                # flashcard = deck.flashcards[self.flashcard_index]
                if self.flipped:
                    self.flashcard_label.config(fg="green")
                    self.flashcard_label.config(text=flashcard.answer)
                    # todo
                else:
                    self.flashcard_label.config(fg="red")
                    self.flashcard_label.config(text=flashcard.question)
                self.set_status_bar_text()

    def show_next_flashcard(self):
        deck = self.controller.database_manager.deck
        if deck is not None:
            if self.flashcard_index < len(self.randomized_flashcards) - 1:
                # flashcards = self.controller.database_manager.deck.flashcards
                flashcards = self.randomized_flashcards
                self.flipped = False
                self.flashcard_index += 1
                self.load_flashcard()
                self.configure_buttons()
                print("self.flashcard_index: ", self.flashcard_index, "; len(flashcards): ", len(flashcards))
                # self.set_button_status()
            else:
                tk.messagebox.showinfo("All done!", "All done! Congrats!")
                self.controller.show_manage_decks_frame()

    def show_previous_flashcard(self):
        # flashcards = self.controller.database_manager.deck.flashcards
        flashcards = self.randomized_flashcards
        if self.flashcard_index != 0:
            self.flipped = False
            self.flashcard_index -= 1
            self.load_flashcard()
            print("self.flashcard_index: ", self.flashcard_index, "; len(flashcards): ", len(flashcards))
            # self.set_button_status()

    # def set_button_status(self):
    #     if self.flashcard_index == 0:
    #         self.left_button.config(state='disabled')
    #     else:
    #         self.left_button.config(state='enabled')
    #     # if self.flashcard_index == len(self.controller.database_manager.deck.flashcards) - 1:
    #     if self.flashcard_index == len(self.randomized_flashcards) - 1:
    #         self.right_button.config(state='disabled')
    #     else:
    #         self.right_button.config(state='enabled')

    # def flip(self):
    #     self.flipped = not self.flipped
    #     self.load_flashcard()

    def flip(self):
        if self.flipped:
            # Answer has already been shown. Now this button acts for "Normal" button tapped.
            self.normal_button_clicked()
        else:
            # Answer has not been shown before. Show the answer and toggle the flag.
            self.flipped = True
            self.load_flashcard()
            self.configure_buttons()

    def very_hard_button_clicked(self):
        self.process_answer(grade=0)
        self.show_next_flashcard()

    def hard_button_clicked(self):
        self.process_answer(grade=1)
        self.show_next_flashcard()

    def normal_button_clicked(self):
        self.process_answer(grade=2)
        self.show_next_flashcard()

    def easy_button_clicked(self):
        self.process_answer(grade=3)
        self.show_next_flashcard()

    def super_easy_button_clicked(self):
        self.process_answer(grade=4)
        self.show_next_flashcard()

    def configure_buttons(self):
        if self.flipped:
            self.super_easy_button.grid()
            self.easy_button.grid()
            self.hard_button.grid()
            self.very_hard_button.grid()
            self.normal_button.config(text="Normal")
        else:
            self.super_easy_button.grid_remove()
            self.easy_button.grid_remove()
            self.hard_button.grid_remove()
            self.very_hard_button.grid_remove()
            self.normal_button.config(text="Show Answer")

    def set_status_bar_text(self):
        self.status_bar.config(text=self.status_bar_text())

    def status_bar_text(self):
        deck = self.controller.database_manager.deck
        if deck is None:
            return StudyFrame.NO_DECK_FOUND_STATUS_TEXT
        elif len(deck.flashcards) == 0:
            return StudyFrame.NO_DECK_FOUND_STATUS_TEXT
        else:
            print()
            # last_study_datetime_string = deck.last_study_datetime.strftime("%m/%d/%Y, %H:%M:%S")
            # print("deck.last_study_datetime: ", deck.last_study_datetime, " type: ", type(deck.last_study_datetime))
            # print("deck.title: ", deck.title)
            flashcard_count = ""
            if self.randomized_flashcards is not None:
                flashcard_count = len(self.randomized_flashcards)
                text = "Deck: " + deck.truncated_title() + \
                   " | Flashcard " + str(self.flashcard_index + 1) + " out of " + str(flashcard_count)
            else:
                text = ""
            return text

    def randomize_deck(self):
        deck = self.controller.database_manager.deck
        flashcards = deck.flashcards
        if self.show_only_due_flashcards:
            flashcards = deck.due_flashcards
        if deck is not None:
            try:
                self.randomized_flashcards = flashcards
                random.shuffle(self.randomized_flashcards)
                # self.randomized_flashcards.shuffle()
            except Exception as error:
                print("Exception randomize_deck: ", error)

    def prepare_view(self, show_only_due_flashcards):
        self.show_only_due_flashcards = show_only_due_flashcards
        deck = self.controller.database_manager.deck
        result = False
        self.flashcard_index = 0
        if deck is None:
            # self.right_button.config(state="disabled")
            # self.left_button.config(state="disabled")
            self.normal_button.config(state="disabled")
            self.flashcard_label.config(text=StudyFrame.NO_DECK_FOUND_FLASHCARD_TEXT)
            result = True
        else:
            deck.set_due_flashcards(self.controller.database_manager)
            self.randomize_deck()
            # todo clean
            if len(deck.flashcards) < 2:
                pass
                # self.right_button.config(state="disabled")
                # self.left_button.config(state="disabled")
            else:
                pass
                # self.right_button.config(state="enabled")
                # self.left_button.config(state="enabled")

            if len(deck.flashcards) < 1:
                self.normal_button.config(state="disabled")
                print("Flashcard cannot be loaded because there is no flashcard.")
                self.flashcard_label.config(text=StudyFrame.NO_FLASHCARD_FOUND_TEXT)
            else:
                self.load_flashcard()
                self.normal_button.config(state="enabled")
        self.set_status_bar_text()
        self.configure_buttons()
        return result

    def start_study_session(self):
        deck = self.controller.database_manager.deck
        if deck is not None:
            deck.set_last_study(self.controller.database_manager)
            self.flipped = False

    def process_answer(self, grade):
        self.flashcard.process_answer(grade=grade, database_manager=self.controller.database_manager)