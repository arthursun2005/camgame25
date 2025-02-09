'''
Usage: the only function you have to care is genmaze(isHandcraft: bool)
Pass true if you want to get the handcrafted maze
Fixed size 3 * 16 * 16
The random thing follows the format of the handcrafted version
'''

import random

def generate_handcraft():
    return [
        # Level 0: Red
        [".#.....##...#g..",
         ".#####....#.###R",
         "..r#...###....#.",
         "##...#.....##...",
         "..G#######G.####",
         ".####.#1##.####r",
         ".........#....#r",
         "######.#.####...",
         ".......#....####",
         ".##.#########.#.",
         "..#.#.....R....R",
         ".##...####.####.",
         ".#..#...r#.#r..R",
         "#####.####.####.",
         "...r#.#r......#R",
         "#2###.####.####1"],
        # Level 1: Green
        ["g..##...B.....#.",
         "R#...g#####.#.#.",
         ".##.###..g###...",
         "g#.rG.#.###...##",
         "####G##0#...#.#2",
         "...#G2###.#####.",
         ".#.####...#g....",
         ".#......########",
         ".###.##....#Gb##",
         "G.b#B.######R##.",
         "####.##......#..",
         "r.......######.#",
         "####.####R..g#.#",
         "g.........####..",
         "####.######....#",
         "r...........##.0"],
        # Level 2: Blue
        ["....B.......#...",
         ".#######.##b#.#.",
         "...b#....####.#.",
         ".####.####....#.",
         "...b#.#....##.#1",
         ".####1#.########",
         "....###.#...#...",
         ".##b##..#.#...#.",
         ".###.BB##.#####.",
         ".....#..#.#.....",
         "######.##.#.####",
         "#...#...#.#.....",
         "#.#.#.#.#.#....R",
         "..#.#.#.#.#...RR",
         ".##.###...#..GGB",
         ".0#.....###.RBB!"],
    ]


def print_maze(maze):
    for grid in maze:
        print("---START---")
        for row in grid:
            print("".join(row))
        print("---END---")

def generate_maze_2d(grid, start):
    # Random DFS algorithm, implemented iteratively

    n = len(grid)
    maze = [['#' for _ in range(n)] for _ in range(n)]
    avail = [(i, j) for i in range(n) for j in range(n) if grid[i][j] == '.']

    def check(x, y):
        return (0 <= x < n) and (0 <= y < n) and grid[x][y] == '.'
    
    assert (start in avail)
    maze[start[0]][start[1]] = '.'
    stk = [start]
    dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
    
    while stk:
        x, y = stk[-1]
        nxt = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            mx, my = x + dx // 2, y + dy // 2

            # Condition: (nx, ny) wall and (mx, my) anything
            if (check(nx, ny) and maze[nx][ny] == '#') and check(mx, my):
                nxt.append((nx, ny, mx, my))
        
        if nxt:
            nx, ny, mx, my = random.choice(nxt)
            maze[mx][my] = '.'
            maze[nx][ny] = '.'
            stk.append((nx, ny))
        else:
            stk.pop()
    
    return maze

def generate_maze_3d(n):
    # Generate masks
    # Mask of layer 0: lower left covered
    # Mask of layer 1: upper right covered
    # Mask of layer 2: lower right covered
    mask0 = [[('#' if i >= n - 4 and j < 4 else '.') for j in range(n)] for i in range(n)]
    mask1 = [[('#' if i < 4 and j >= n - 4 else '.') for j in range(n)] for i in range(n)]
    mask2 = [[('#' if i >= n - 4 and j >= n - 4 else '.') for j in range(n)] for i in range(n)]

    # Generate layers
    layer0 = generate_maze_2d(mask0, (0, 0))

    crit01 = (-1, -1)
    for off in range(6, -1, -1):
        for x in range(n - 1, n - 5, -1):
            for y in range(n - 1, n - 5, -1):
                if (n - 1) * 2 - (x + y) != off:
                    continue
                if layer0[x][y] == '.':
                    crit01 = (x, y)
    assert (crit01[0] != -1)
    layer1 = generate_maze_2d(mask1, crit01)
    layer0[crit01[0]][crit01[1]] = '1'
    layer1[crit01[0]][crit01[1]] = '0'

    crit12 = (-1, -1)
    for off in range(6, -1, -1):
        for x in range(0, 4):
            for y in range(0, 4):
                if x + y != off:
                    continue
                if layer1[x][y] == '.':
                    crit12 = (x, y)
    layer2 = generate_maze_2d(mask2, crit12)
    layer1[crit12[0]][crit12[1]] = '2'
    layer2[crit12[0]][crit12[1]] = '1'

    return ([layer0, layer1, layer2], (crit01, crit12))

def add_walls(maze, crits):
    # TO BE IMPLEMENTED (trust I'll do it tmr)
    return maze

def carve_blocks(maze):
    n = len(maze[0])

    # Layer 0: carve out lower left
    tel = (-1, -1)
    for i in range(n - 3, n):
        for j in range(2, -1, -1):
            maze[0][i][j] = '.'
            if maze[2][i][j] == '.':
                tel = (i, j)
    assert (tel[0] != -1)
    maze[0][tel[0]][tel[1]] = '2'
    maze[2][tel[0]][tel[1]] = '0'
    if tel == (n - 1, 0):
        maze[0][n - 3][2] = 'r'
    else:
        maze[0][n - 1][0] = 'r'

    # Layer 1: carve out upper right
    tel = (-1, -1)
    for i in range(2, -1, -1):
        for j in range(n - 3, n):
            maze[1][i][j] = '.'
            if maze[2][i][j] == '.':
                tel = (i, j)
    assert (tel[0] != -1)
    maze[1][tel[0]][tel[1]] = '2'
    maze[2][tel[0]][tel[1]] = '1'
    if tel == (0, n - 1):
        maze[1][2][n - 3] = 'g'
    else:
        maze[1][0][n - 1] = 'g'
    
    # Layer 2: carve out lower right
    match = "RGB!"
    for i in range(n - 5, n):
        for j in range(n - 5, n):
            maze[2][i][j] = '.'
            dist = (n - 1) * 2 - (i + j)
            if dist < 4:
                maze[2][i][j] = match[3 - dist]

    maze[2][n - 4][n - 4] = 'b'
    
    return maze

def genmaze(isHandcraft):
    if isHandcraft:
        return generate_handcraft()
    
    n = 16
    maze, start = generate_maze_3d(n)
    maze = add_walls(maze, start)
    maze = carve_blocks(maze)
    # print_maze(maze)
    # print(start)
    return maze

# maze = generate_maze_2d([['.' for j in range(n)] for i in range(n)], (0, 0))
# for row in maze:
#     print("".join(row))

