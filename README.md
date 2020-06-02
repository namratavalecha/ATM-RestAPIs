# ATM - REST APIs

This repository consists of the basic functionalities for an ATM machine using Django.

## Problem Statement:

Minimum Requirement  :  

1. Create an API to register a user's card (8-digits) and ATM Pin (4-digits)

2. Create an authentication API to validate the user by 8-digit card number and 4-digit ATM pin.

3. Create an API to deposit the money in the user's account.

4. Create an API to withdraw the money from the user's bank account.

NOTE: Keep the following things in considerations:

1- ATM Machine should always give the least number of notes (example: if the user withdraw Rs 2500, the ATM machine should give 1 note of Rs 2000 and 1 note of Rs 500)

2- The number of notes should be reduced/increase in ATM on every transaction.

3- The user cannot withdraw more than Rs 20,000 in one transaction.

## Deployment

### Setup
```bash
pip install -r requirements.txt
```

### Run in dev
```bash
virtualenv venv
source venv/bin/activate
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Registering a User's card and pin

![Screenshot from 2020-06-03 04-46-03](https://user-images.githubusercontent.com/40838784/83578773-39475200-a555-11ea-99ab-3f0251c2bf0f.png)

## Validate Card number and pin

![Screenshot from 2020-06-03 04-43-09](https://user-images.githubusercontent.com/40838784/83578981-ae1a8c00-a555-11ea-84d9-2025c194dbb7.png)

## Making a Deposit

![Screenshot from 2020-06-03 04-41-03](https://user-images.githubusercontent.com/40838784/83579030-cb4f5a80-a555-11ea-8650-2dfa9843534c.png)

## Withdrawing Money

![Screenshot from 2020-06-03 04-39-37](https://user-images.githubusercontent.com/40838784/83579071-e6ba6580-a555-11ea-9ec8-75436a11f95b.png)
