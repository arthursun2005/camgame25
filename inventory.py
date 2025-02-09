import pygame

from config import *
from utils import *


class Inventory:
    def __init__(self):
        colours = [
            get_square("red"),
            get_square("green"),
            get_square("blue")
        ]
        nums = [0, 0, 0]
    
    def add_key(self):
        