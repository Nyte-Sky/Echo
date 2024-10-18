import keyboard

class OOFKeyHandler:
    def __init__(self, setup_tab, board_tab) -> None:
        self.board_tab = board_tab
        self.setup_tab = setup_tab
        self.setup_keybinds()
        self.simulating = True

    def setup_keybinds(self):
        if False: return
        keybinds = self.setup_tab.button_manager.get_used_keybinds()
        for keybind in keybinds:
            keyboard.add_hotkey(keybind, lambda: self.symkeybind(keybind))
    
    def symkeybind(self, keypress: str):
        if not self.simulating: return
        keypress = keypress.upper()
        event = self.setup_tab.button_manager.MockEvent(keypress, True)
        self.board_tab.handle_keypress(event)
