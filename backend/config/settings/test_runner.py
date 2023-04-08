from django.test.runner import DiscoverRunner

# python manage.py test vpp --settings='config.settings.test'


class TestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
