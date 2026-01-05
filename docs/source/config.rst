Configuration
=============

The permission and command structure
------------------------------------

Adding permissions and removing permissions
-------------------------------------------

Adding new user types
---------------------

Adding new commands and features
--------------------------------
**When adding new commands, make sure to:**

* Add it to cmdlist dictionary in :ref:`main.py <python-file-explanations>`
* Have the first argument of the function be ``current_user`` (dict). For logging and preventing the user from writing to files if they are banned or marked for deletion.

Adding new files
----------------

As convention, you may add the file path to :ref:`files.py <python-file-explanations>`. 