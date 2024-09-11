from .base import *

from decimal import Decimal, ROUND_HALF_UP, getcontext

"""
decimal context는 context를 설정한 파일에만 적용되는게 아니라 django 전체 시스템에 적용된다.
때문에 getcontext().prec 을 여러곳에서 설정하게 되면 가장 마지막에 설정된 값으로 유지되기 때문에
안전하게 settings에서 한번만 설정을 하는게 가장 좋을 것 같다.
"""
getcontext().prec = 20  # 전체 자릿수를 20으로 설정
getcontext().rounding = ROUND_HALF_UP
print(f"Decimal Context - {globals()['getcontext']()}")


if WHOAMI == "prod":
    from .production import *
elif WHOAMI == "dev":
    from .development import *
else:
    print("Unknown WHOAMI -", WHOAMI)
    exit()

if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer"
    ]

MYIP = [
    f"http://{MY_LOCAL_IP}",
    f"https://{MY_LOCAL_IP}",
    f"http://{MY_PUBLIC_IP}",
    f"https://{MY_PUBLIC_IP}",
]

for _host in HOST:
    MYIP += [
        f"http://{_host}",
        f"https://{_host}",
    ]

CORS_ORIGIN_WHITELIST += MYIP
CSRF_TRUSTED_ORIGINS += MYIP

if False:

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

    print(f"CORS_ORIGIN_WHITELIST: {CORS_ORIGIN_WHITELIST}")
    print(f"CSRF_TRUSTED_ORIGINS: {CSRF_TRUSTED_ORIGINS}")
