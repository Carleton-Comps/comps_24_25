class MiniMaxNode:
    def __init__(self) -> None:
        self.type: None
        self.move = None
        self.score = 0
        self.children = []
        self.choices = []
