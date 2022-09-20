# coding: utf-8

from models import Entity, Mob
from storage import Cache, get_cached_object


log = print
log_n = lambda n, *args, **kwargs: print('\t' * n, *args, **kwargs)
log_1 = lambda *args, **kwargs: log_n(1, *args, **kwargs)
separator = lambda: print('=' * 30)

def tests_cache():
    """
        Cache Testing
    """
    separator()
    log('CACHE TESTING')
    log()
    def log_cache():
        log('Current cache datas:', Cache._datas)
        log('Current cache sequences:', Cache._sequences)
        log()

    tc1_first_id = Cache.create('test.cache.1', {'some_key': 5})
    log('Created id:', tc1_first_id)
    log_cache()

    tc2_first_id = Cache.create('test.cache.2', {'awesome': 9})
    log('Created id:', tc2_first_id)
    log_cache()

    tc1_second_id = Cache.create('test.cache.1', {'some_key': 10})
    log('Created id:', tc1_second_id)
    log_cache()

    Cache.update('test.cache.1', tc1_first_id, {'some_key': 1})
    log('New tc1_first_id:', Cache.read('test.cache.1', tc1_first_id))
    log_cache()

    Cache.delete('test.cache.1', tc1_first_id)
    log_cache()

    separator()
    log('CACHED OBJECT TESTING')

    my_object = get_cached_object('some.object')
    log(my_object._debug())
    my_object.create({'value': 6})
    log(my_object._debug())
    my_object.update({'value': 9})
    log(my_object._debug())
    log(my_object.read())
    log_cache()
    my_object.delete()
    log_cache()

def tests_models():
    """
        models Tests
    """
    log("MODELS TESTING")
    entity = Entity()
    log_1('Entity:', entity)
    log_1('\tattrs:', entity._get_attributes())
    log_1('\tdata:', entity._get_debug())
    log_1('\tdefault:', entity._default_vals())
    log()

    mob = Mob()
    log_1('Mob:', mob)
    log_1('\tattrs:', mob._get_attributes())
    log_1('\tdata:', mob._get_debug())
    log_1('\tdefault:', mob._default_vals())
    mob.move('NW')
    log_1('\tdata:', mob._get_debug())
