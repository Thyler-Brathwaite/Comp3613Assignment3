class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, obs):
        self._observers.append(obs)

    def notify_observers(self, event_type, payload):
        for obs in self._observers:
            obs.update(event_type, payload)
