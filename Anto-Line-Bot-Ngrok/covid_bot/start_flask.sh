#!/usr/bin/bash

export LINE_CHANNEL_SECRET="7ea429370d4067dedc898531df9c3f1f"
export LINE_CHANNEL_ACCESS_TOKEN="eINJlmnTm6Rowb6MAXseQzmKSniHBwYBn0dLZduj7d452Zt5RzkteCRxcbbTnfdXkfqeSAHZT/m0aaG7QOhK2VDaLG8PgxaqutcMXlHoTu13vX086cTZL7r9a/faiteAp95OP1wSj0U3LB/QCDs3YAdB04t89/1O/w1cDnyilFU="
export USE_NGROK=True
export FLASK_ENV=development
export FLASK_APP=app.py
flask run
