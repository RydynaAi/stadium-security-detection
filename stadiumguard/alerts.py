import sys


class AlertManager:
    def __init__(self, log, cooldown_seconds):
        self.log = log
        self.cooldown = cooldown_seconds
        self.last_alert = {}

    def handle(self, event, image):
        last = self.last_alert.get(event.event_type)
        if last is not None and event.timestamp - last < self.cooldown:
            return False
        self.last_alert[event.event_type] = event.timestamp
        self.log.record(event, image)
        print(f"ALERT {event.event_type} at {event.timestamp:.2f}s (confidence {event.confidence:.2f})")
        sys.stdout.write("\a")
        sys.stdout.flush()
        return True 
