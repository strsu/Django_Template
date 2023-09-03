from .base import *

if WHOAMI == "prod":
    from .production import *
elif WHOAMI == "dev":
    from .development import *
else:
    print("Unknown WHOAMI -", WHOAMI)
    exit()

print(f"Running - {WHOAMI}")
