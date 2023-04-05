from cx_Freeze import setup, Executable

setup(name="Person and Cell Phone Detector ",
      version = "0.1",
      description = "This is a small program to detect persons and cellphones in realtime ",
      executable = [Executable("program.py")]
      )