"""
NOT IN USE ATM.
def squarer(i, j, new, squares, sq):
    if sq is (0 or 3 or 6):
        if j is (0 or 3 or 6):
            squares[sq][i] = new
        elif j is (1 or 4 or 7):
            squares[sq][i+3] = new
        elif j is (2 or 5 or 8):
            squares[sq][i+6] = new
    if sq is (1 or 4 or 7):
        if j is (0 or 3 or 6):
            squares[sq][i-3] = new
        elif j is (1 or 4 or 7):
            squares[sq][i] = new
        elif j is (2 or 5 or 8):
            squares[sq][i+3] = new
    if sq is (2 or 5 or 8):
        if j is (0 or 3 or 6):
            squares[sq][i-6] = new
        elif j is (1 or 4 or 7):
            squares[sq][i-3] = new
        elif j is (2 or 5 or 8):
            squares[sq][i] = new
"""

def solverExclusion(rows, squares):
    # updates rows based on child input
    new_rows = rows
    col_a, col_b, col_c, col_d, col_e, col_f, col_g, col_h, col_i = [], [], [], [], [], [], [], [], []
    new_cols = [col_a, col_b, col_c, col_d, col_e, col_f, col_g, col_h, col_i]

    # updates columns
    for i in range(9):
        for j in new_rows:
            new_cols[i].append(j[i])

    """
    Main yield loop
    function:
    1. check for 0 in determined row
    2. if value == 0 repeat from 1 till 9
    3. check if value can be assigned each 1-9 value based on rows, columns and squares test
    4. yield generator
    5. repeat for each 1-9 value
    """
    check = False
    counter = 0
    for j in range(len(rows)):
        for i in range(len(rows)):
            if rows[j][i] == 0:
                for new in range(1,10):
                    if new not in new_rows[j]:
                        if new not in new_cols[i]:
                            if i < 3 and j < 3 and new not in squares[0]:
                                temp = new
                                counter += 1
                            elif 3 <= i < 6 and j < 3 and new not in squares[1]:
                                temp = new
                                counter += 1
                            elif 6 <= i < 9 and j < 3 and new not in squares[2]:
                                temp = new
                                counter += 1
                            elif i < 3 and 3 <= j < 6 and new not in squares[3]:
                                temp = new
                                counter += 1
                            elif 3 <= i < 6 and 3 <= j < 6 and new not in squares[4]:
                                temp = new
                                counter += 1
                            elif 6 <= i < 9 and 3 <= j < 6 and new not in squares[5]:
                                temp = new
                                counter += 1
                            elif i < 3 and 6 <= j < 9 and new not in squares[6]:
                                temp = new
                                counter += 1
                            elif 3 <= i < 6 and 6 <= j < 9 and new not in squares[7]:
                                temp = new
                                counter += 1
                            elif 6 <= i < 9 and 6 <= j < 9 and new not in squares[8]:
                                temp = new
                                counter += 1
                # Not happy with this part
                if counter is 1:
                    new_rows[j][i] = temp
                    new_cols[i][j] = temp
                    check = True
                counter = 0
    if check is False:
        new_rows = False
    yield new_rows


def solverBruteForce(rows, squares):
    # updates rows based on child input
    new_rows = rows
    col_a, col_b, col_c, col_d, col_e, col_f, col_g, col_h, col_i = [], [], [], [], [], [], [], [], []
    new_cols = [col_a, col_b, col_c, col_d, col_e, col_f, col_g, col_h, col_i]
    # updates columns
    for i in range(9):
        for j in new_rows:
            new_cols[i].append(j[i])
    # determines the row to be manipulated
    for i in range(len(rows)):
        if 0 in rows[i]:
            j = i
            break
    """
    Main yield loop
    function:
    1. check for 0 in determined row
    2. if value == 0 repeat from 1 till 9
    3. check if value can be assigned each 1-9 value based on rows, columns and squares test
    4. yield generator
    5. repeat for each 1-9 value
    """
    for i in range(len(rows)):
        if rows[j][i] == 0:
            for new in range(1,10):
                if new not in new_rows[j]:
                    if new not in new_cols[i]:
                        if i < 3 and j < 3 and new not in squares[0]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
                        elif 3 <= i < 6 and j < 3 and new not in squares[1]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
                        elif 6 <= i < 9 and j < 3 and new not in squares[2]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
                        elif i < 3 and 3 <= j < 6 and new not in squares[3]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
                        elif 3 <= i < 6 and 3 <= j < 6 and new not in squares[4]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
                        elif 6 <= i < 9 and 3 <= j < 6 and new not in squares[5]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
                        elif i < 3 and 6 <= j < 9 and new not in squares[6]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
                        elif 3 <= i < 6 and 6 <= j < 9 and new not in squares[7]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
                        elif 6 <= i < 9 and 6 <= j < 9 and new not in squares[8]:
                            new_rows[j][i] = new
                            new_cols[i][j] = new
                            yield new_rows
            break
