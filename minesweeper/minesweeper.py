import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0
        # cell is a pair (i,j)

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    # individually for each sentence, there is limited information you can get.
    # update only when all is known to be safe, or mine

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            print("Cells set are all safe: ", self.cells)
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        updated_sentence = set()
        for x in self.cells:
            if x != cell:
                updated_sentence.add(x)
            else:
                self.count -= 1
        self.cells = updated_sentence
        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        updated_sentence = set()
        for x in self.cells:
            if x != cell:
                updated_sentence.add(x)
        self.cells = updated_sentence

        # raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # # 1)
        # self.moves_made.add(cell)
        #
        # # 2)
        # """mark the cell as a safe cell, updating any sentences that contain the cell"""
        # self.mark_safe(cell)  # AI mark_safe has already taken care of loop
        # # 3)
        # new_cells = set()
        # for i in range(cell[0]-1, cell[0]+2):
        #     for j in range(cell[1]-1, cell[1]+2):
        #         # ignore (i,j)
        #         if (i, j) == cell:
        #             continue
        #         if (i, j) in self.safes:
        #             continue
        #         # if it is a mine, reduce uncertainty count by 1
        #         if (i, j) in self.mines:
        #             count = count - 1
        #             continue
        #         # include those not determined to be mine or safes
        #         if 0 <= i < self.height and 0 <= j < self.width:
        #             new_cells.add((i, j))
        # # add the new sentence to the AI's KB
        # print(f'Move on cell: {cell} has added sentence to Knowledge {new_cells} = {count}')
        # new_sentence = Sentence(new_cells, count)
        # self.knowledge.append(new_sentence)
        #
        # # 4) iteratively mark new guaranteed safe and mines
        # """
        # 1. update when cell set 1 is the subset of cell set 2
        # """
        # update_needed = True
        #
        # while update_needed:
        #     update_needed = False
        #     safes = set()
        #     mines = set()
        #
        #     # Try to get new information, if yes, new information can
        #     # be provided, then set update to be true, cross examine each
        #     # pair of sentence to draw new conclusion
        #     for sentence in self.knowledge:
        #         safes = safes.union(sentence.known_safes())
        #         mines = mines.union(sentence.known_mines())
        #     print("safes list so far ", safes)
        #     if safes:
        #         update_needed = True
        #         for cell in safes:
        #             self.mark_safe(cell)
        #     if mines:
        #         update_needed = True
        #         for cell in mines:
        #             self.mark_safe(cell)
        #     # remove empty sentence after you updated
        #     # i.e. {A, E, D} = 0, after update on A, E, D mark_safe, {0} = 0
        #     """
        #     non_empty = set()
        #     for sentence in self.knowledge:
        #         if len(sentence.cells):
        #             non_empty.add(sentence.cells)
        #     self.knowledge = non_empty
        #     """
        #     self.knowledge[:] = [x for x in self.knowledge if len(x.cells)]
        #
        #     # try to examine each pair of sentence for subset
        #     for sentence_1 in self.knowledge:
        #         for sentence_2 in self.knowledge:
        #
        #             # ignore if sentence is identical
        #             if sentence_1 == sentence_2:
        #                 continue
        #
        #             # error raised if cell < count
        #             if len(sentence_1.cells) < sentence_1.count:
        #                 print('Error - sentence with count > cell number')
        #                 raise ValueError
        #
        #             # symmetric, set operation:
        #             if sentence_1.cells.issubset(sentence_2.cells):
        #                 new_cells = sentence_2.cells - sentence_1.cells
        #                 new_count = sentence_2.count - sentence_1.count
        #                 new_sentence = Sentence(new_cells, new_count)
        #
        #                 # add new sentence to KB if haven't existed
        #                 if new_sentence not in self.knowledge:
        #                     update_needed = True
        #                     self.knowledge.append(new_sentence)
        # step 1 add move into moves_made
        self.moves_made.add(cell)
        # step 2 mark the cell as safe
        self.mark_safe(cell)
        # step 3 add the new sentence
        neighbors = []
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.height and 0 <= j < self.width and (i, j) != cell:
                    if (i, j) in self.mines:
                        # we already know that (i, j) is mine, decrease count by 1
                        count -= 1
                    elif (i, j) in self.safes:
                        # we already know that (i, j) is safe, do nothing
                        pass
                    else:
                        # unknown cell, add into neighbours
                        neighbors.append((i, j))
        self.knowledge.append(Sentence(neighbors, count))  # add the knowledge

        made_changes = True
        while made_changes:
            made_changes = False
            # step 4 start inferring:
            iter_mines = []
            iter_safes = []
            # phase I, basic inference from each sentence
            for sentence in self.knowledge:
                sent_safes = sentence.known_safes()
                sent_mines = sentence.known_mines()
                for safe in sent_safes:
                    if safe not in self.safes:
                        # detected new safe
                        self.safes.add(safe)
                        iter_safes.append(safe)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_available = self.safes - self.moves_made
        print("Those are currently safe cells!", self.safes)
        if safe_available:
            next_move = safe_available.pop()
            print("Safe move available!", next_move)
            return next_move
        else:
            print("No Save Move available!")
            return None

        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines

        This function will be called if a safe move is not possible
        """
        total_cells = set()
        for i in range(self.width):
            for j in range(self.height):

                # add all cells in board
                total_cells.add((i, j))
        choice = total_cells - (self.mines.union(self.moves_made))
        if not choice:
            # No other move available
            print("No move available, the rest is all bomb!")
            return None
        else:
            return random.choice(list(choice))

        # raise NotImplementedError
