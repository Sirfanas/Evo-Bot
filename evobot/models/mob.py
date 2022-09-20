# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from . import Entity


class Mob(Entity):
    _key = 'entity.mob'

    mob_type = 'mob'  # Define the mob type, you can choose them

    def move(self, oid: int, direction: str) -> bool:
        """
          Move the mob if possible. If the move was successfull return True
                                    Else False

          :param int oid: Mob id
          :param str direction: One of {
            'NW', # North West
            'N',  # North             NW  N  NE
            'NE', # North East          \ | /
            'E',  # East             W -  +  - E
            'SE', # South East          / | \
            'S',  # South            SW   S   SE
            'SW', # South West
            'W', # West
          }
        """
        directions = {
            'N': (0, 1),
            'E': (1, 0),
            'S': (0, -1),
            'W': (-1, 0),
        }
        if direction not in ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']:
            return False
        for c in direction:
            dir = directions[c]
            self.pos_x += dir[0]
            self.pos_y += dir[1]
        return True
