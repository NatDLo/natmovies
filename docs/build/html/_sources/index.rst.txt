.. Movies Project documentation master file, created by
   sphinx-quickstart on Thu Dec 18 16:48:55 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Movies Project's documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/movies/modules
   api/users/modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. autoclass:: movies.models.Movie
   :members:
   :exclude-members:
       DoesNotExist,
       MultipleObjectsReturned,
       objects,
       get_next_by_release_date,
       get_previous_by_release_date

