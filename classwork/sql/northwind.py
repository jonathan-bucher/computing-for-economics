import sqlite3
import pandas as pd

name = ['jebucher']

con = sqlite3.connect(r"C:\Users\jonat\GSE 524\data\northwind.db") 

d1 = pd.read_sql_query("SELECT * FROM Orders WHERE ShipCountry = 'USA'", con)
# print(d1[:5])

d2 = pd.read_sql_query("SELECT DISTINCT ShipCountry FROM Orders", con)
# print(d2[:5])

d3 = pd.read_sql_query("SELECT ShipCountry, COUNT(CustomerId) AS Customers \
                       FROM Orders GROUP BY ShipCountry HAVING Customers > 0 \
                       ORDER BY Customers DESC", con)
# print(d3[:5])

d4 = pd.read_sql_query("SELECT Orders.Id FROM Orders JOIN Customer ON Customer.Id = Orders.CustomerId WHERE Customer.Country != Orders.ShipCountry", con)
# print(d4[:5])

d5 = pd.read_sql_query("SELECT Orders.Id, SUM((1 - OrderDetail.Discount) * OrderDetail.Quantity * OrderDetail.UnitPrice) AS Revenue FROM OrderDetail JOIN Orders \
                       ON Orders.ID = OrderDetail.OrderId \
                       GROUP BY OrderDetail.OrderId", con)
# print(d5[:5])

d6 = pd.read_sql_query("SELECT Orders.Id, Orders.OrderDate, Revenue FROM Orders NATURAL JOIN \
                       (SELECT Orders.Id, SUM((1 - OrderDetail.Discount) * OrderDetail.Quantity * OrderDetail.UnitPrice) AS Revenue FROM OrderDetail JOIN Orders \
                       ON Orders.ID = OrderDetail.OrderId \
                       GROUP BY OrderDetail.OrderId) \
                       JOIN Customer ON Customer.Id = Orders.CustomerId \
                       WHERE Customer.Country = 'USA'", con)
# print(d6[:5])

d7 = pd.read_sql_query("SELECT DISTINCT Customer.CompanyName FROM Orders JOIN Customer ON Customer.Id = Orders.CustomerId \
                       WHERE Orders.ShipCity = 'Eugene'", con)
# print(d7[:5])

d8 = pd.read_sql_query("SELECT DISTINCT CompanyName FROM \
                       (SELECT COUNT(Customer.CompanyName) AS Count, Customer.CompanyName FROM Orders JOIN Customer ON Customer.Id = Orders.CustomerId \
                       WHERE Orders.ShipCity = 'Eugene' GROUP BY Orders.ShipCity) \
                        WHERE Count > 1", con)
# print(d8)

con.close()

def orderlookup(city: str, country: str):

    # open connection
    con = sqlite3.connect(r"C:\Users\jonat\GSE 524\data\northwind.db") 

    df = pd.read_sql_query(f"SELECT * FROM Orders WHERE Orders.ShipCity = '{city}' AND Orders.ShipCountry = '{country}'", con)

    con.close()

    return df