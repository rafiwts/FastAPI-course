from app.calc import add, BankAccount
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def regular_bank_account():
    return BankAccount(1000)


def test_bank_set_initial_amount(regular_bank_account):
    assert regular_bank_account.balance == 1000


def test_default_ammount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_deposit(regular_bank_account):
    regular_bank_account.deposit(300) == 1300


def test_withdraw(regular_bank_account):
    regular_bank_account.withdraw(400) == 600 


def test_interest(regular_bank_account):
    regular_bank_account.balance == 1100


def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(100)
    assert zero_bank_account.balance == 100


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (10, 40, 50),
    (12, 4, 16)
]) # treated like variable

def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

@pytest.mark.parametrize("deposited, withdrew, expected",[
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000),
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(regular_bank_account):
    with pytest.raises(Exception):
        regular_bank_account.withdraw(1200)

