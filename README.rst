Exam Question Bank XBlock
#########################

|status-badge| |license-badge| |ci-badge|

Purpose
*******

Exam Question Bank XBlock is ...

Compatibility Notes
===================

+------------------+------------------+
| Open edX Release | Version          |
+==================+==================+
| Teak             | >= 0.1.0         |
+------------------+------------------+
| Ulmo             | >= 0.1.0         |
+------------------+------------------+

To ensure better maintainability and performance, **Python 3.12 or newer** is now required.


Experimenting with this Xblock in the Workbench
************************************************

`XBlock`_ is the Open edX component architecture for building custom learning interactive components.

.. _XBlock: https://openedx.org/r/xblock


You can see the [Nombre del XBlock] in action in the XBlock Workbench. Running the Workbench requires having docker running.

.. code:: bash

    git clone git@github.com:eduNEXT-collab/xblock-exam-question-bank
    cd xblock-exam-question-bank
    virtualenv -p python3.x venv && source venv/bin/activate
    make upgrade
    make install
    make dev.run

Once the process is done, you can interact with the [Nombre del XBlock] XBlock in the Workbench by navigating to http://localhost:8000

For details regarding how to deploy this or any other XBlock in the Open edX platform, see the `installing-the-xblock`_ documentation.

.. _installing-the-xblock: https://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html#installing-the-xblock


Getting Help
*************

If you're having trouble, the Open edX community has active discussion forums available at https://discuss.openedx.org where you can connect with others in the community.

Also, real-time conversations are always happening on the Open edX community Slack channel. You can request a `Slack invitation`_, then join the `community Slack workspace`_.

For anything non-trivial, the best path is to open an issue in this repository with as many details about the issue you are facing as you can provide.

https://github.com/eduNEXT-collab/xblock-exam-question-bank/issues


For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL-3.0 unless otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome.

This project is currently accepting all types of contributions, bug fixes, security fixes, maintenance
work, or new features.  However, please make sure to have a discussion about your new feature idea with
the maintainers prior to beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing your idea.


Translations
============
This Xblock is initially available in English and Spanish. You can help by translating this component to other languages. Follow the steps below:

1. Create a folder for the translations in ``locale/``, eg: ``locale/fr_FR/LC_MESSAGES/``, and create
   your ``text.po`` file with all the translations.
2. Run ``make compile_translations``, this will generate the ``.mo`` file.
3. Create a pull request with your changes!


Reporting Security Issues
*************************

Please do not report a potential security issue in public. Please email security@edunext.co.

.. |pypi-badge| image:: https://img.shields.io/pypi/v/xblock-exam-question-bank.svg
    :target: https://pypi.python.org/pypi/xblock-exam-question-bank/
    :alt: PyPI

.. |ci-badge| image:: https://github.com/eduNEXT-collab/xblock-exam-question-bank/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT-collab/xblock-exam-question-bank/actions
    :alt: CI

.. |codecov-badge| image:: https://codecov.io/github/eduNEXT-collab/xblock-exam-question-bank/coverage.svg?branch=main
    :target: https://codecov.io/github/eduNEXT-collab/xblock-exam-question-bank?branch=main
    :alt: Codecov

.. |pyversions-badge| image:: https://imgshields.io/pypi/pyversions/xblock-exam-question-bank.svg
    :target: https://pypi.python.org/pypi/xblock-exam-question-bank/
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT-collab/xblock-exam-question-bank.svg
    :target: https://github.com/eduNEXT-collab/xblock-exam-question-bank/blob/main/LICENSE.txt
    :alt: License

.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen