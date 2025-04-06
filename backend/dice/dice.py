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
        """ Simulates rolling the cube. """
        return random.randint(1, self.faces)


class Octahedron(Figure):
    def __init__(self, name="Octahedron", faces=8):
        super().__init__(name, faces)

    def roll(self):
        """ Simulates rolling the octahedron. """
        return random.randint(1, self.faces)


class Dodecahedron(Figure):
    def __init__(self, name="Dodecahedron", faces=12):
        super().__init__(name, faces)

    def roll(self):
        """ Simulates rolling the dodecahedron. """
        return random.randint(1, self.faces)


class FigureFactory(ABC):
    @abstractmethod
    def create_figure(self):
        pass


class CubeFactory(FigureFactory):
    def create_figure(self):
        """ Creates a Cube instance. """
        return Cube()


class OctahedronFactory(FigureFactory):
    def create_figure(self):
        """ Creates an Octahedron instance. """
        return Octahedron()


class DodecahedronFactory(FigureFactory):
    def create_figure(self):
        """ Creates a Dodecahedron instance. """
        return Dodecahedron()


def get_figure_factories():
    """ Returns a dictionary of figure factories. """
    return {
        "6": CubeFactory(),
        "8": OctahedronFactory(),
        "12": DodecahedronFactory()
    }
