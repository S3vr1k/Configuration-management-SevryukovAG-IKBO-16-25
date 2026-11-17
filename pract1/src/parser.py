import os
import shlex

def parse_command(text):
    tokens = shlex.split(text)

    if not tokens:
        return []

    command = tokens[0]
    arguments = []

    for token in tokens[1:]:
        arguments.append(os.path.expandvars(token))

    return [command, *arguments]