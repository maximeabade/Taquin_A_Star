import random
import itertools
import collections
import time


class Node:
    def __init__(self, puzzle, parent=None, action=None, heuristic=None):
        self.puzzle = puzzle
        self.parent = parent
        self.action = action
        self.heuristic = heuristic

    @property
    def state(self):
        return str(self)

    @property
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        yield from reversed(p)

    @property
    def solved(self):
        return self.puzzle.solved

    @property
    def actions(self):
        return self.puzzle.actions

    @property
    def cost(self):
        current_state = self.puzzle.convL()
        return len(list(self.path)) + self.heuristic(current_state)

    def __lt__(self, other):
        return self.cost < other.cost

    def __str__(self):
        return str(self.puzzle)


class Solver:
    def __init__(self, start, heuristic):
        self.start = start
        self.heuristic = heuristic

    def solve(self):
        print("Recherche de solution avec :", self.heuristic.__name__)
        print(self.start.board)
        queue = collections.deque([Node(self.start, heuristic=self.heuristic)])
        seen = set()
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            if node.solved:
                z = list(node.path)
                self.aff5(z)
                print("solution trouvée en", len(z), "coups")
                break
            for move, action in node.actions:
                child = Node(move(), node, action, self.heuristic)
                if child.state not in seen:
                    queue.appendleft(child)
                    seen.add(child.state)

    def solve_Astar(self):
        print("Recherche de solution A* avec :", self.heuristic.__name__)
        print(self.start.board)
        queue = [Node(self.start, heuristic=self.heuristic)]
        seen = set()
        seen.add(queue[0].state)
        while queue:
            queue.sort()
            node = queue.pop(0)
            if node.solved:
                z = list(node.path)
                self.aff5(z)
                print("solution trouvée en", len(z), "coups")
                break
            for move, action in node.actions:
                child = Node(move(), node, action, self.heuristic)
                if child.state not in seen:
                    queue.append(child)
                    seen.add(child.state)

    def solve_Long(self):
        print("Recherche de solution 2 avec :", self.heuristic.__name__)
        queue = collections.deque([Node(self.start, heuristic=self.heuristic)])
        seen = set()
        seen.add(queue[0].state)
        while queue:
            node = queue.pop()
            if node.solved:
                z = list(node.path)
                self.aff5(z)
                print("solution trouvée en", len(z), "coups")
                break
            for move, action in node.actions:
                child = Node(move(), node, action, self.heuristic)
                if child.state not in seen:
                    queue.append(child)
                    seen.add(child.state)

    def aff5(self, p, i=1):
        node = p[0]
        p = p[1:]
        x = node.puzzle.convL()

        print("coup", i, " : ")
        for row in range(0, len(x), node.puzzle.width):
            print(x[row:row + node.puzzle.width])

        if p:
            self.aff5(p, i + 1)
        else:
            print("fin")


class Puzzle:
    def __init__(self, board):
        self.width = len(board[0])
        self.board = board

    @property
    def solved(self):
        tab = []
        sol = True
        for i in range(self.width):
            tab.extend(self.board[i])

        for j in range(len(tab) - 2):
            if tab[j] != (tab[j + 1] - 1):
                sol = False
        if tab[-1] != 0:
            sol = False
        return sol

    @property
    def actions(self):
        def create_move(at, to):
            return lambda: self.move(at, to)

        moves = []
        for i, j in itertools.product(range(self.width), range(self.width)):
            direcs = {'R': (i, j - 1), 'L': (i, j + 1), 'D': (i - 1, j), 'U': (i + 1, j)}

            for action, (r, c) in direcs.items():
                if r >= 0 and c >= 0 and r < self.width and c < self.width and self.board[r][c] == 0:
                    move = create_move((i, j), (r, c)), action
                    moves.append(move)
        return moves

    def shuffle(self):
        puzzle = self
        for k in range(1000):
            puzzle = random.choice(puzzle.actions)[0]()
        x = puzzle.convL()
        print(x)
        self.board = puzzle.board  # Mettez à jour le board
        return Puzzle(self.board)  # Initialisez un nouveau puzzle avec le board mis à jour

    def copy(self):
        board = []
        for row in self.board:
            board.append([x for x in row])
        return Puzzle(board)

    def move(self, at, to):
        copy = self.copy()
        i, j = at
        r, c = to
        copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
        return copy

    def convL(self):
        L = []
        for row in self.board:
            L.extend(row)
        return L

    def hamming_heuristic(self, current):
        count = 0
        goal = list(range(self.width * self.width))

        for i in range(len(current) - 1):
            if current[i] != goal[i]:
                count += 1

        return count

    def manhattan_heuristic(self, current):
        total_distance = 0
        goal = [[0] * self.width for _ in range(self.width)]
        for i in range(self.width):
            for j in range(self.width):
                goal[i][j] = i * self.width + j + 1
            goal[self.width - 1][self.width - 1] = 0

        for i in range(self.width):
            for j in range(self.width):
                value = current[i * self.width + j]
                if value != 0:
                    goal_row, goal_col = divmod(value - 1, self.width)
                    total_distance += abs(i - goal_row) + abs(j - goal_col)

        return total_distance

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.board:
            yield from row


def main():
    board = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    puzzl = Puzzle(board)

    while True:
        print("\n1 - Mélanger")
        print("2 - Résoudre avec heuristique de Hamming - Can be long...")
        print("3 - Résoudre avec heuristique de Manhattan")
        print("4 - Quitter")

        choice = input("Choisissez une option : ")

        if choice == '1':
            puzzl = puzzl.shuffle()
            x = puzzl.convL()
        elif choice == '2':
            heuristic = puzzl.hamming_heuristic
            solver = Solver(puzzl, heuristic)
            solver.solve_Astar()
        elif choice == '3':
            heuristic = puzzl.manhattan_heuristic
            solver = Solver(puzzl, heuristic)
            solver.solve_Astar()
        elif choice == '4':
            break
        else:
            print("Option invalide. Veuillez choisir une option valide.")


if __name__ == "__main__":
    main()