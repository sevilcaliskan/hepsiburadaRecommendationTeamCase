# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import json
import argparse

sameCart = pd.read_csv('C:\\Users\\User\\Desktop\\hepsiburada\\data\\product_90pct.txt',
                       encoding='utf-8',
                       sep=";")
similar = pd.read_csv('C:\\Users\\User\\Desktop\\hepsiburada\\data\\all_categories_backup.txt',
                      encoding='utf-8',
                      sep=";")
f = open('C:\\Users\\User\\Desktop\\hepsiburada\\data\\meta.json', encoding='utf-8')
meta = json.load(f)
pd.DataFrame(meta)
meta = pd.json_normalize(meta, record_path=['meta'])


def findFirst10(product):
    df_1 = sameCart[sameCart.Product_A == product].sort_values(by='Lift', ascending=False).head(10)[
        ['Product_A', 'Product_B', 'Lift']]
    df_1 = df_1.rename(columns={'Product_A': 'Input_Product', 'Product_B': 'productid'})
    df_2 = sameCart[sameCart.Product_B == product].sort_values(by='Lift', ascending=False).head(10)[
        ['Product_B', 'Product_A', 'Lift']]
    df_2 = df_2.rename(columns={'Product_B': 'Input_Product', 'Product_A': 'productid'})
    most = pd.concat([df_1, df_2], ignore_index=True)
    most.drop_duplicates(subset="productid", keep='first', inplace=True)
    return most.head(10)


def findFirst10Cart(productList):
    topten = pd.DataFrame()
    for i in productList:
        topten1 = findFirst10(i)
        topten1 = topten1[~topten1.productid.isin(productList)]
        topten = pd.concat([topten, topten1], ignore_index=True)
    topten = topten.sort_values(by='Lift', ascending=False)
    topten.drop_duplicates(subset="productid", keep='first', inplace=True)
    return topten.head(10)


def productsAndScores(productList):
    topten = findFirst10Cart(productList)
    result = pd.merge(topten, meta[meta.productid.isin(topten.productid)][['productid', 'name']], on="productid")
    result = pd.merge(result, meta[meta.productid.isin(topten.Input_Product)][['productid', 'name']],
                      left_on='Input_Product', right_on='productid')
    return result[['Input_Product', 'productid_x', 'name_y', 'name_x', 'Lift']]


def findFirst10_sim(product):
    df_1 = similar[similar.Product_A_id == product].sort_values(by='Similarity', ascending=False).head(10)[
        ['Product_A_id', 'Product_B', 'Similarity']]
    df_1 = df_1.rename(columns={'Product_A_id': 'Product', 'Product_B': 'similar_Product'})
    df_2 = similar[similar.Product_B == product].sort_values(by='Similarity', ascending=False).head(10)[
        ['Product_B', 'Product_A_id', 'Similarity']]
    df_2 = df_2.rename(columns={'Product_B': 'Product', 'Product_A_id': 'similar_Product'})
    most = pd.concat([df_1, df_2], ignore_index=True)
    most.drop_duplicates(subset="similar_Product", keep='first', inplace=True)
    return most.head(10)


def findFirst10Cart_sim(productList):
    topten = pd.DataFrame()
    for i in productList:
        topten1 = findFirst10_sim(i)
        topten1 = topten1[~topten1.similar_Product.isin(productList)]
        topten = pd.concat([topten, topten1], ignore_index=True)
    topten = topten.sort_values(by='Similarity', ascending=False)
    topten.drop_duplicates(subset="similar_Product", keep='first', inplace=True)
    return topten.head(10)


def productsAndScores_sim(productList):
    topten = findFirst10Cart_sim(productList)
    result = pd.merge(topten, meta[meta.productid.isin(topten.Product)][['productid', 'name']], left_on="Product",
                      right_on="productid")
    result = pd.merge(result, meta[meta.productid.isin(topten.similar_Product)][['productid', 'name']],
                      left_on='similar_Product', right_on='productid')
    return result[['Product', 'productid_y', 'name_x', 'name_y', 'Similarity']]


def printOutput(productList):
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print("Products in the list are: ")
        print(meta[meta.productid.isin(productList)])
        print("Products usually put in the cart together: ")
        print(productsAndScores(productList))
        print("Similar products: ")
        print(productsAndScores_sim(productList))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments for the cart as a list')
    parser.add_argument("--c", default=1, type=str, help="This is the list of products in the cart")
    args = parser.parse_args()
    cart = args.c.split(",")
    printOutput(cart)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
