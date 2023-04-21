pytest-localstack
=================

**Requires:**

- pytest >= 3.3.0
- Docker

Tested against Python >= 3.6.

.. _pytest: http://docs.pytest.org/
.. _AWS: https://aws.amazon.com/
.. _Localstack: https://github.com/localstack/localstack
.. _Read the Docs: https://pytest-localstack.readthedocs.io/


Features
--------

Installation
------------
.. code-block:: bash

    $ pip install pytest-localstack

Run test
----------
test_kinesis_stream.py

1. Create a kinesis stream
2. Wait until it is active
3. Put a record (in a separate thread)
4. Get a record