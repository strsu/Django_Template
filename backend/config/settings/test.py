from config.settings.production import *

# production을 import 했기 때문에 manage.py 에서 테스트 코드를 돌려야 한다.
TEST_RUNNER = "config.settings.test_runner.TestRunner"
