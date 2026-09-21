import json
import random
import string
from pathlib import Path


class Bank:
    database = "data.json"
    data = []
    try:
        if Path(database).exists():

            with open(database) as fs:
                data = json.loads(fs.read())
        else:
            print("no such file exists")
    except Exception as err:
        print(f"an exception occured as {err}")

    @classmethod
    def __update(cls):
        with open(Bank.database, "w") as fs:
            fs.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        id = alpha + num + spchar
        random.shuffle(id)
        account_no = "".join(id)

        while any(i["accountNo"] == account_no for i in Bank.data):
            random.shuffle(id)
            account_no = "".join(id)
        
        return account_no

    def createaccount(self):
        info = {
            "name": input("Enter Your Name :-"),
            "age": int(input("Enter Your Age :-")),
            "email": input("Enter Your Email :-"),
            "pin": int(input("Create A 4 Digit Pin :-")),
            "accountNo": Bank.__accountgenerate(),
            "balance": 0,
        }
        if info["age"] < 18 or not (1000 <= info["pin"] <= 9999):
            print("Sorry YOU Cannot Create Account ")
        else:
            print("Account Has Been Created Succesfully.")
            for i in info:
                print(f"{i} : {info[i]}")
            print("Please Note Down Your Account Number.")
            Bank.data.append(info)
            Bank.__update()

    def depositmoney(self):
        accnumber = input("Please Provide Your Account Number :-")
        pin = int(input("Please Provide Your Pin :-"))
        userdata = [
            i for i in Bank.data if i["accountNo"] == accnumber and i["pin"] == pin
        ]

        if not userdata:
            print("Sorry No Such Data Found.")
        else:
            amount = int(input("ENTER Amount For Deposit :-"))
            if amount > 10000 or amount <= 0:
                print(
                    "Sorry The Amount Is Too Much U Can Deposit Below And Above Zero."
                )
            else:
                userdata[0]["balance"] += amount
                Bank.__update()
                print("Your Amount Successfully Deposited.")

    def withdrawmoney(self):
        accnumber = input("Please Provide Your Account Number :-")
        pin = int(input("Please Provide Your Pin :-"))
        userdata = [
            i for i in Bank.data if i["accountNo"] == accnumber and i["pin"] == pin
        ]

        if not userdata:
            print("Sorry No Such Data Found.")
        else:
            amount = int(input("ENTER Amount For Withdraw :-"))
            if amount <= 0:
                print("Please Enter A Valid Amount.")
            elif userdata[0]["balance"] < amount:
                print("Sorry You Dont Have That Much Money.")
            else:
                userdata[0]["balance"] -= amount
                Bank.__update()
                print("Your Amount Successfully Withdraw.")

    def showdetails(self):
        accnumber = input("Please Provide Your Account Number :-")
        pin = int(input("Please Provide Your Pin :-"))
        userdata = [
            i for i in Bank.data if i["accountNo"] == accnumber and i["pin"] == pin
        ]
        if not userdata:
            print("Sorry No Such Data Found.")
        else:
            print("Your Information Are \n\n\n")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")

    def updatedetails(self):
        accnumber = input("Please Provide Your Account Number :-")
        pin = int(input("Please Provide Your Pin :-"))
        userdata = [
            i for i in Bank.data if i["accountNo"] == accnumber and i["pin"] == pin
        ]
        if not userdata:
            print("Sorry No Such Data Found.")
        else:
            print("You Cannot Change The Age , Account Number , Balance.")

            print("Fill The Details For Change or Leave It Empty If No Change.")

            newdata = {
                "name": input("Please Provide New Name Or Press Enter To Skip :-"),
                "email": input("Please Provide New Email Or Press Enter To Skip :-"),
                "pin": input("Please Provide New Pin Or Press Enter To Skip :-"),
            }
            if newdata["name"] == "":
                newdata["name"] = userdata[0]["name"]
            if newdata["email"] == "":
                newdata["email"] = userdata[0]["email"]
            if newdata["pin"] == "":
                newdata["pin"] = userdata[0]["pin"]
            newdata["age"] = userdata[0]["age"]
            newdata["balance"] = userdata[0]["balance"]
            newdata["accountNo"] = userdata[0]["accountNo"]

            if type(newdata["pin"]) == str:
                newdata["pin"] = int(newdata["pin"])
            
            if len(str(newdata["pin"])) != 4:
                print("PIN Must Be 4 Digits.")
                return
            for i in newdata:
                if newdata[i] == userdata[0][i]:
                    continue
                else:
                    userdata[0][i] = newdata[i]

            Bank.__update()
            print("Your Details Is Updated Successfully.")

    def delete(self):
        accnumber = input("Please Provide Your Account Number :-")
        pin = int(input("Please Provide Your Pin :-"))
        userdata = [
            i for i in Bank.data if i["accountNo"] == accnumber and i["pin"] == pin
        ]
        if not userdata:
            print("Sorry No Such Data Found.")
        else:
            check = input(
                "Press Y If You Actually Want To Delete Your Account or Press n."
            )
            if check.lower() == "y":
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Your Account Delete Successfully")
                Bank.__update()
            else:
                print("Account Deletion Cancelled.")


user = Bank()


print("PRESS 1 FOR CREATING A ACCOUNT")
print("PRESS 2 FOR DEPOSIT MONEY")
print("PRESS 3 FOR WITHDRAW MONEY")
print("PRESS 4 FOR DETAILS")
print("PRESS 5 FOR UPDATE DETAILS")
print("PRESS 6 FOR DELETE ACCOUNT")

check = int(input("ENTER YOUR RESPONSE:-"))

if check == 1:
    user.createaccount()
if check == 2:
    user.depositmoney()
if check == 3:
    user.withdrawmoney()
if check == 4:
    user.showdetails()
if check == 5:
    user.updatedetails()
if check == 6:
    user.delete()
