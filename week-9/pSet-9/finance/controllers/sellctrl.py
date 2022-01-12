from flask import flash, session, render_template, redirect, url_for, request
from helpers import apology, lookup
from forms.sell import SellForm
from models.operations import OperationsModel
from models.users import UsersModel


class SellController:
    def __init__(self):
        pass

    def sell(self, db):
        """Sell shares of stock"""

        # see what shares we have
        data = OperationsModel().get_user_ownedshares(db, session["user_id"])

        # print("data-sell: ", data)

        # validate query
        form = SellForm()

        if not data:
            return apology("Sorry, You don't have any shares to sell! buy some first.")

        # if we got shares, then fill select options
        form.symbol.choices = [opt["symbol"] for opt in data]

        if request.method == "POST":

            if form.validate_on_submit():

                # query lookup
                lkup = lookup(form.symbol.data)

                if not lkup:
                    flash("No Data Found For This Stock", "info")

                    return render_template("sell.html", form=form)

                # Is shares sufficient?
                stock_price = lkup["price"]

                try:
                    # see what we owen from this symbol
                    owned = next(
                        filter(lambda row: row["symbol"] == lkup["symbol"], data)
                    )

                    number_owned = 0

                    # if no records then nothing there
                    if not owned:
                        return apology(
                            "You don't have any shares to sell! buy some first."
                        )

                    # bought_sum = owned[0]["bought_sum"] or 0
                    # sold_sum = owned[0]["sold_sum"] or 0
                    # print("owned-sell: ", owned, "bought-sell: ", bought_sum, "sold-sell: ", sold_sum)
                    print("owned-sell: ", owned["owned_shares"])

                    # if no bought then there is nothing to calc sell from
                    # if not bought_sum:
                    #     return apology("You don't have any shares to sell! buy some first.")

                    # number_owned += (bought_sum - sold_sum)
                    number_owned += owned["owned_shares"] - form.shares.data
                    # print("number_owned-sell: ", number_owned)

                    # if number of shares < 0 then apology
                    if number_owned < 0:
                        return apology("You can't sell this number of shares!")

                    # then, calc new cash
                    cash = owned["cash"] + (
                        float(stock_price) * float(form.shares.data)
                    )

                    # update user cash
                    UsersModel().update_user_cash(db, session["user_id"], cash)

                    # record in the table
                    OperationsModel().create_operation(
                        db,
                        user_id=session["user_id"],
                        symbol=lkup["symbol"],
                        price=stock_price,
                        change=lkup["change"],
                        number_of_shares=form.shares.data,
                        owned_shares=number_owned,
                        operation="sell",
                    )

                    # success
                    flash("Successfull Selling", "success")

                    # update session cash
                    session["user_cash"] = cash

                    return redirect(url_for("index"))

                except TypeError as er:
                    print("An exception occurred", er)
                    return render_template("sell.html", form=form)

        return render_template("sell.html", form=form)
