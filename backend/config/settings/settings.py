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

MYIP = [
    f"http://{MY_LOCAL_IP}",
    f"https://{MY_LOCAL_IP}",
    f"http://{MY_PUBLIC_IP}",
    f"https://{MY_PUBLIC_IP}",
]

CORS_ORIGIN_WHITELIST += MYIP
CSRF_TRUSTED_ORIGINS += MYIP
