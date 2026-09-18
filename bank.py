from decimal import Decimal , InvalidOperation
import json

class BankAccount:
    def __init__(self,name,account_number,balance):
        self.name =  name
        self.account_number = account_number
        self.balance  = balance
        self.history = []
    def view_balance(self):
        print("Your balance: ",self.balance) 

    def deposit(self,amount,operation,num = None):
        if amount > 0:
          self.balance += amount
          if operation == "deposit":
           self.history.append("Deposit: "+"+"+str(amount))
          elif operation == "transfer":
           self.history.append("Transfer from account "+str(num)+": "+str(amount))
          return True
        else:
          print("\nEnter a valid amount!(greater than zero)") 
          return False 
               
    def withdraw(self,amount,operation,num = None):
            if amount > 0:
                if self.balance >= amount: 
                    self.balance -= amount
                    if operation == "withdraw":
                     self.history.append("Withdraw: "+"-"+str(amount))
                    elif operation == "transfer":
                      self.history.append("Transfer to account "+str(num)+": "+str(amount))
                    return True
                else:
                    print("\nYour balance is not enough!")
                    return False 
            else:
                print("\nEnter a valid amount!(greater than zero)") 
                return False 

    def show_info(self):
        print("\nName:",self.name)     
        print("Account Number:",self.account_number)
        print("Balance:",self.balance) 
accounts = {}       
try:
  with open("accounts.json","r") as file:
    data = json.load(file)
except FileNotFoundError:
  data = {}    
except json.JSONDecodeError:
  data = {}     

for account_number , accounts_data in data.items():
  account = BankAccount(accounts_data["name"],accounts_data["account_number"],Decimal(accounts_data["balance"]))
  account.history = accounts_data["history"]
  accounts[account_number] = account
  
def save_accounts():
  accounts_data = {}
  for account_number , account in accounts.items():
    accounts_data[account_number] = {"name":account.name,"account_number":account.account_number
    ,"balance" : str(account.balance) , "history" : account.history}
  with open("accounts.json","w") as file:
    json.dump(accounts_data,file,indent = 4)


print("=== Bank Account ===\n")
while True:
    print("\n1. Create Account")
    print("2. Access Account")
    print("3. Exit\n")
    option=input("Choose an option(1/2/3): ")
    if option == "1":
      while True:
       name  = input("Enter your name: ").lower()
       if not name.replace(" ","").isalpha():
        print("\nInvalid Input!it must be letters\n")
        continue
       break
      while True:
       account_number = input("Enter your account number: ")
       if not account_number.isdigit():
        print("\nInvalid Input!it must be numbers\n")
        continue 
       break
       
      if account_number in accounts:
        print("\nThis account number already exists,try another one!")
        continue
      while True:
        try:
          balance = Decimal(input("Enter your initial balance: "))
          if balance > 0:
           break
          print("\nInitial balance must be greater than zero!\n")
        except InvalidOperation:
          print("\nInvalid Input!\n")  
      
      account = BankAccount(name,account_number,balance)
      accounts[account_number] = account
      save_accounts()
      print("\nYour account has been successfully created!\n")  
    
    elif option == "2":
      account_number = input("Enter your account number: ")    
      if account_number in accounts:
        account = accounts[account_number]

        while True:
          print("\n1. View Balance")
          print("2. Deposit")
          print("3. Withdraw")
          print("4. Transfer Money")
          print("5. Show Account Info")
          print("6. Transaction History")
          print("7. Delete Account")
          print("8. Logout\n")       
          
          account_option = input("Choose an option(1/2/3/4/5/6/7/8): ")
          if account_option == "1":
            account.view_balance()

          elif account_option == "2": 
            try:
             success = account.deposit(Decimal(input("\nEnter a value to deposit: ")),"deposit")
             if success:
              save_accounts()
             print("\nYour Balance :",account.balance)
            except InvalidOperation:
             print("\nInvalid Input!\n")  
              
          elif account_option == "3":   
            try:
             success = account.withdraw(Decimal(input("\nEnter a value to withdraw: ")),"withdraw")
             if success:
              save_accounts()
             print("\nYour Balance :",account.balance)
            except InvalidOperation:
              print("\nInvalid Input!\n") 

          elif account_option == "4":
            recipient_account_number = input("\nEnter recipient account number: ") 
            success = False
            if recipient_account_number in accounts:
              if recipient_account_number != account.account_number:
               recipient_account = accounts[recipient_account_number]
               try:
                transfer_amount = Decimal(input("\nEnter an amount to transfer: "))
                success = account.withdraw(transfer_amount,"transfer",recipient_account.account_number)
                print("\nYour Balance :",account.balance)
               except InvalidOperation:
                print("\nInvalid Input!\n")
               if success:
                recipient_account.deposit(transfer_amount,"transfer",account.account_number)
                save_accounts()
              else:
               print("\nFailed!You can't transfer money to yourself!\n") 
            else:
               print("\nThis account does not exist!\n")  
          elif account_option == "5":  
            account.show_info()

          elif account_option == "6":
            print("\n=== Transaction History ===\n")
            if not account.history:
              print("\nNo transactions yet!\n")
            else:  
             for transaction in account.history:
              print(transaction)
          
          elif account_option == "7":
            answer = input("\nAre you sure you want to delete this account?(yes/no)\n").lower()
            if answer == "yes":
             if account.balance > 0:
              print("\nyou can not delete your account!withdraw the money first!\n")
             else:
              del accounts[account_number]
              save_accounts()
              print("\nDeletion Is Done\n")
              break  
            elif answer == "no":
              pass
            else:
              print("Invalid Input!")     
                
            
          elif account_option == "8":
            break
          else:
            print("\nInvalid Option!")
      else:
        print("\nThis account does not exist,try again!")    
    elif option == "3":
      break  
    else:
      print("\nInvalid Option")