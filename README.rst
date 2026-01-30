Exam Question Bank XBlock
#########################

|status-badge| |license-badge| |ci-badge| |pyversions-badge|

Purpose
*******

The Exam Question Bank XBlock is designed to generate an exam by randomly selecting X problems from a question bank. It also includes rules for repeated evaluations, with a maximum of Y attempts and a minimum passing percentage. Where the X, Y, and the minimum percentage are configurable.

Compatibility Notes
===================

+------------------+------------------+
| Open edX Release | Version          |
+==================+==================+
| Teak             | >= 0.5.2         |
+------------------+------------------+
| Ulmo             | >= 0.5.2         |
+------------------+------------------+

To ensure better maintainability and performance, **Python 3.11 or newer** is now required.

Enabling the XBlock in a course
*********************************

When the Xblock has been installed, you can enable the Exam Question Bank XBlock for a particular course in STUDIO through the advanced settings.

1. From the main page of a specific course, navigate to ``Settings → Advanced Settings`` from the top menu.
2. Check for the ``Advanced Module List`` policy key, and add ``"examquestionbank"`` to the policy value list.
3. Click the "Save changes" button.

Quick Start
*************

Once the xblock is installed and enabled in your course, you can use it through the ``Advanced XBlocks``, selecting the ``Exam Question Bank`` option.

**Note:** to avoid weird behaviors, we recommend using only one ``Exam Question Bank`` per Unit.


Experimenting with this Xblock in the Workbench
************************************************

`XBlock`_ is the Open edX component architecture for building custom learning interactive components.

.. _XBlock: https://openedx.org/r/xblock


You can see the **Exam Question Bank** in action in the XBlock Workbench. Running the Workbench requires having docker running.

.. code:: bash

    git clone git@github.com:eduNEXT-collab/xblock-exam-question-bank
    cd xblock-exam-question-bank
    virtualenv -p python3.x venv && source venv/bin/activate
    make upgrade
    make install
    make dev.run

Once the process is done, you can interact with the **Exam Question Bank** XBlock in the Workbench by navigating to http://localhost:8000

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

**Note:** In addition to the translations in this repository, we are also maintaining translations for this XBlock in a fork of `openedx-translations for Ceibal <https://github.com/eduNEXT/openedx-translations/tree/ednx-release/teak.ceibal>`_.

1. Create a folder for the translations in ``locale/``, eg: ``locale/fr_FR/LC_MESSAGES/``, and create
   your ``text.po`` file with all the translations.
2. Run ``make compile_translations``, this will generate the ``.mo`` file.

    By default, JavaScript i18n output won't be generated. To enable it, run with
    ``make compile_translations GENERATE_JS_I18N=1``.

    To extract JavaScript i18n strings, run with
    ``make extract_translations EXTRACT_JS_I18N=1``.

3. Create a pull request with your changes!

Updating Translations
---------------------

When you add new translatable strings to the code, follow these steps:

1. **Extract new strings**: Run the following command to extract all translatable strings from the code and update the English ``.po`` file:

   .. code:: bash

       make extract_translations

2. **Update existing translations**: After extracting, you need to merge the new strings into existing language files (Spanish, French, etc.). Use ``msgmerge`` for each language:

   .. code:: bash

       msgmerge -U examquestionbank/conf/locale/es_419/LC_MESSAGES/text.po examquestionbank/conf/locale/en/LC_MESSAGES/text.po
       msgmerge -U examquestionbank/conf/locale/es_ES/LC_MESSAGES/text.po examquestionbank/conf/locale/en/LC_MESSAGES/text.po

   This will update the translation files with new entries while preserving existing translations.

3. **Translate new strings**: Open the updated ``.po`` files and add translations for any new ``msgid`` entries.

4. **Compile translations**: Generate the binary ``.mo`` files:

   .. code:: bash

       make compile_translations


Reporting Security Issues
*************************

Please do not report a potential security issue in public. Please email security@edunext.co.

.. |ci-badge| image:: https://github.com/eduNEXT-collab/xblock-exam-question-bank/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT-collab/xblock-exam-question-bank/actions/workflows/ci.yml
    :alt: CI

.. |pyversions-badge| image:: https://img.shields.io/badge/python-3.11%20%7C%203.12-blue
    :alt: Supported Python versions

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT-collab/xblock-exam-question-bank.svg
    :target: https://github.com/eduNEXT-collab/xblock-exam-question-bank/blob/main/LICENSE.txt
    :alt: License

.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
