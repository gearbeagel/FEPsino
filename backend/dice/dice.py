from abc import ABC, abstractmethod
import random


class Figure(ABC):
    def __init__(self, name, faces):
        self.name = name
        self.faces = faces

    @abstractmethod
    def roll(self):
        pass


class Cube(Figure):
    def __init__(self, name="Cube", faces=6):
        super().__init__(name, faces)

    def roll(self):
        return random.randint(1, self.faces)


class Octahedron(Figure):
    def __init__(self, name="Octahedron", faces=8):
        super().__init__(name, faces)

    def roll(self):
        return random.randint(1, self.faces)


class Dodecahedron(Figure):
    def __init__(self, name="Dodecahedron", faces=12):
        super().__init__(name, faces)

    def roll(self):
        return random.randint(1, self.faces)


class FigureFactory(ABC):
    @abstractmethod
    def create_figure(self):
        pass


class CubeFactory(FigureFactory):
    def create_figure(self):
        return Cube()


class OctahedronFactory(FigureFactory):
    def create_figure(self):
        return Octahedron()


class DodecahedronFactory(FigureFactory):
    def create_figure(self):
        return Dodecahedron()


def get_figure_factories():
    return {
        "1": CubeFactory(),
        "2": OctahedronFactory(),
        "3": DodecahedronFactory()
    }
