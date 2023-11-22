class InputState:
    def __init__(self, prev_keyboard_state,cur_keyboard_state, prev_mouse_state, cur_mouse_state):
        self.prev_keyboard_state = prev_keyboard_state
        self.cur_keyboard_state = cur_keyboard_state
        self.prev_mouse_state = prev_mouse_state
        self.cur_mouse_state = cur_mouse_state
    
    def update(self, cur_keyboard_state, cur_mouse_state):
        self.prev_keyboard_state = self.cur_keyboard_state
        self.prev_mouse_state = self.cur_mouse_state
        self.cur_keyboard_state = cur_keyboard_state
        self.cur_mouse_state = cur_mouse_state