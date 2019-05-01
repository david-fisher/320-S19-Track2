import datetime as datetime


class User():

    def __init__(self, first_name, last_name, customer_token):
        self.first_name = first_name
        self.last_name = last_name
        self.stripe_customer = customer_token
        self.verification_charge = None
        self.is_verified = False
        self.last_verified = None

    def save(self):
      pass

    def __str__(self):
      return self.first_name + " " + self.last_name

class VerificationCharge():
    def __init__(self, timestamp, amount):
      self.timestamp = timestamp
      self.amount = amount