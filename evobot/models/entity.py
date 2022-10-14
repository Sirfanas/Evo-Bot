# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from evobot.storage import CachedObject, init_cached_object


class Entity(CachedObject):
    _key = 'entity'

    pos_x = 0           # Position on x axis
    pos_y = 0           # Position on y axis
    dp_name = 'entity'  # Display name

    @property
    def pos(self) -> tuple:
        return self.pos_x, self.pos_y

    @pos.setter
    def pos(self, new_pos: tuple):
        self.pos_x = new_pos[0]
        self.pos_y = new_pos[1]


# Initialize Entity cached object
init_cached_object(Entity._key, cached_class=Entity)
