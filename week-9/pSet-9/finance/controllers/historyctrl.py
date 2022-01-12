from models.operations import OperationsModel
from flask import session, render_template, request
from helpers import apology
from math import ceil


class HistoryController:
    def __init__(self):
        self.operations_instance = OperationsModel()

    def history(self, db):
        """Show history of transactions"""
        if session["user_id"]:

            try:
                # pagination params
                pageSize = request.args.get("pageSize", type=int) or 10
                page = request.args.get("page", type=int) or 1
                orderBy = request.args.get("orderBy") or 'date'
                # start = request.args.get("start") or 0
                # end = request.args.get("end") or 0

                ttl = self.operations_instance.get_history_total_by_user(
                    db, session["user_id"]
                )

                if not ttl:
                    return apology("You Have No Stocks History Yet!")

                # print(
                #     "r-page: ",
                #     page,
                #     "r-pageSize: ",
                #     pageSize,
                #     "ttl",
                #     ttl,
                #     "view_args",
                #     request.args.get("page"),
                #     "ordrBy: ",
                #     orderBy
                # )                    

                log = self.operations_instance.get_paginated_user_history(
                    db, 
                    session["user_id"], 
                    page=page, 
                    pageSize=pageSize,
                    # orderBy=orderBy
                    # start=start, 
                    # end=end
                )

                if not log:
                    return apology("Nothing More!")
                
                # sort curret page rows
                # handle sorting here to avoid db returned total sorted list
                # which will be different than current page rows
                if bool(orderBy):
                    log.sort(reverse=True, key=lambda a: a[orderBy])

                log = {
                    "data": log,
                    "ttl": ttl[0]["count"],
                    "pages": ceil(ttl[0]["count"] / pageSize),
                    "currentPage": int(page),
                    "orderBy": orderBy,
                    "pageSize": pageSize
                    # "start": log[0]["id"],
                    # "end": log[-1]["id"],
                }

                # print(
                #     "data: ",
                #     log["data"],
                #     "ttl: ",
                #     log["ttl"],
                #     "pages: ",
                #     log["pages"],
                #     "currentPage: ",
                #     log["currentPage"],
                # )
                return render_template("history.html", log=log)

            except TypeError as er:
                print("An exception occurred", er)
                return apology("An exception occurred")

        return apology("Who The Hell You Are?!")
