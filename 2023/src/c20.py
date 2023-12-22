from shared import BaseChallenge


class Component:
    def __init__(self, line: str, components: dict[str, "Component"]):
        label, destinations = line.split("->")
        destinations = destinations.split(",")

        self.label = label.strip()
        self.components = components
        components[self.label] = self
        self.destinations = [destination.strip() for destination in destinations]
        self.high_counter = 0
        self.low_counter = 0

    @classmethod
    def from_line(cls, line: str, components: dict[str, "Component"]) -> "Component":
        if line[0] == "%":
            return Flipper(line[1:], components)
        if line[0] == "&":
            return Conjunction(line[1:], components)
        if line.startswith("broadcaster"):
            return Broadcaster(line, components)
        raise ValueError(f"Unknown component: {line}")

    def input(self, pulse: bool, sender: "Component"):
        if pulse:
            self.high_counter += 1
        else:
            self.low_counter += 1

    def send_to_destination(self, pulse: bool):
        for destination in self.destinations:
            if destination in self.components:
                self.components[destination].input(pulse, self)
            else:
                if pulse:
                    self.high_counter += 1
                else:
                    self.low_counter += 1

    def __repr__(self):
        return f"Component(label={self.label},destinations={self.destinations})"


class Broadcaster(Component):
    def input(self, pulse: bool, sender: "Component"):
        super().input(pulse, sender)
        self.send_to_destination(pulse)

    def __repr__(self):
        return f"Broadcaster(label={self.label},destinations={self.destinations})"


class Flipper(Component):
    def __init__(self, line: str, components: dict[str, "Component"]):
        super().__init__(line, components)
        self.pulse = False

    def input(self, pulse: bool, sender: "Component"):
        super().input(pulse, sender)
        if not pulse:
            self.pulse = not self.pulse
            self.send_to_destination(self.pulse)

    def __repr__(self):
        return f"Flipper(label={self.label},destinations={self.destinations})"


class Conjunction(Component):
    def __init__(self, line: str, components: dict[str, "Component"]):
        super().__init__(line, components)
        self.pulses = {
            label: False
            for label, component in components.items()
            if self.label in component.destinations
        }

    def input(self, pulse: bool, sender: "Component"):
        super().input(pulse, sender)
        self.pulses[sender.label] = pulse
        self.send_to_destination(not all(self.pulses.values()))

    def __repr__(self):
        return f"Conjunction(label={self.label},destinations={self.destinations})"


class Rx(Component):
    def __init__(self, line: str, components: dict[str, "Component"]):
        super().__init__(line, components)
        self.rx_low_counter = 0
        self.rx_high_counter = 0

    def input(self, pulse: bool, sender: "Component"):
        super().input(pulse, sender)
        if pulse:
            self.rx_high_counter += 1
        else:
            self.rx_low_counter += 1

    @property
    def has_ended(self):
        return self.rx_low_counter == 1

    def __repr__(self):
        return f"Rx(label={self.label},h={self.rx_high_counter},l={self.rx_low_counter}"


class Challenge20(BaseChallenge):
    def __init__(self):
        super().__init__()
        self.components: dict[str, Component] = {}

    def _press_button(self):
        self.components["broadcaster"].input(False, None)

    def first(self):
        """ """
        self.components: dict[str, Component] = {}
        for line in self.stripped_lines:
            Component.from_line(line, self.components)

        for _ in range(1000):
            self._press_button()

        low_counter = 0
        high_counter = 0
        for component in self.components.values():
            low_counter += component.low_counter
            high_counter += component.high_counter

        return low_counter * high_counter

    def second(self):
        """ """
        self.components: dict[str, Component] = {}
        for line in self.stripped_lines:
            Component.from_line(line, self.components)
        self.components["rx"] = Rx("rx ->", self.components)

        counter = 0
        while not self.components["rx"].has_ended:
            self.components["rx"].rx_low_counter = 0
            self.components["rx"].rx_high_counter = 0
            self._press_button()
            print(self.components["rx"], counter)
            counter += 1

        return counter


if __name__ == "__main__":
    Challenge20().run()
