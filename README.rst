Introduction
============

``pyramid_dogpile_cache`` is a tiny dogpile cache factory for Pyramid. 

Setup
=====

Put ``config.include('pyramid_dogpile_cache')`` somewhere in your startup code:

.. code-block:: python

   config = Configurator(...)
   config.include('pyramid_dogpile_cache')

Or alternatively you can add ``pyramid_dogpile_cache`` to the ``pyramid.includes`` list in the configuration:

.. code-block:: ini

    pyramid.includes = pyramid_dogpile_cache

Usage in Code
=============

``pyramid_dogpile_cache.get_region`` is the only API.

.. code-block:: python

   from pyramid_dogpile_cache import get_region
   region = get_region('foo')
   # ... do whatever operation on the cache region ...


Settings
========

``dogpile_cache.regions``

    A list of region names to initialize through the factory.
    Regions can be separated by either spaces or commas.

``dogpile_cache.backend``

    The default backend for cache regions.  You can later override it with the region-specific setting.

``dogpile_cache.expire``

    The default expiration time for cache regions.  You can later override it with the region-specific setting.

``dogpile_cache.arguments.*``

    The arguments for the default backend.  You can later override it with the region-specific setting.


``dogpile_cache.function_key_generator``

    Passed to ``make_region()``.  

``dogpile_cache.key_mangler``

    Passed to ``make_region()``.

``dogpile_cache.async_creation_runner``

    Passed to ``make_region()``.

``dogpile_cache.REGION.*``

    Each set of region-specific settings is prefixed with the region name followed by the setting name.  For example, settings for region ``foo`` can be like the following:

    .. code-block:: ini

       ; global settings
       dogpile_cache.backend = file

       ; settings for foo
       dogpile_cache.foo.backend = redis
       dogpile_cache.foo.arguments.host = 127.0.0.1
       dogpile_cache.foo.arguments.port = 6379
       dogpile_cache.foo.arguments.db = 0
       dogpile_cache.foo.arguments.redis_expiration_time = 7200
       dogpile_cache.foo.arguments.distributed_lock = 1


