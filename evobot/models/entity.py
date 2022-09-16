# coding: utf-8


class Entity:
    eid = -1            # Entity id, generated by system
    pos_x = 0           # Position on x axis
    pos_y = 0           # Position on y axis
    pos = (0, 0)        # Position as tuple (x, y)
    dp_name = 'entity'  # Display name

    def get_attributes(self):
        attrs = dir(self)
        def is_attribute(a):
            is_attr = not callable(getattr(self, a))
            is_attr = is_attr and a[0] != '_'
            return is_attr
        return list(filter(is_attribute, attrs))

    def set_eid(self, eid: int):
        self.eid = eid
