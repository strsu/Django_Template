from .base import *

if WHOAMI == "prod":
    from .production import *
elif WHOAMI == "dev":
    from .development import *
else:
    print("Unknown WHOAMI -", WHOAMI)
    exit()

print(f"Running - {WHOAMI}")

if WHOAMI == "dev":
    print("██████╗ ███████╗██╗   ██╗    ██████╗ ██████╗ ")
    print("██╔══██╗██╔════╝██║   ██║    ██╔══██╗██╔══██╗")
    print("██║  ██║█████╗  ██║   ██║    ██║  ██║██████╔╝")
    print("██║  ██║██╔══╝  ╚██╗ ██╔╝    ██║  ██║██╔══██╗")
    print("██████╔╝███████╗ ╚████╔╝     ██████╔╝██████╔╝")
    print("╚═════╝ ╚══════╝  ╚═══╝      ╚═════╝ ╚═════╝ ")
    print("                                     DEV DB  ")
elif WHOAMI == "prod":
    print("██████╗ ██████╗  ██████╗ ██████╗     ██████╗ ██████╗ ")
    print("██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██╔══██╗██╔══██╗")
    print("██████╔╝██████╔╝██║   ██║██║  ██║    ██║  ██║██████╔╝")
    print("██╔═══╝ ██╔══██╗██║   ██║██║  ██║    ██║  ██║██╔══██╗")
    print("██║     ██║  ██║╚██████╔╝██████╝     ██████╔╝██████╔╝")
    print("╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚════╝      ╚═════╝ ╚═════╝ ")
    print("                                            PROD DB  ")

import platform

print(platform.system())
