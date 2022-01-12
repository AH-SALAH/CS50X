from models.operations import OperationsModel
from flask import (
    render_template,
    session,
)
from helpers import apology, lookup
from time import sleep

class IndexController:

    def __init__(self):
        pass

    def index(self, db):
        """Show portfolio of stocks"""
        if session["user_id"]:
            
            try:
                owned = OperationsModel().get_user_custom_ownedshares(db, session["user_id"])
                # print("index-owned: ", owned)
                if not owned:
                    return apology("Then, You Have No Stocks!")
                
                # query the new data for every symbol 
                for row in owned:
                    lkup = lookup(row["symbol"])
                    
                    if lkup:
                        # add current data to the row
                        row["name"] = lkup["name"]
                        row["price"] = lkup["price"]
                        row["change"] = lkup["change"]
                        row["total"] = (lkup["price"] * row["shares"])
                    
                    sleep(1)

                totals = {"cash": owned[0]["cash"], "total_grand": 0}
                
                # total grand = cash + current total holding
                # add total holding to total grand
                for row in owned:
                    if row["total"]:
                        totals["total_grand"] += row["total"]
                
                # add cash on total grand
                totals["total_grand"] += totals["cash"]
                
                # print("index-owned: ", owned, totals)

                return render_template("index.html", owned=owned, totals=totals)

            except KeyError as er:
                print('An exception occurred', er)
                return apology("An exception occurred")
            except TypeError as er:
                print('An exception occurred', er)
                return apology("An exception occurred")

        return apology("Who The Hell You Are?!")
