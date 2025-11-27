class Observer:
    def update(self, subject, event_type, payload):
        raise NotImplementedError("Observer must implement update")
