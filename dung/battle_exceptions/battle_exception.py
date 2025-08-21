class BattleException(Exception):
    def __init__(self, message, action_messages=None):
        super().__init__(message)
        self.action_messages = action_messages if action_messages is not None else []
