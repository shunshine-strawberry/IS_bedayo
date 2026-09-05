import clips
import os

env = clips.Environment()

base_dir = os.path.dirname(os.path.abspath(__file__))
clips_file = os.path.join(base_dir, "loan.CLP")

env.load(clips_file)

print("\n===== LOAN ANALYSIS =====\n")

name = input("Name: ")
age = int(input("Age: "))
employment = input("Employed? (yes/no): ").lower()
income = int(input("Monthly Income: "))
credit = input("Credit (poor/average/good): ").lower()
loan_amount = int(input("Loan Amount Requested: "))

applicant = f'''
(applicant
   (name "{name}")
   (age {age})
   (employment {employment})
   (income {income})
   (credit {credit})
   (loan-amount {loan_amount})
)
'''

env.reset()
env.assert_string(applicant)

env.run()