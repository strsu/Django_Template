from .base import *

if WHOAMI == "prod":
    from .production import *
elif WHOAMI == "dev":
    from .development import *
else:
    print("Unknown WHOAMI -", WHOAMI)
    exit()

print(f"Running - {WHOAMI}, DEBUG - {DEBUG}")

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

if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer"
    ]

MYIP = [
    f"http://{MY_LOCAL_IP}",
    f"https://{MY_LOCAL_IP}",
    f"http://{MY_PUBLIC_IP}",
    f"https://{MY_PUBLIC_IP}",
    f"http://{HOST}",
    f"https://{HOST}",
]

CORS_ORIGIN_WHITELIST += MYIP
CSRF_TRUSTED_ORIGINS += MYIP
