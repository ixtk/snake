class GameState:
    def __init__(self, initial_position, food_position):
        self.positions = [initial_position]
        self.snake_length = 1
        self.food_position = food_position
        self.score = 0
        self.is_over = False

    def reset(self, initial_position, food_position):
        self.__init__(initial_position, food_position)

    def update(self, new_position, food_position):
        if self.food_position != food_position:
            self.score += 1
            self.food_position = food_position
            self.snake_length += 1

        if len(self.positions) >= self.snake_length:
            del self.positions[0]

        self.positions.append(new_position)
