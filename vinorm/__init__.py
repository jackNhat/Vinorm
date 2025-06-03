import subprocess
import os
import importlib.util

def TTSnorm(text, punc=False, unknown=True, lower=True, rule=False):
    # Use importlib.util.find_spec to find the location of vinorm
    spec = importlib.util.find_spec("vinorm")
    if spec is None or not spec.origin:
        raise ModuleNotFoundError("vinorm module not found")

    # Get the directory containing the vinorm module
    vinorm_dir = os.path.dirname(spec.origin)

    # Write input text to file
    input_file = os.path.join(vinorm_dir, "input.txt")
    with open(input_file, "w+", encoding="utf-8") as fw:
        fw.write(text)

    # Set environment variable
    myenv = os.environ.copy()
    myenv['LD_LIBRARY_PATH'] = os.path.join(vinorm_dir, "lib")

    # Prepare command
    executable = os.path.join(vinorm_dir, "main")
    command = [executable]
    if punc:
        command.append("-punc")
    if unknown:
        command.append("-unknown")
    if lower:
        command.append("-lower")
    if rule:
        command.append("-rule")

    # Execute the command
    subprocess.check_call(command, env=myenv, cwd=vinorm_dir)

    # Read output text from file
    output_file = os.path.join(vinorm_dir, "output.txt")
    with open(output_file, "r", encoding="utf-8") as fr:
        output_text = fr.read()

    # Process output
    TEXT = ""
    S = output_text.split("#line#")
    for s in S:
        if s == "":
            continue
        TEXT += s + ". "

    return TEXT
