from math import sqrt
from random import randint
from queue import Queue


class Possition:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def pos_sum(self, a):
        return Possition(self.x + a.x, self.y + a.y)

    def equal(self, a):
        return (self.x == a.x and self.y == a.y)

    def is_valid(self, lab):
        if self.x < 0 or self.y < 0 or self.x >= lab.n or self.y >= lab.m:
            return False

        if lab.laberinto[self.x][self.y] == "X":
            return False

        return True

    def esSalida(self, lab):
        if self.is_valid(lab) and lab.laberinto[self.x][self.y] == 'S':
            return True

        return False

    def is_seen(self, lab):
        if self.is_valid(lab) and lab.laberinto[self.x][self.y] == 'V':
            return True

        return False
    
    def is_wall(self, lab):
        if self.x < 0 or self.y < 0 or self.x >= lab.n or self.y >= lab.m:
            return False

        if lab.laberinto[self.x][self.y] != "X":
            return False

        return True

    def get_walls(self, lab):
        walls = []

        for m in moves:
            new_pos = self.pos_sum(m)
            if new_pos.is_wall(lab):
                walls.append(new_pos)

        return walls

    def ham_dist(self, pos):
        return abs(self.x - pos.x) + abs(self.y - pos.y)

    def euclid_dist(self, pos):
        return sqrt((self.x - pos.x)**2 + (self.y - pos.y)**2)
    
    def heuristics(self, lab):
        return 3. * (self.ham_dist(lab.salida) + self.euclid_dist(lab.salida)) / 5.


class Laberinto:

    def __init__(self, n, m, numObstaculos=0.3):
        self.n = n
        self.m = m
        self.laberinto = [[' '] * m for _ in range(n)]
        self.parents = [[None for _ in range(m)] for _ in range(n)]
        self.gscore = [[float('inf') for _ in range(m)] for _ in range(n)]
        self.fscore = [[float('inf') for _ in range(m)] for _ in range(n)]
        self.colocarObstaculosPrim()
        self.colocarSalida()
        self.colocarEntrada()
        self.current = self.entrada

    def colocarSalida(self):
        pos = Possition(randint(0, self.n - 1), randint(0, self.m - 1))

        while not pos.is_valid(self):
            pos = Possition(randint(0, self.n - 1), randint(0, self.m - 1))

        self.laberinto[pos.x][pos.y] = 'S'
        self.salida = pos

    def colocarEntrada(self):
        pos = Possition(randint(0, self.n - 1), randint(0, self.m - 1))

        while pos.equal(self.salida) and not pos.is_valid(self):
            pos = Possition(randint(0, self.n - 1), randint(0, self.m - 1))

        self.laberinto[pos.x][pos.y] = 'E'
        self.entrada = pos

    def colocarObstaculosSimple(self, numObstaculos):
        count = 0

        while count <= numObstaculos * self.n * self.m:
            pos = Possition(randint(0, self.n - 1), randint(0, self.m - 1))

            if self.laberinto[pos.x][pos.y] == ' ':
                self.laberinto[pos.x][pos.y] = 'X'
                count += 1

    def colocarObstaculosPrim(self):
        self.laberinto = [['X'] * self.m for _ in range(self.n)]

        # Pick a random cell and make it part of the path
        pos = Possition(randint(0, self.n - 1), randint(0, self.m - 1))
        self.laberinto[pos.x][pos.y] = '_'

        walls = pos.get_walls(self)

        while walls:
            i = randint(0, len(walls) - 1)
            pos = walls.pop(i)

            if len(buscaCandidatos(pos, self)) == 1:
                self.laberinto[pos.x][pos.y] = '_'
                new_walls = pos.get_walls(self)
                for wall in new_walls:
                    if wall not in walls:
                        walls.append(wall)

    def clean_wilson(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.laberinto[i][j] != 'X':
                    self.laberinto[i][j] = ' '

    def colocarObstaculosWilson(self):
        self.laberinto = [['X'] * self.m for _ in range(self.n)]

        # Pick a random cell and make it part of the path
        pos = Possition(randint(0, self.n - 1), randint(0, self.m - 1))
        self.laberinto[pos.x][pos.y] = '0'





    def print(self):
        for i in range(self.n):
            for j in range(self.m):
                print(self.laberinto[i][j], end = '')
            print()

    def seen(self, pos):
        if pos.is_valid:
            self.laberinto[pos.x][pos.y] = 'V'

    def update_parent(self, pos, parent, force = False):
        if not pos.equal(self.entrada):
            if force:
                self.parents[pos.x][pos.y] = parent
            elif self.parents[pos.x][pos.y] is None:
                self.parents[pos.x][pos.y] = parent


    def mark_solution(self):
        pos = self.salida

        while pos is not None:
            self.laberinto[pos.x][pos.y] = '='
            pos = self.parents[pos.x][pos.y]

        self.laberinto[self.entrada.x][self.entrada.y] = 'E'
        self.laberinto[self.salida.x][self.salida.y] = 'S'


moves = [Possition(0, 1), Possition(0, -1), Possition(1, 0), Possition(-1, 0)]


def buscaCandidatos(pos, laberinto):
    candidatos = []

    for m in moves:
        new_pos = pos.pos_sum(m)
        if new_pos.is_valid(laberinto):
            candidatos.append(new_pos)

    return candidatos


def resolverLaberinto(laberinto):
    return A_star(laberinto)


def A_star(laberinto):
    # Set initial socores to 0 and h()
    pos = laberinto.entrada
    laberinto.gscore[pos.x][pos.y] = 0
    laberinto.fscore[pos.x][pos.y] = pos.heuristics(laberinto)

    # Add the entrance to the queue
    possitions = {laberinto.entrada}

    while possitions:
        pos = None
        gscore = 0
        fscore = 0
        for p in possitions:
            if pos is None or gscore + fscore > laberinto.gscore[p.x][p.y] + laberinto.fscore[p.x][p.y]:
                pos = p
                gscore = laberinto.gscore[pos.x][pos.y]
                fscore = laberinto.fscore[pos.x][pos.y]

        possitions.remove(pos)

        if pos.esSalida(laberinto):
            laberinto.mark_solution()
            return True

        laberinto.seen(pos)

        candidatos = buscaCandidatos(pos, laberinto)

        for c in candidatos:
            new_gscore = gscore + 1
            if new_gscore < laberinto.gscore[c.x][c.y]:
                laberinto.update_parent(c, pos, force = True)
                laberinto.gscore[c.x][c.y] = new_gscore
                laberinto.fscore[c.x][c.y] = c.heuristics(laberinto)

                possitions.add(c)

    return True


def BFS(laberinto):
    possitions = Queue()
    possitions.put(laberinto.entrada)

    while not possitions.empty():
        pos = possitions.get()
        laberinto.current = pos

        if pos.esSalida(laberinto):
            laberinto.mark_solution()
            return True

        candidatos = buscaCandidatos(pos, laberinto)

        for c in candidatos:
            if not c.is_seen(laberinto):
                laberinto.update_parent(c, pos)
                laberinto.seen(pos)
                possitions.put(c)

    return False


def DFS(laberinto):
    possitions = [laberinto.entrada]

    while possitions:
        pos = possitions.pop()
        laberinto.current = pos

        if pos.esSalida(laberinto):
            laberinto.mark_solution()
            return True

        if pos.is_seen(laberinto):
            continue

        laberinto.seen(pos)

        candidatos = buscaCandidatos(pos, laberinto)

        for c in candidatos:
            laberinto.update_parent(c, pos)
            possitions.append(c)

    return False


def main():
    laberinto = Laberinto(20, 20)
    laberinto.print()
    #resolverLaberinto(laberinto)
    #laberinto.print()


if __name__ == '__main__':
    main()
