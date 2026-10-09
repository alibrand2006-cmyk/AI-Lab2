class ClassroomAgent:
    def __init__(self):
        self.previous_mode = None

    def act(self, temp, occupied):
        if not occupied:
            target_mode = "ECO"
        elif temp > 26:
            target_mode = "COOL"
        elif temp < 20:
            target_mode = "WARM"
        else:
            target_mode = "IDLE"

        if target_mode == self.previous_mode:
            send_command = False
        else:
            send_command = True

        previous_mode = self.previous_mode
        self.previous_mode = target_mode

        return previous_mode, target_mode, send_command


agent = ClassroomAgent()

percepts = [
    (29, True),
    (29, True),
    (20, True),
    (26, True),
    (19, True),
    (29, False)
]

for percept in percepts:
    previous, target, command = agent.act(*percept)
    status = "COMMAND" if command else "NO COMMAND"

    print(
        "Previous:", previous,
        "| Percept:", percept,
        "| Target:", target,
        "|", status
    )