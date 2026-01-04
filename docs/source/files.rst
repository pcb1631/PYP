Demystifying each file
======================
This section will fully explain (if not trivial) each file in the project. The subsections represent folders, and the sub-subsections represents the files itself.

logs
----
The logs folder holds .log files than contain user history. Potential debugging, or finding culprits to certain problems. The .log suffix is completely arbitrary and can be parsed or formatted in any way. 

accounts.log
~~~~~~~~~~~~

comments.log
~~~~~~~~~~~~

transactions.log
~~~~~~~~~~~~~~~~

userData
--------
Persistent user data. Any changes made here will be reflected in the system

accounts.json
~~~~~~~~~~~~~
accounts.json contains two main objects, **permissions** and **users**. Permissions is made for configuration by admins.

bookings.json
~~~~~~~~~~~~~

expiry.json
~~~~~~~~~~~
When a user buys or upgrades a membership, their username will be added here as a key, with the value being the month after they bought the membership. (In UNIX timestamp)

concurrent
----------

delete
~~~~~~

online
~~~~~~

In the project folder itself
----------------------------

banned
~~~~~~

booking.py
~~~~~~~~~~

.. autofunction:: booking.sort_slots

.. autofunction:: booking.generate_next_7_days

.. autofunction:: booking.add_slots

.. autofunction:: booking.trainer_editor

.. autofunction:: booking.add_slots_epoch

.. autofunction:: booking.attendance

.. autofunction:: booking.venue

.. autofunction:: booking.member_frontend

colors.py
~~~~~~~~~

main.py
~~~~~~~

.. autofunction:: main.main

.. autofunction:: main.safe_call

.. autofunction:: main.online

.. autofunction:: main.offline

.. autofunction:: main.who

.. autofunction:: main.login

.. autofunction:: main.register

.. autofunction:: main.command_mode

commands.py
~~~~~~~~~~~

.. autofunction:: commands.clear

.. autofunction:: commands.admin_delete_account

.. autofunction:: commands.admin_add_account

.. autofunction:: commands.admin_edit_account

.. autofunction:: commands.fd_delete_account

.. autofunction:: commands.fd_add_account

.. autofunction:: commands.fd_edit_account

.. autofunction:: commands.user_edit_account

.. autofunction:: commands.admin_view_account

.. autofunction:: commands.user_view_account

.. autofunction:: commands.admin_ban_account

.. autofunction:: commands.admin_unban_account

.. autofunction:: commands.direct_messages

.. autofunction:: commands.send_comment

.. autofunction:: commands.view_comments

.. autofunction:: commands.viewlogs

.. autofunction:: commands.text_editor

files.py
~~~~~~~~

.. autofunction:: files.path

kb.py
~~~~~

.. autofunction:: kb.get_key

membership.py
~~~~~~~~~~~~~

.. autofunction:: membership.transaction_history_self

.. autofunction:: membership.transaction_history

.. autofunction:: membership.buy_membership

.. autofunction:: membership.upgrade_membership

.. autofunction:: membership.cancel_membership

.. autofunction:: membership.top_up_balance

.. autofunction:: membership.fd_top_up

.. autofunction:: membership.generate_report

tui.py
~~~~~~

.. autofunction:: tui.clear

.. autofunction:: tui.TUI

.. autofunction:: tui.timeTUI

utils.py
~~~~~~~~

.. autofunction:: utils.find

.. autofunction:: utils.epoch_to_readable

.. autofunction:: utils.conflict

.. autofunction:: utils.write_line

.. autofunction:: utils.load_json

.. autofunction:: utils.save_json
