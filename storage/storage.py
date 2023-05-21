class BaseStorage:
    def is_known_user(self, user_id):
        pass

    def save_event(self, user_id, event):
        pass

    def get_user_events(self, user_id):
        pass

    def delete_event(self, user_id, event):
        pass

    def close(self):
        pass
