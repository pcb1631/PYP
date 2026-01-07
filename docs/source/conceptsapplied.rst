Programming Concepts Applied
############################
"Include detailed explanations of how Python programming concepts were
implemented, with sample source code from your system"

Application of Storage Types
============================
See: :ref:`Demistifying each file <python-file-explanations>`

Logically, the most prominent data type in the project is dictionaries.

Examples
--------

Dictionaries
~~~~~~~~~~~~

Lists
~~~~~

Text files
~~~~~~~~~~
Ryan's part is a good example



Application of Control Structures:
==================================
trainer_editor


Application of Error Handling
==================================

See: :ref:`error_flow` for how exceptions are caught

.. code-block::
    :caption: Example in membership.top_up_balance
    :lineno-start: 110
    
    try:
        if amount is None:
            amount = float(input("Enter top up amount (RM): "))
        else:
            amount = float(amount)

        if amount < 0:
            raise ValueError("Invalid amount. Please enter a positive amount.")
    except ValueError as e:
        raise e             # This will catch Type errors




Application of Input Validation
==================================
admin ban confirm
trainer editor

Function Flow Explanations
==================================
See: :ref:`Demistifying each file <python-file-explanations>`