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


@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (10, 40, 50),
    (12, 4, 16)
]) # treated like variable

def test_add(num1, num2, expected):
    assert add(num1, num2) == expected
