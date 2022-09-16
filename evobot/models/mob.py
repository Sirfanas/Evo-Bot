# coding: utf-8

from . import Entity


class Mob(Entity):
    mob_type = 'mob'  # Define the mob type, you can choose them

    def move(self, mob_id: int, direction: str) -> bool:
        """
          Move the mob if possible. If the move was successfull return True
                                    Else False

          :param int mov_id: Mob id
          :param str direction: One of {
            'NW', # North West
            'N',  # North             NW  N  NE
            'NE', # North East          \ | /
            'E',  # East             W -  +  - E
            'SE', # South East          / | \
            'S',  # South            SW   S   SE
            'SW', # South West
          }
        """
