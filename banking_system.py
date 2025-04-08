import csv
import os
import time
from datetime import datetime
import itertools
from system_reader import CSVLastRowExtractor

class BankAccount:
    def __init__(self, account_id: int, user_name: str, balance: float = 0.0, currency: str = 'HKD') -> None:
        """
        Initialize the BankAccount class with account details.

        :param account_id: Unique identifier for the account
        :param user_name: Name of the account holder
        :param balance: Initial balance of the account (default is 0.0)
        :param currency: Currency type of the account (default is 'HKD')
        """
        self.account_id = account_id
        self.user_name = user_name
        self.balance = balance
        self.currency = currency
        self._account_transactions_filename = f'{self.account_id}_transactions.csv'

    def __str__(self):
        return f"Account no. {self.account_id} - {self.user_name}: {self.currency} ${self.balance:,.2f}"

    def deposit(self, amount, banking_system):
        """
        Deposit a specified amount into the account.

        :param amount: Amount to deposit
        :param banking_system: Instance of the BankingSystem class
        :raise ValueError: If the deposit amount is not positive
        """
        if amount > 0:
            self.balance += amount
            transaction_id = next(banking_system._transaction_id_counter)
            reference_number = next(banking_system._reference_number_counter)
            banking_system.record_transaction(self, 'deposit', amount, transaction_id, reference_number)
            print(f"{self.user_name} deposited: {self.currency} ${amount:,.2f}")
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount, banking_system):
        """
        Withdraw a specified amount from the account if sufficient funds exist.

        :param amount: Amount to withdraw
        :param banking_system: Instance of the BankingSystem class
        :raise ValueError: If the withdrawal amount is invalid or exceeds the balance
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            transaction_id = next(banking_system._transaction_id_counter)
            reference_number = next(banking_system._reference_number_counter)
            banking_system.record_transaction(self, 'withdraw', amount, transaction_id, reference_number)
            print(f"{self.user_name} withdrew: {self.currency} ${amount:,.2f}")
        else:
            raise ValueError("Insufficient funds or invalid withdrawal amount.")

    def transfer(self, target_account, amount, banking_system):
        """
        Transfer a specified amount to another account if sufficient funds exist.

        :param target_account: The target BankAccount to transfer funds to
        :param amount: Amount to transfer
        :param banking_system: Instance of the BankingSystem class
        :raise ValueError: If the transfer amount is invalid or exceeds the balance
        """
        if 0 < amount <= self.balance:
            self.balance -= amount
            target_account.balance += amount
            transaction_id = next(banking_system._transaction_id_counter)
            reference_number = next(banking_system._reference_number_counter)
            banking_system.record_transaction(self, 'transfer_to', amount, transaction_id, reference_number, target_account)
            target_transaction_id = next(banking_system._transaction_id_counter)          
            banking_system.record_transaction(target_account, 'receive_from', amount, target_transaction_id, reference_number, self)
            print(f"{self.user_name} transfered: {self.currency} ${amount:,.2f} to {target_account.user_name}")
        else:
            raise ValueError("Insufficient funds or invalid transfer amount.")
    
    def view_transactions(self, banking_system):
        """
        View all transactions associated with this account.

        :param banking_system: Instance of the BankingSystem class
        """
        banking_system.read_account_transaction(self.account_id)
        
    def view_balance(self):
        """
        View the current balance of the account.

        :return: The current balance
        """
        return self.balance

class BankingSystem:
    def __init__(self):
        self.accounts = {}
        self._system_accounts_filename = 'system_accounts.csv'
        self._system_transactions_filename = 'system_transactions.csv'
        self._account_id_counter = itertools.count(1)
        self._transaction_id_counter = itertools.count(1)
        self._reference_number_counter = itertools.count(1)
        self._load_account_profiles_and_balances()
        self._load_latest_transaction_id_ref()
        print("Banking system is running now.")
    
    def set_system_filenames(self, system_accounts_filename, system_transactions_filename):
        self._system_accounts_filename  = system_accounts_filename 
        self._system_transactions_filename = system_transactions_filename

    def __del__(self):
        print("Destructor called.")
        print("Turned off the BankingSystem.\n")
    
    def _load_account_profiles_and_balances(self):
        """
        Load account profiles and their latest balances from the system_accounts.csv and {account_id}_transactions.csv.
        """
        if os.path.isfile(self._system_accounts_filename):
            with open(self._system_accounts_filename , 'r') as csvfile:
                print("Geting system's accounts")
                reader = csv.reader(csvfile)
                next(reader)
                
                last_account_id = None
                
                for row in reader:
                    account_id, user_name, _ = row
                    if user_name not in self.accounts:
                        account_id, currency, balance, timestamp_end = self._load_account_latest_balance(int(account_id))
                        self.accounts[user_name] = BankAccount(account_id, user_name, balance, currency)
                    else:
                        print(f"Duplicate account found for username '{user_name}'. Skipping loading of this account.")
                
                if last_account_id is not None:
                    # Update latest account_id
                    self._account_id_counter = itertools.count(last_account_id + 1)
        else:
            print("Banking system is new, no any account information yet.")
    
    def _load_latest_transaction_id_ref(self):
        """
        Load the latest transaction and reference numbers from the system_transactions.csv.
        """
        if os.path.isfile(self._system_transactions_filename):
            columns_to_extract = ['transaction_id', 'reference_number']
            
            # Extract the desired columns from the last row
            extracted_values = CSVLastRowExtractor.extract_last_rows(self._system_transactions_filename, columns_to_extract)
            
            last_transaction_id, last_reference_number = extracted_values
                
            self._transaction_id_counter = itertools.count(int(last_transaction_id) + 1)
            self._reference_number_counter = itertools.count(int(last_reference_number) + 1)
            
        else:
            print("Banking system is new, no any transaction records yet.")
                    
    def _load_account_latest_balance(self, account_id: int):
        """
        Load the latest balance of a specific account from its transaction file: {account_id}_transactions.csv.

        :param account_id: Unique identifier for the account
        :return: Tuple containing account_id, currency, balance, and timestamp_end
        """    
        file_path = f"{account_id}_transactions.csv"
        columns_to_extract = ['account_id', 'currency', 'balance', 'timestamp_end']
        
        # Extract the desired columns from the last row using CSVLastRowExtractor class method
        extracted_values = CSVLastRowExtractor.extract_last_rows(file_path, columns_to_extract)
        
        account_id, currency, balance, timestamp_end = extracted_values
            
        return int(account_id), currency, float(balance), timestamp_end               
    
    def create_account(self, user_name, starting_balance=0.0, currency='HKD'):
        """
        Create a new account for a user.

        :param user_name: Name of the account holder
        :param starting_balance: Initial balance of the account (default is 0.0)
        :param currency: Currency type of the account (default is 'HKD')
        """
        if user_name in self.accounts:
            print(f"Account with username '{user_name}' already exists. Skipping creation.")
            return
        
        account_id = next(self._account_id_counter)
        new_account = BankAccount(account_id, user_name, starting_balance, currency)
        self.accounts[user_name] = new_account
        transaction_id = next(self._transaction_id_counter)
        reference_number = next(self._reference_number_counter)
        self.record_transaction(new_account, 'create_account', starting_balance, transaction_id, reference_number)
        print(f"Created account with username '{user_name}'\n")
    
    def get_account(self, user_name):
        """
        Retrieve an account by username.

        :param user_name: Name of the account holder
        :return: BankAccount instance
        :raise ValueError: If no account is found with the given username
        """
        account = self.accounts.get(user_name)
        if not account:
            raise ValueError(f"No account found with user_name: {user_name}")
        return account

    def save_account_profiles(self, transaction):
        """
        Save account profiles to the system accounts file.

        :param transaction: Transaction details
        """
        file_exists = os.path.isfile(self._system_accounts_filename)
        
        with open(self._system_accounts_filename, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['account_id', 'user_name', 'account_created_time'])
 
            writer.writerow([transaction['account_id'], transaction['user_name'], transaction['timestamp_end']])
   
    def check_transaction_validity(self, transaction, latency=0.1):
        """
        Check the validity of a transaction. Simulated to always be valid.

        :param transaction: Transaction details
        :param latency: Simulated latency in seconds (default is 0.1)
        :return: True, indicating the transaction is valid
        """
        time.sleep(latency)
        return True
                
    def record_transaction(self, account, transaction_type, amount, transaction_id: int, reference_number: int, target_account=None):
        """
        Record a transaction for an account.

        :param account: BankAccount instance
        :param transaction_type: Type of transaction (e.g.'create_account', 'deposit', 'withdraw', 'transfer_to', 'receive_from')
        :param amount: Amount involved in the transaction
        :param transaction_id: Unique identifier for the transaction
        :param reference_number: Reference number for the transaction, same reference number for a pair of 'transfer_to' and 'receive_from' transaction
        :param target_account: Target BankAccount instance for transfer transactions (default is None)
        """
        transaction = {
            'transaction_id': transaction_id,
            'timestamp_start': datetime.now().isoformat(),
            'account_id': account.account_id,
            'user_name': account.user_name,
            'type': transaction_type,
            'amount': amount,
            'currency': account.currency,
            'balance': account.balance,
        }
        
        if target_account:
            transaction['target_id'] = target_account.account_id
            transaction['target_user_name'] = target_account.user_name
        else:
            transaction['target_id'] = None
            transaction['target_user_name'] = None

        if self.check_transaction_validity(transaction):
            transaction['timestamp_end'] = datetime.now().isoformat()
            transaction['status'] = 'Completed'  
            transaction['reference_number'] =  reference_number
            transaction['remarks'] =  None
        else:
            transaction['timestamp_end'] = datetime.now().isoformat()
            transaction['status'] = 'Failed'
            transaction['reference_number'] = None
            transaction['remarks'] =  'checked invalid'

        self._log_to_transaction_csv(self._system_transactions_filename, transaction)
        self._log_to_transaction_csv(account._account_transactions_filename, transaction)   
        
        if transaction_type == "create_account":
            self.save_account_profiles(transaction)
        
        # Print transaction details
        print(f"Transaction ID: {transaction_id}, User: {account.user_name}, Type: {transaction_type}, "
              f"Amount: {amount}, Balance: {account.balance}, Status: {transaction['status']}, Reference no.: {reference_number}")
            
    def _generate_account_transaction(self, account_id: int):
        """
        Generate transactions for a specific account from its transaction file: {account_id}_transactions.csv.
    
        :param account_id: Unique identifier for the account
        :return: Generator yielding dictionaries containing transaction details
        """
        file_path = f"{account_id}_transactions.csv"

        if os.path.isfile(file_path):
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    yield row
     
    def read_account_transaction(self, account_id: int):
        """
        Read and print transactions for a specific account using the generator.
        
        :param account_id: Unique identifier for the account
        """
        # Using the generator to read transactions
        transactions = self._generate_account_transaction(account_id)
        
        # Iterate over the generator and print each transaction
        for transaction in transactions:
            print(transaction)
        
    def _log_to_transaction_csv(self, file, transaction):
        print(f"logging to {file}...")
        file_exists = os.path.isfile(file)

        with open(file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(['transaction_id', 'timestamp_start', 'account_id', 'user_name', 'type', 'amount', 
                                 'currency', 'balance', 'target_id', 'target_user_name', 'reference_number', 'timestamp_end', 'status',
                                 'remarks'
                                 ])
            
            writer.writerow([
                    transaction['transaction_id'],
                    transaction['timestamp_start'],
                    transaction['account_id'],
                    transaction['user_name'],
                    transaction['type'],
                    transaction['amount'],
                    transaction['currency'],
                    transaction['balance'],
                    transaction['target_id'],
                    transaction['target_user_name'],
                    transaction['reference_number'],
                    transaction['timestamp_end'],
                    transaction['status'],
                    transaction['remarks']
            ])

    def get_total_accounts(self):
        return len(self.accounts)

    def get_total_balance(self):
        return sum(account.balance for account in self.accounts.values())
    
    def get_average_balance(self):
        total_accounts = self.get_total_accounts()
        total_balance = self.get_total_balance()
        return total_balance / total_accounts if total_accounts > 0 else 0

    def __str__(self):
        account_summary = "\n".join(str(account) for account in self.accounts.values())
        total_accounts = self.get_total_accounts()
        total_balance = self.get_total_balance()
        average_balance = self.get_average_balance()
        result = (
            f"{account_summary}\n\n"
            f"Total No. of Accounts: {total_accounts}\n"
            f"Total Balance: HKD ${total_balance:,.2f}\n"
            f"Average Account Balance: HKD ${average_balance:,.2f}\n"
        )
        return result
    
# Usage Example
if __name__ == "__main__":
    start_time = time.time()  # Record the start time

    # Initialization of the banking system
    banking_system = BankingSystem()
    
    # Create accounts
    banking_system.create_account("Ben", 1000.0)
    banking_system.create_account("Ricky", 500.0)
    
    # Retrieve the accounts
    ben_account = banking_system.get_account("Ben")
    ricky_account = banking_system.get_account("Ricky")
    
    # illustate the system if not have the account
    try:
        victor_account = banking_system.get_account("Victor")
        print(victor_account)
    except ValueError as e:
        print(e)
    
    print("\nInitial state:")
    print(banking_system)
    
    # Perform some transactions
    # Ben deposits 500
    ben_account.deposit(500, banking_system)
    print("\nAfter Ben deposits 500:")
    print(banking_system)

    # Ricky withdraws 200
    ricky_account.withdraw(200, banking_system)
    print("\nAfter Ricky withdraws 200:")
    print(banking_system)
    
    # Create account
    banking_system.create_account("Victor", 25000.5)
    victor_account = banking_system.get_account("Victor")
    print(banking_system)

    # Ben transfers 300 to Ricky
    ben_account.transfer(ricky_account, 300, banking_system)
    print("\nAfter Ben transfers 300 to Ricky:")
    print(banking_system)
    
    # Victor transfers 1000.52 to Ricky
    victor_account.transfer(ricky_account, 1000.52, banking_system)
    print("\nAfter Victor transfers 1000.52 to Ricky:")
    print(banking_system)
    
    # Turn off the system
    del banking_system
    
    # Initialization of the banking system
    print("\nInitial state again:")
    next_banking_system = BankingSystem()
    # The new day banking system will load existing system_accounts, system_transactions CSV
    print(next_banking_system)
    
    # Retrieve the accounts
    ben_account = next_banking_system.get_account("Ben")
    victor_account = next_banking_system.get_account("Victor")
    
    # Ben withdraws 1000
    ben_account.withdraw(1000, next_banking_system)
    print("\nAfter Ben withdraws 1000:")
    print(next_banking_system)
    
    # Victor transfers 50 to Ben
    victor_account.transfer(ben_account, 50, next_banking_system)
    print("\nAfter Victor transfers 50 to Ben:")
    print(next_banking_system)
    
    print("From Banking System's view - list Ben's transaction records:")
    # Ben account_id is 1
    next_banking_system.read_account_transaction(1)
    
    print("\nFrom Account User's view - list user's own transaction records:")
    victor_account.view_transactions(next_banking_system)

    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Time taken: {elapsed_time:.2f} seconds")