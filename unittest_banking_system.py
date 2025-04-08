import unittest
import os
from banking_system import BankingSystem
 
class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        self.system = BankingSystem()
        self.system.create_account("Ben", 500)
        self.system.create_account("Ricky", 300)
        self.system.create_account("Victor", 200.25)
        
    def tearDown(self):
        print("\nDelete files during unittest")
        # Clean up any files that may have been created during testing
        for account in self.system.accounts.values():
            account_file = f"{account.account_id}_transactions.csv"
            if os.path.isfile(account_file):
                os.remove(account_file)
        
        # Clean up the system accounts file if it exists
        if os.path.isfile(self.system._system_accounts_filename):
            os.remove(self.system._system_accounts_filename)
        
        # Clean up the system transactions file if it exists
        if os.path.isfile(self.system._system_transactions_filename):
            os.remove(self.system._system_transactions_filename)

    def test_create_account(self):
        print("Unittest: create account")
        self.system.create_account("Linda", 200)
        linda_account = self.system.get_account("Linda")
        self.assertEqual(linda_account.balance, 200)

    def test_deposit(self):
        print("Unittest: deposit")
        ben_account = self.system.get_account("Ben")
        ben_account.deposit(200, self.system)
        self.assertEqual(ben_account.balance, 700)

    def test_withdraw(self):
        print("Unittest: withdraw")
        ben_account = self.system.get_account("Ben")
        ben_account.withdraw(100, self.system)
        self.assertEqual(ben_account.balance, 400)

    def test_overdraft(self):
        print("Unittest: prevent overdraft")
        ben_account = self.system.get_account("Ben")
        with self.assertRaises(ValueError):
            ben_account.withdraw(600, self.system)

    def test_transfer(self):
        print("Unittest: transfer")
        ben_account = self.system.get_account("Ben")
        ricky_account = self.system.get_account("Ricky")
        victor_account = self.system.get_account("Victor")
        
        ben_account.transfer(ricky_account, 150, self.system)
        ben_account.transfer(victor_account, 10.2 , self.system)
        self.assertEqual(ben_account.balance, 339.8)
        self.assertEqual(ricky_account.balance, 450)
        self.assertEqual(victor_account.balance, 210.45)

if __name__ == "__main__":
    unittest.main()
