from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.db import connection
from django.core.cache import cache

from concurrent.futures import ThreadPoolExecutor, as_completed

from api.v1.model_view_set.models import Account

User = get_user_model()

# python manage.py test api.v1.model_view_set.tests.test_account


class AccountConcurrencyTest(TransactionTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test", email="test", password="test"
        )
        self.account = Account.objects.create(customer=self.user, balance=100)

    def tearDown(self):
        connection.close()

    def deposit_worker(self, deposit_amount):
        """
        Worker function to call deposit method for concurrency test.
        """
        try:
            Account.deposit(self.user, deposit_amount)
        except ValueError as e:
            return str(e)
        return None

    def withdraw_worker(self, withdraw_amount):
        """
        Worker function to call withdraw method for concurrency test.
        """
        try:
            Account.withdraw(self.user, withdraw_amount)
        except ValueError as e:
            return str(e)
        return None

    def test_concurrent_deposit(self):
        deposit_amount = 10
        num_threads = 10
        initial_balance = self.account.balance

        results = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(self.deposit_worker, deposit_amount)
                for _ in range(num_threads)
            ]
            for future in as_completed(futures):
                result = future.result()
                if future.done():
                    results.append(result)
                else:
                    future.cancelled()

        # Check if any thread raised an error due to race conditions or locking issues
        self.assertTrue(
            all(
                result is None or "잠시 후 다시 시도해주세요" in result
                for result in results
            )
        )

        # Refresh the account balance from the database
        self.account.refresh_from_db()

        successful_deposit = results.count(None)

        # Calculate the expected final balance
        expected_balance = initial_balance + deposit_amount * successful_deposit
        self.assertEqual(self.account.balance, expected_balance)

        # Ensure cache is cleared after the test
        account_key = f"account_deposit_key:{self.user.uuid}"
        self.assertIsNone(cache.get(account_key))

        print(f"입금성공: {successful_deposit}")
        print(f"입금실패: {num_threads-successful_deposit}")

    def test_concurrent_withdraw(self):
        withdraw_amount = 10
        num_threads = 10
        initial_balance = self.account.balance

        results = []
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(self.withdraw_worker, withdraw_amount)
                for _ in range(num_threads)
            ]
            for future in as_completed(futures):
                result = future.result()
                if future.done():
                    results.append(result)
                else:
                    future.cancelled()

        # Check if any thread raised an error due to insufficient funds or other issues

        self.assertTrue(
            all(result is None or result == "잔액이 부족합니다." for result in results)
        )

        # Refresh the account balance from the database
        self.account.refresh_from_db()

        # Calculate the expected final balance
        successful_withdrawals = results.count(None)
        sufficient_funds_errors = num_threads - successful_withdrawals
        expected_balance = initial_balance - withdraw_amount * successful_withdrawals

        self.assertEqual(self.account.balance, expected_balance)

        # Ensure that there are no more successful withdrawals than the balance would allow
        self.assertTrue(successful_withdrawals <= initial_balance // withdraw_amount)
        self.assertTrue(
            sufficient_funds_errors
            >= num_threads - (initial_balance // withdraw_amount)
        )

        # Print some debug information
        print(f"출금성공: {successful_withdrawals}")
        print(f"출금실패: {sufficient_funds_errors}")
