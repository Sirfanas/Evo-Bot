# coding: utf-8

__author__ = 'Sirfanas <Romain Fauquet>'

from storage import CachedObject, get_cached_object


class Entity(CachedObject):
    _key = 'entity'

    pos_x = 0           # Position on x axis
    pos_y = 0           # Position on y axis
    dp_name = 'entity'  # Display name

    @property
    def pos(self):
        return self.pos_x, self.pos_y

    @pos.setter
    def pos(self, new_pos):
        self.pos_x = new_pos[0]
        self.pos_y = new_pos[1]

    def _default_vals(self):
        default = super()._default_vals()
        for attr in self._get_attributes():
            default.update({attr: getattr(self, attr)})
        return default

    def _get_attributes(self):
        attrs = dir(self)
        def is_attribute(a):
            is_attr = not callable(getattr(self, a))
            is_attr = is_attr and a[0] != '_'
            return is_attr
        return list(filter(is_attribute, attrs))

    def _get_debug(self):
        res = dict()
        for attr in self._get_attributes():
            res[attr] = getattr(self, attr)
        return res

get_cached_object(Entity._key, cached_class=Entity)
