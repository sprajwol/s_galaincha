from django.apps import AppConfig


class LoginSystemConfig(AppConfig):
    name = 'login_system'

    def ready(self):
        import login_system.signals
