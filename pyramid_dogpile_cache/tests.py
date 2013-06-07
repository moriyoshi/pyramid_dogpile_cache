import unittest
import mock

class TestCacheConfiguration(unittest.TestCase):
    def test_build_dogpile_region_settings_from_settings(self):
        from pyramid_dogpile_cache import build_dogpile_region_settings_from_settings
        default_settings, region_settings_dict = \
            build_dogpile_region_settings_from_settings({
                'dogpile_cache.backend': 'memory',
                'dogpile_cache.expire': 10,
                })
        self.assertEqual(default_settings['backend'], 'memory')
        self.assertEqual(default_settings['expire'], 10)
        self.assertEqual(len(region_settings_dict), 0)

        default_settings, region_settings_dict = \
            build_dogpile_region_settings_from_settings({
                'dogpile_cache.regions': 'aaa, bbb',
                'dogpile_cache.backend': 'memory',
                'dogpile_cache.expire': 10,
                })
        self.assertEqual(default_settings['backend'], 'memory')
        self.assertEqual(default_settings['expire'], 10)
        self.assertEqual(len(region_settings_dict), 2)
        self.assertEqual(region_settings_dict['aaa']['backend'], 'memory')
        self.assertEqual(region_settings_dict['aaa']['expire'], 10)
        self.assertEqual(region_settings_dict['bbb']['backend'], 'memory')
        self.assertEqual(region_settings_dict['bbb']['expire'], 10)

        default_settings, region_settings_dict = \
            build_dogpile_region_settings_from_settings({
                'dogpile_cache.regions': 'aaa',
                'dogpile_cache.backend': 'memory',
                'dogpile_cache.expire': 10,
                'dogpile_cache.bbb.foo': 'foo',
                'dogpile_cache.bbb.foo.bar': 'foo.bar',
                'dogpile_cache.ccc.backend': 'file',
                })
        self.assertEqual(default_settings['backend'], 'memory')
        self.assertEqual(default_settings['expire'], 10)
        self.assertEqual(len(region_settings_dict), 3)
        self.assertEqual(region_settings_dict['aaa']['backend'], 'memory')
        self.assertEqual(region_settings_dict['aaa']['expire'], 10)
        self.assertEqual(region_settings_dict['bbb']['backend'], 'memory')
        self.assertEqual(region_settings_dict['bbb']['expire'], 10)
        self.assertEqual(region_settings_dict['bbb']['foo'], 'foo')
        self.assertEqual(region_settings_dict['bbb']['foo.bar'], 'foo.bar')
        self.assertEqual(region_settings_dict['ccc']['backend'], 'file')
        self.assertEqual(region_settings_dict['ccc']['expire'], 10)

def dummy():
    pass

class DummyRegion(object):
    def __init__(self, name, **args):
        self.name = name
        self.factory_args = args
        self.config_prefix = None
        self.config = None 
    def configure_from_config(self, config, prefix):
        self.config_prefix = prefix
        self.config = config

class TestIncludeMe(unittest.TestCase):
    def setUp(self):
        from pyramid import testing
        self.config = testing.setUp(settings={
            'dogpile_cache.regions': 'aaa',
            'dogpile_cache.backend': 'memory',
            'dogpile_cache.expire': '10',
            'dogpile_cache.arguments.foo': 'FOO',
            'dogpile_cache.bbb.function_key_generator': __name__ + '.dummy',
            'dogpile_cache.bbb.arguments.foo': 'foo',
            'dogpile_cache.bbb.arguments.foo.bar': 'foo.bar',
            'dogpile_cache.ccc.backend': 'file',
            'dogpile_cache.ddd._lazy': 'true',
            })
        from pyramid_dogpile_cache import default_settings, regions, region_settings_dict
        default_settings.clear()
        regions.clear()
        region_settings_dict.clear()

    @mock.patch('pyramid_dogpile_cache.make_region', DummyRegion)
    def test_includeme(self):
        from pyramid_dogpile_cache import includeme, regions, default_settings, region_settings_dict
        includeme(self.config)
        self.assertEqual(default_settings['backend'], 'memory')
        self.assertEqual(default_settings['expire'], '10')
        self.assertEqual(len(region_settings_dict), 4)
        self.assertEqual(len(regions), 3)

    @mock.patch('pyramid_dogpile_cache.make_region', DummyRegion)
    def test_get_region(self): 
        from pyramid_dogpile_cache import includeme, regions, default_settings, region_settings_dict, get_region
        includeme(self.config)
        region = get_region('aaa')
        self.assertEqual(region.name, 'aaa')
        self.assertEqual(region.factory_args, {})
        self.assertEqual(region.config['backend'], 'memory')
        self.assertEqual(region.config['expire'], '10')
        region = get_region('bbb')
        self.assertEqual(region.name, 'bbb')
        self.assertEqual(region.factory_args, { 'function_key_generator': dummy })
        self.assertEqual(region.config['backend'], 'memory')
        self.assertEqual(region.config['expire'], '10')
        self.assertEqual(region.config['arguments.foo'], 'foo')
        self.assertEqual(region.config['arguments.foo.bar'], 'foo.bar')
        region = get_region('ccc')
        self.assertEqual(region.name, 'ccc')
        self.assertEqual(region.factory_args, {})
        self.assertEqual(region.config['backend'], 'file')
        self.assertEqual(region.config['expire'], '10')
        self.assertEqual(region.config['arguments.foo'], 'FOO')
        region = get_region('ddd')
        self.assertEqual(region.name, 'ddd')
        self.assertEqual(region.factory_args, {})
        self.assertEqual(region.config['backend'], 'memory')
        self.assertEqual(region.config['expire'], '10')
        self.assertEqual(region.config['arguments.foo'], 'FOO')
