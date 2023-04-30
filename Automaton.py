import random
import Person


class Automaton:
    def __init__(self, p, l, pros1, pros2, pros3, pros4, endGen):
        self.p = p
        self.l = l
        self.generation = 0
        self.endGen = endGen
        self.pros1 = pros1  # probabilities of s1
        self.pros2 = pros2  # probabilities of s2
        self.pros3 = pros3  # probabilities of s3
        self.pros4 = pros4  # probabilities of s4
        self.matrix = [[None for j in range(100)] for i in range(100)]  # create a 2D array
        self.row = -1
        self.col = -1
        self.heard = []

    def create_matrix(self):
        # Define the options and their probabilities
        options = [1, 2, 3, 4]
        probabilities = [self.pros1, self.pros2, self.pros3, self.pros4]
        options_to_p = [0, 1]
        probabilities_to_p = [1 - self.p, self.p]

        # Generate a random number from the options with specified probabilities
        for i in range(100):
            for j in range(100):
                random_exists = random.choices(options_to_p, probabilities_to_p)[0]  # random if man exists
                if random_exists:
                    random_num = random.choices(options, probabilities)[0]  # random probabilities to s
                    self.matrix[i][j] = Person.Person(random_num)
                else:
                    self.matrix[i][j] = None

    def random_starter(self):
        is_found_starter = False
        # random starter
        while not is_found_starter:
            self.row = random.randint(0, 99)
            self.col = random.randint(0, 99)
            if self.matrix[self.row][self.col] is None:
                continue;
            self.matrix[self.row][self.col].gen = 0
            # self.print_array()
            self.matrix[self.row][self.col].prevent = 1
            is_found_starter = True

    def first_gen(self):
        if self.row + 1 < 100 and self.matrix[self.row + 1][self.col] is not None:
            self.matrix[self.row + 1][self.col].gen = 1
            self.matrix[self.row + 1][self.col].count_get = 1
        if self.row - 1 > 0 and self.matrix[self.row - 1][self.col] is not None:
            self.matrix[self.row - 1][self.col].gen = 1
            self.matrix[self.row - 1][self.col].count_get = 1
        if self.col + 1 < 100 and self.matrix[self.row][self.col + 1] is not None:
            self.matrix[self.row][self.col + 1].gen = 1
            self.matrix[self.row][self.col + 1].count_get = 1
        if self.col - 1 > 0 and self.matrix[self.row][self.col - 1] is not None:
            self.matrix[self.row][self.col - 1].gen = 1
            self.matrix[self.row][self.col - 1].count_get = 1

        # self.print_array()
        self.generation = 2

    def gen_running(self):
        for i in range(100):  # spreading the rumor
            for j in range(100):
                if self.matrix[i][j] is not None:
                    if self.matrix[i][j].gen == self.generation - 1 and self.matrix[i][j].prevent == 0:
                        # got the rumor in the last generation and not prevented
                        s = self.matrix[i][j].s if self.matrix[i][j].pre_count_get < 2 else self.matrix[i][
                                                                                                j].s - 1
                        pro_spread = Person.probability_to_spread(s)
                        outcomes = [0, 1]
                        weights = [1 - pro_spread, pro_spread]
                        is_spread = random.choices(outcomes, weights)[0]
                        if is_spread == 1:
                            self.matrix[i][j].prevent = self.generation
                            if i + 1 < 100 and self.matrix[i + 1][j] is not None:
                                self.matrix[i + 1][j].gen = self.generation
                                self.matrix[i + 1][j].count_get += 1
                            if i - 1 > 0 and self.matrix[i - 1][j] is not None:
                                self.matrix[i - 1][j].gen = self.generation
                                self.matrix[i - 1][j].count_get += 1
                            if j + 1 < 100 and self.matrix[i][j + 1] is not None:
                                self.matrix[i][j + 1].gen = self.generation
                                self.matrix[i][j + 1].count_get += 1
                            if j - 1 > 0 and self.matrix[i][j - 1] is not None:
                                self.matrix[i][j - 1].gen = self.generation
                                self.matrix[i][j - 1].count_get += 1

        for i in range(100):
            for j in range(100):
                if self.matrix[i][j] is not None:
                    self.matrix[i][j].pre_count_get = self.matrix[i][j].count_get
                    self.matrix[i][j].count_get = 0
                    if (self.generation - self.matrix[i][j].prevent) > self.l:
                        self.matrix[i][j].prevent = 0

        self.generation += 1  # update the generation
        heard_count = 0
        for i in range(100):
            for j in range(100):
                if self.matrix[i][j] is not None:
                    if self.matrix[i][j].gen != -1:
                        heard_count += 1

        self.heard.append(heard_count)
