DEBUG = True

# CORS_ALLOW_ALL_ORIGINS = True # 이건 True해도 WHITELIST 없으면 cors 발생함,,

CORS_ALLOW_CREDENTIALS = True  # 이건 반드시 필요, 없으면 cors 발생
CORS_ORIGIN_WHITELIST = [
    "https://localhost",
    "http://localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "https://localhost",
]

ALLOWED_HOSTS = ["*"]

# if DEBUG:

#     INTERNAL_IPS = ("127.0.0.1", "localhost")

#     DEBUG_TOOLBAR_PANELS = [
#         "debug_toolbar.panels.history.HistoryPanel",
#         "debug_toolbar.panels.versions.VersionsPanel",
#         "debug_toolbar.panels.timer.TimerPanel",
#         "debug_toolbar.panels.settings.SettingsPanel",
#         "debug_toolbar.panels.headers.HeadersPanel",
#         "debug_toolbar.panels.request.RequestPanel",
#         "debug_toolbar.panels.sql.SQLPanel",
#         "debug_toolbar.panels.staticfiles.StaticFilesPanel",
#         "debug_toolbar.panels.templates.TemplatesPanel",
#         "debug_toolbar.panels.cache.CachePanel",
#         "debug_toolbar.panels.signals.SignalsPanel",
#         "debug_toolbar.panels.redirects.RedirectsPanel",
#         "debug_toolbar.panels.profiling.ProfilingPanel",
#     ]

#     def show_toolbar(request):
#         return True

#     DEBUG_TOOLBAR_CONFIG = {
#         "SHOW_TOOLBAR_CALLBACK": show_toolbar,
#     }
