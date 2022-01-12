from flask import flash, session, render_template, redirect, url_for
from helpers import apology, lookup
from forms.buy import BuyForm
from models.operations import OperationsModel
from models.users import UsersModel


class BuyController:
    def __init__(self):
        pass

    def buy(self, db):
        """Buy shares of stock"""

        # validate query
        form = BuyForm()
        if form.validate_on_submit():

            # create table if not exists
            try:
                OperationsModel().create_table(db)
            except TypeError as er:
                print("An exception occurred", er)
                return render_template("buy.html", form=form)

            # query lookup
            lkup = lookup(form.symbol.data)

            if not lkup:
                flash("No Data Found For This Stock", "info")

                return render_template("buy.html", form=form)

            # Is cash sufficient?
            stock_price = lkup["price"]

            row = UsersModel().select_from_user(db, session["user_id"], cash="cash")

            cash = row[0]["cash"] - (float(stock_price) * float(form.shares.data))
            if cash < 0:

                return apology("Your Current Cash Is Not Sufficient", 403)
                # flash("Sorry, Your Current Cash Is Not Sufficient", "danger")

                # return render_template("buy.html", form=form)

            try:
                # update user cash
                UsersModel().update_user_cash(db, session["user_id"], cash)
                kash = UsersModel().select_from_user(db, session["user_id"], cash="cash")

                # update session cash
                session["user_cash"] = kash[0]["cash"]

                # see what we owen
                owned = OperationsModel().calc_user_ownedshares(db, session["user_id"], lkup["symbol"], "sell", "buy")

                number_owned = int(form.shares.data)

                if owned:
                    bought_sum = owned[0]["bought_sum"] or 0
                    sold_sum = owned[0]["sold_sum"] or 0
                    # print("owned: ", owned, "bought: ", bought_sum, "sold_sum: ", sold_sum)

                    if bought_sum:
                        number_owned += bought_sum - sold_sum
                        # print("number_owned: ", number_owned)

                # record in the table
                OperationsModel().create_operation(
                    db,
                    user_id=session["user_id"],
                    symbol=lkup["symbol"],
                    price=stock_price,
                    change=lkup["change"],
                    number_of_shares=form.shares.data,
                    owned_shares=number_owned,
                    operation="buy",
                )

                # success
                flash("Successfull Purchase", "success")

                return redirect(url_for("index"))

            except TypeError as er:
                print("An exception occurred", er)
                return render_template("buy.html", form=form)

        return render_template("buy.html", form=form)
