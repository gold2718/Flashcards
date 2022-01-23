#   Program FlashCards
#
#   Copyright 2020 Ertugrul Harman
#
#       E-mail  : harmancode@gmail.com
#       Twitter : https://twitter.com/harmancode
#       Web     : https://harman.page
#
#   This file is part of Flashcards.
#
#   Flashcards is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Run the Flashcards application by Ertugrul Harman."""

import argparse
import sys
from Program import Program

def main():
    parser = argparse.ArgumentParser(description=__doc__)

    help_str = "Path to a Flashcards database (stored session) file"
    parser.add_argument("--database", metavar='<Flashcards database file>',
                        type=str, required=False, default="Flashcards.db",
                        help=help_str)
    args = parser.parse_args(sys.argv[1:])
    db_path = args.database
    program = Program(db_path)
    program.mainloop()

# Call the main function
if __name__ == "__main__":
    main()
