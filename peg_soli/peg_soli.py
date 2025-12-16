import time
import random

SIZE = 9       
BLOCKS = 6     
POWER_PEGS = 2 
def init_board():
    b = [[1]*SIZE for _ in range(SIZE)]

    for i in range(SIZE):
        for j in range(SIZE):
            if (i < 3 or i > 5) and (j < 3 or j > 5):
                b[i][j] = -1

    b[4][4] = 0  

    for _ in range(BLOCKS):
        r, c = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
        if b[r][c] == 1:
            b[r][c] = 2

    for _ in range(POWER_PEGS):
        r, c = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
        if b[r][c] == 1:
            b[r][c] = 3

    return b

def print_board(b):
    for row in b:
        line = ""
        for cell in row:
            if cell == -1:
                line += "  "
            elif cell == 1:
                line += "O "
            elif cell == 3:
                line += "P "
            elif cell == 2:
                line += "X "
            else:
                line += ". "
        print(line)
    print()

def moves(b):
    m = []
    for r in range(SIZE):
        for c in range(SIZE):
            if b[r][c] not in (1, 3):
                continue
            jump_lengths = [1, 2]
            for jmp in jump_lengths:
                
                if r - (jmp+1) >= 0:
                    path = [b[r-i][c] for i in range(1, jmp+1)]
                    if all(x in (1,3) for x in path if b[r][c] == 3 or x != 2) and b[r-(jmp+1)][c] == 0:
                        m.append((r, c, r-(jmp+1), c))
                if r + (jmp+1) < SIZE:
                    path = [b[r+i][c] for i in range(1, jmp+1)]
                    if all(x in (1,3) for x in path if b[r][c] == 3 or x != 2) and b[r+(jmp+1)][c] == 0:
                        m.append((r, c, r+(jmp+1), c))
                if c - (jmp+1) >= 0:
                    path = [b[r][c-i] for i in range(1, jmp+1)]
                    if all(x in (1,3) for x in path if b[r][c] == 3 or x != 2) and b[r][c-(jmp+1)] == 0:
                        m.append((r, c, r, c-(jmp+1)))
                if c + (jmp+1) < SIZE:
                    path = [b[r][c+i] for i in range(1, jmp+1)]
                    if all(x in (1,3) for x in path if b[r][c] == 3 or x != 2) and b[r][c+(jmp+1)] == 0:
                        m.append((r, c, r, c+(jmp+1)))
    return m

def make(b, r1, c1, r2, c2):
    b[r1][c1] = 0
    dr = (r2 - r1) // max(abs(r2 - r1), 1)
    dc = (c2 - c1) // max(abs(c2 - c1), 1)
    steps = max(abs(r2 - r1), abs(c2 - c1)) - 1
    for i in range(1, steps+1):
        b[r1 + i*dr][c1 + i*dc] = 0
    b[r2][c2] = 1

def undo(b, r1, c1, r2, c2):
    b[r2][c2] = 0
    dr = (r2 - r1) // max(abs(r2 - r1), 1)
    dc = (c2 - c1) // max(abs(c2 - c1), 1)
    steps = max(abs(r2 - r1), abs(c2 - c1)) - 1
    for i in range(1, steps+1):
        b[r1 + i*dr][c1 + i*dc] = 1
    b[r1][c1] = 1

def count(b):
    return sum(x in (1,3) for row in b for x in row)


def solve(b, seq=[]):
    if count(b) == 1 and b[4][4] == 1:
        print("SOLVED!\n")
        print_board(b)
        return True

    for r1, c1, r2, c2 in moves(b):
        make(b, r1, c1, r2, c2)
        print_board(b)
        time.sleep(0.5)
        seq.append((r1, c1, r2, c2))

        if solve(b, seq):
            return True

        undo(b, r1, c1, r2, c2)
        print_board(b)
        time.sleep(0.5)
        seq.pop()

    return False

# Main
def main():
    board = init_board()
    print("Initial board:\n")
    print_board(board)

    if not solve(board):
        print("No solution found.")
    else:
        print("Solved!")

if __name__ == "__main__":
    main()
