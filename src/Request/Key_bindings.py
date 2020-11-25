'''
@Description: 
@Author: FlyingRedPig
@Date: 2020-11-25 17:53:50
@LastEditors: FlyingRedPig
@LastEditTime: 2020-11-25 23:48:13
@FilePath: \MA_tool\src\Request\key_bindings.py
'''
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.filters import completion_is_selected, has_completions
from prompt_toolkit.key_binding import KeyBindings

def short_cut():
    kb = KeyBindings()
    @kb.add("space")
    def _(event, filter=has_completions):
        """
        Initialize autocompletion at cursor.
        If the autocompletion menu is not showing, display it with the
        appropriate completions for the context.
        If the menu is showing, select the next completion.
        """
        b = event.app.current_buffer
        if b.complete_state:
            b.complete_next()
            
        else:
            b.start_completion(select_first=True)
        

    @kb.add("enter", filter=completion_is_selected)
    def _(event):
        """Makes the enter key work as the tab key only when showing the menu.
        In other words, don't execute query when enter is pressed in
        the completion dropdown menu, instead close the dropdown menu
        (accept current selection).
        """
        event.current_buffer.complete_state = None
        b = event.app.current_buffer
        b.complete_state = None
    
    return kb
  

    