from __future__ import annotations
import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache
import copy
from enum import Enum

np.set_printoptions(threshold=np.inf)


class State(Enum):
    OFF = 0
    ON = 1


class Signal(Enum):
    LOW = 0
    HIGH = 1


class FlipFlop:
    def __init__(self, module_names, name) -> None:
        self.module_names = module_names
        self.name = name
        self.state = False

    def process(self, signal, sender):
        if signal == Signal.HIGH:
            return []
        self.state = not self.state
        return_signal = Signal.HIGH if self.state else Signal.LOW
        return [
            (self.name, return_signal, module_name) for module_name in self.module_names
        ]

    def is_initial(self):
        return not self.state


class Conjunction:
    def __init__(self, module_names, name) -> None:
        self.module_names = module_names
        self.name = name
        self.memory = {}

    def init_memory(self, module_names):
        for module_name in module_names:
            self.memory[module_name] = Signal.LOW

    def process(self, signal, sender):
        self.memory[sender] = signal
        return_signal = (
            Signal.HIGH if Signal.LOW in self.memory.values() else Signal.LOW
        )
        return [
            (self.name, return_signal, module_name) for module_name in self.module_names
        ]

    def is_initial(self):
        return Signal.HIGH not in self.memory.values()


class Broadcaster:
    def __init__(self, module_names, name) -> None:
        self.module_names = module_names
        self.name = name

    def process(self, signal, sender):
        return [(self.name, signal, module_name) for module_name in self.module_names]

    def is_initial(self):
        return True


def press_button_rx(modules, relevant_inputs):
    found_relevant_input = ""
    signals = [("button", Signal.LOW, "broadcaster")]
    while signals:
        new_signals = []
        for sender, signal, receiver in signals:
            if signal == Signal.HIGH and sender in relevant_inputs:
                found_relevant_input = sender
            if receiver not in modules:
                continue
            new_signals += modules[receiver].process(signal, sender)
        signals = new_signals
    return found_relevant_input


def press_button(modules):
    signal_count = {Signal.LOW: 0, Signal.HIGH: 0}
    signals = [("button", Signal.LOW, "broadcaster")]
    while signals:
        new_signals = []
        for sender, signal, receiver in signals:
            signal_count[signal] += 1
            if receiver not in modules:
                continue
            new_signals += modules[receiver].process(signal, sender)
        signals = new_signals
    return signal_count


def part1(data):
    modules = {}
    inputs = {}
    for line in data:
        if line.startswith("broadcaster"):
            _, module_names = line.split("->")
            module_names = module_names.replace(" ", "").split(",")
            name = "broadcaster"
            modules[name] = Broadcaster(module_names, name)
        elif line.startswith("%"):
            name, module_names = line.split("->")
            module_names = module_names.replace(" ", "").split(",")
            name = name.replace("%", "").replace(" ", "")
            modules[name] = FlipFlop(module_names, name)
        elif line.startswith("&"):
            name, module_names = line.split("->")
            module_names = module_names.replace(" ", "").split(",")
            name = name.replace("&", "").replace(" ", "")
            modules[name] = Conjunction(module_names, name)
        for module_name in module_names:
            if module_name not in inputs:
                inputs[module_name] = []
            inputs[module_name].append(name)

    for module in modules.values():
        if isinstance(module, Conjunction):
            module.init_memory(inputs[module.name])

    total_counts = {Signal.LOW: 0, Signal.HIGH: 0}
    total_loops = 1000
    for i in range(total_loops):
        counts = press_button(modules)
        total_counts[Signal.LOW] += counts[Signal.LOW]
        total_counts[Signal.HIGH] += counts[Signal.HIGH]
        all_initial = True
        for module in modules.values():
            all_initial &= module.is_initial()
            if not all_initial:
                break
        if all_initial:
            break
    loop_length = i + 1
    remaining_loops = total_loops // loop_length - 1
    total_counts[Signal.LOW] += remaining_loops * total_counts[Signal.LOW]
    total_counts[Signal.HIGH] += remaining_loops * total_counts[Signal.HIGH]
    remaining = total_loops - (remaining_loops + 1) * loop_length
    for i in range(remaining):
        counts = press_button(modules)
        total_counts[Signal.LOW] += counts[Signal.LOW]
        total_counts[Signal.HIGH] += counts[Signal.HIGH]

    return np.prod(list(total_counts.values()))


def part2(data):
    modules = {}
    inputs = {}
    for line in data:
        if line.startswith("broadcaster"):
            _, module_names = line.split("->")
            module_names = module_names.replace(" ", "").split(",")
            name = "broadcaster"
            modules[name] = Broadcaster(module_names, name)
        elif line.startswith("%"):
            name, module_names = line.split("->")
            module_names = module_names.replace(" ", "").split(",")
            name = name.replace("%", "").replace(" ", "")
            modules[name] = FlipFlop(module_names, name)
        elif line.startswith("&"):
            name, module_names = line.split("->")
            module_names = module_names.replace(" ", "").split(",")
            name = name.replace("&", "").replace(" ", "")
            modules[name] = Conjunction(module_names, name)
        for module_name in module_names:
            if module_name not in inputs:
                inputs[module_name] = []
            inputs[module_name].append(name)

    for module in modules.values():
        if isinstance(module, Conjunction):
            module.init_memory(inputs[module.name])

    relevant_inputs = []
    new_input = inputs["rx"][0]
    for input in inputs[new_input]:
        relevant_inputs.append(input)

    count = 0
    counts = []
    while len(relevant_inputs) > 0:
        count += 1
        found_relevant_input = press_button_rx(modules, relevant_inputs)
        if found_relevant_input != "":
            relevant_inputs.remove(found_relevant_input)
            counts.append(count)

    return np.lcm.reduce(counts)


if __name__ == "__main__":
    # file = "2023/day_20/test2.txt"
    # file = "test2.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
