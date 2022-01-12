from flask import flash, render_template, request
from helpers import apology, lookup


class QuoteController:
    def __init__(self):
        pass

    def quote(self):
        """Get stock quote."""

        if request.method == "POST":
            symbol = request.form.get("symbol")

            if not symbol:
                flash("please, write a stock symbol", "warning")
                return render_template("quote.html")

            data = lookup(symbol)
            error = ""

            if not data:
                error = "No data found"
                return apology("NO Data Found")

            return render_template("quote.html", data=data, error=error)

        else:
            return render_template("quote.html")