import rubik
from collections import deque

def shortest_path(start, end):
    if start == end: return []
    fparents = {start: None}
    bparents = {end: None}
    fmoves  = {}
    bmoves = {}
    for move in rubik.quarter_twists:
        fmoves[move] = move
        bmoves[rubik.perm_inverse(move)] = move
    forward = (fmoves, fparents, bparents)
    backward = (bmoves, bparents, fparents)
    queue = deque([(start, forward), (end, backward), None])

    for i in xrange(7):
        while True:
            vertex = queue.popleft()
            if vertex is None:
                queue.append(None)
                break
            position = vertex[0]
            moves, parents, other_parents = vertex[1]
            for move in moves:
                nextp = rubik.perm_apply(move, position)
                if nextp not in parents:
                    parents[nextp] = (moves[move], position)
                    queue.append((nextp, vertex[1]))
                    if nextp in other_parents:
                        forwardp = path(nextp, fparents)
                        backwardp = path(nextp, bparents)
                        backwardp.reverse()
                        return forwardp + backwardp
    return None

def path(position, parents):
    result = []
    while True:
        move_p = parents[position]
        if move_p is None:
            result.reverse()
            return result
        result.append(move_p[0])
        position = move_p[1]
