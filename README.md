# simple_banking_system_test
 
## Overview
- This repository contains a simple banking system implemented in Python. It includes 3 python scripts, namely a core banking system script, a utility for reading CSV files, and a unit test suite to validate the functionality. The project simulates basic banking operations such as account creation, deposits, withdrawals, transfers, and transaction logging, with data persistence using CSV files.

## Table of contents

## Features
- Users can create a new bank account with a name and starting balance
- Users can deposit money to their accounts
- Users can withdraw money from their accounts
- Users are not allowed to overdraft their accounts
- Users can transfer money to other accounts in the same banking system
- Save and load system state to CSV

## File Overview
1.[**`banking_system.py`**](https://github.com/victor-w-dev/simple_banking_system/blob/main/banking_system.py)
  - **Purpose**: The main script that defines the `BankAccount` and `BankingSystem` classes. It handles:  
     - Account creation and management.  
     - Transactions (deposits, withdrawals, transfers).  
     - Persistence of account details and transaction history in CSV files.  
     - Loading existing accounts and transactions on system startup.  
  - **Key Features**:  
    - Supports multiple accounts with unique IDs.  
    - Tracks balances and transactions with timestamps and reference numbers.  
    - Provides methods to view account balances and transaction histories.  
    - Example usage is included in the `if __name__ == "__main__":` block.

2.[**`system_reader.py`**](https://github.com/victor-w-dev/simple_banking_system/blob/main/system_reader.py)
  - **Purpose**: A utility script containing the `CSVLastRowExtractor` class, which efficiently extracts the last row of data from a CSV file using a deque. This is used by `banking_system.py` to load the latest account balances and transaction IDs.  
  - **Key Features**:  
    - Reads specific columns from the last row of a CSV file.  
    - Handles errors such as missing files or invalid columns.  
    - Lightweight and reusable for other CSV-based projects.
    
3.[**`unittest_banking_system.py`**](https://github.com/victor-w-dev/simple_banking_system/blob/main/unittest_banking_system.py)
  - **Purpose**: A unit test suite for `banking_system.py` using Python's `unittest` framework. It ensures the banking system functions correctly.  
  - **Key Features**:  
    - Tests account creation, deposits, withdrawals, transfers, and overdraft prevention.  
    - Automatically cleans up generated CSV files after each test run.  
    - Provides feedback on test success or failure.

## Getting Started

### Prerequisites
- Python 3.x installed on your system.

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/simple_banking_system_test.git
   cd simple_banking_system_test
2. No additional dependencies are required—all scripts use Python's standard library.

### Usage

1. **Run the Banking System**  
   Execute `banking_system.py` to see the example usage:  
   ```bash
   python banking_system.py
   ```
   This will create sample accounts, perform transactions, and display the system's state.
2. **Run Unit Tests**
   Test the banking system functionality:
   ```bash
   python unittest_banking_system.py
   ```
   The script will output test results and clean up generated files.
   
