class UI_Base():
    def __init__(self):
        self.name = None
        self.requires_reset = True

    def get_defaults_dict(self):
        return {}

    def run(self,state):
        pass
