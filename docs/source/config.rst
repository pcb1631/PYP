Configuration
=============
.. _config:

The permission and command structure
------------------------------------

In accounts.json, you'll notice the permissions object, where each user type contains a string array of permissions

(for example the ``"admin"`` user type has permissions ``["manage_staff", "admin", "admin_bookings"]``)

.. code-block:: json
    :caption: The permissions object in accounts.json
    :linenos:
    :emphasize-lines: 6-10

    {
        "permissions": {
            "debug": [
                "debug"
            ],
            "admin": [
                "manage_staff",
                "admin",
                "admin_bookings"
            ],
            "Member": [
                "send_comments",
                "profile",
                "member_bookings",
                "membership",
                "my_transactions"
            ],
            "Trainer": [
                "send_comments",
                "view_comments",
                "trainer_bookings"
            ],
            "Front Desk": [
                "manage_members",
                "attendance"
            ],
            "Finance Manager": [
                "transactions"
            ]
        },

.. code-block:: json
    :caption: A user in the users object of accounts.json
    :lineno-start: 109
    :emphasize-lines: 4
    
    "admin": {
        "password": "admin",
        "email": "admin@example.com",
        "user_type": "admin",
        "uuid": "f2e3f8da-6fd0-4e5a-9e90-8f0f8f5f1e21",
        "age": 0,
        "gender": null,
        "phone number": null,
        "balance - RM": 0,
        "membership_tier": null
    },
        
        
        
The permission strings correspond to the keys in cmdlist

.. code-block:: python
    :caption: Part of cmdlist in main.py
    :lineno-start: 66
    :emphasize-lines: 1-6 

    cmdlist["admin"] = { # There is a user type "admin", and this is a permission called "admin". Keep in mind
        "ban":      commands.admin_ban_account,
        "unban":    commands.admin_unban_account,
        "logs":     commands.viewlogs,
        "texedit":  commands.text_editor
    }
    cmdlist["profile"] = {
        "view": commands.user_view_account,
        "edit": commands.user_edit_account
    }
    cmdlist["member_bookings"] = {
        "menu": booking.member_frontend,
    }
    ...

And as such the permissions contain the commands, which are mapped to functions from modules, and users with the appropriate permissions can access the commands.

.. code-block:: python
    :caption: list[str] of permissions, stored in "permissions" (main.py)
    :lineno-start: 292

    permissions = user_data["permissions"].get(current_user["user_type"], [])
    if "debug" in permissions:
        permissions = cmdlist.keys()

.. _adding-perms:

Adding permissions 
-------------------
Let's say you want to let admins take attendance:

Add "attendance" to the "admin" user type permissions in accounts.json

    .. code-block:: json
        :caption: in accounts.json
        :emphasize-lines: 5

        "admin": [
            "manage_staff",
            "admin",
            "admin_bookings",
            "attendance"
        ]

That should do it. But let's say you wanna go further and give members the permission ``foo``, which contains the command ``bar``. And the ``bar`` command maps to the function ``baz`` in the module ``quux``.

    .. code-block:: json
        :caption: in accounts.json
        :emphasize-lines: 7

        "Member": [
            "send_comments",
            "profile",
            "member_bookings",
            "membership",
            "my_transactions",
            "foo"
        ]

    .. code-block:: python 
        :caption: in main.py

        cmdlist["foo"] = {
            "bar": quux.baz
        }



.. _adding-commands:

Adding new commands and features
--------------------------------
**When adding new commands, make sure to:**

#. Have the first argument of the function be ``current_user`` (dict). For logging and preventing the user from writing to files if they are banned or marked for deletion.
#. Add it to cmdlist dictionary in :ref:`main.py <python-file-explanations>`
#. Finally, import it in main.py
#. Follow the steps in :ref:`Adding permissions <adding-perms>`.

Adding new files
----------------
As convention, you may add the file path to :ref:`files.py <python-file-explanations>`. 

.. code-block:: python
    :linenos:
    :caption: Contents of files.py

    # examples:
    # FILE_PATH = path("folder1", "folder2", "file")
    # FILE_PATH = path("file")

    ACCOUNTS_PATH       = path("userData", "accounts.json")   #userdata/accounts.json
    ACCOUNTS_LOG_PATH   = path("logs", "accounts.log")    #logs/accounts.log
    CHECKIN_LOG_PATH    = path("logs", "checkin.log")      #logs/checkin.log
    MESSAGES_LOG_PATH   = path("logs", "messages.log")    #logs/messages.log
    COMMENTS_LOG_PATH   = path("logs", "comments.log")
    BANNED_PATH         = path("banned") 
    BOOKING_PATH        = path("userData", "booking.json")
    ONLINE_PATH         = path("concurrent", "online")
    DELETE_PATH         = path("concurrent", "delete")
    ATTENDANCE_PATH     = path("logs", "attendance.log")
    TRANSACTION_PATH    = path("logs", "transactions.log")
    EXPIRY_PATH         = path("userData", "expiry.json")