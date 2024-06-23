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

CORS_ORIGIN_WHITELIST += [MY_LOCAL_IP, MY_PUBLIC_IP]
CSRF_TRUSTED_ORIGINS += [MY_LOCAL_IP, MY_PUBLIC_IP]
