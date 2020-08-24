import csv
from re import sub
from decimal import Decimal
import operator

Categories = []
Merchant = []
Cost = []
num_purchases = 0
category_type = {"Dining Out", "Entertainment", "Groceries", "Miscellaneous", "Clothing", "Recreation"}
category_count = [0, 0, 0, 0, 0, 0, 0]
cost_spent_per_category = [0, 0, 0, 0, 0, 0, 0]
total_amount_spent = 0

def main():
    print("\nBanking Information Summary\n---------------------------------")
    parse_data()
    calculate_by_merchant()
    calculate_by_category()
    print(f'\nTotal spent this year: ${total_amount_spent}')

def parse_data():
    # parse through the data
    with open('yeardata.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            elif not row:
                line_count += 1
            else:
                Categories.append(row[0])
                Merchant.append(row[1].replace("SQ *", ""))
                Cost.append(row[2])

# Merchant Information
def calculate_by_merchant():
    print('\nTop 10 places I visited\n--------------------------------------')
    merchant_list = []
    for merchant in Merchant:
        if merchant not in merchant_list:
            merchant_list.append(merchant)
    merch_list_count = [0]*1000

    for entry in Merchant:
        for k, merch in enumerate(merchant_list):
            if entry == merch:
                merch_list_count[k] += 1
    merchant_dictionary = {}
    for i, merchant in enumerate(merchant_list):
        merchant_dictionary[merchant_list[i]] = merch_list_count[i]
    sorted_merchant_list = sorted(merchant_dictionary.items(), key=operator.itemgetter(1), reverse = True)

    with open('csv_file.csv', mode= 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',',lineterminator='\n', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for index, item in enumerate(sorted_merchant_list):
            if index < 10:
                print(f'You visited {item[0]} \t{item[1]} times')
                writer.writerow(item)

# Category Information
def calculate_by_category():
    global num_purchases
    global total_amount_spent
    for j, purchase in enumerate(Categories):
        num_purchases += 1
        for index, cat_type in enumerate(category_type):
            if purchase == cat_type:
                category_count[index] += 1

                value = Decimal(sub(r'[^\d.]', '', Cost[j]))
                cost_spent_per_category[index] += value
                total_amount_spent += value
    print("\nCategorical percentage breakdown\n---------------------------------")
    category_dictionary = {}
    for i, cat in enumerate(category_type):
        percent = round(category_count[i]/num_purchases * 100.0, 2)
        category_dictionary[cat] = percent
    sorted_categories = sorted(category_dictionary.items(), key=operator.itemgetter(1), reverse = True)
    for item in sorted_categories:
        print(f'{item[0]}: {item[1]}%')

    print('\nTotal spending by category\n---------------------------------')
    with open('expenses.csv', mode= 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        expense_dictionary = {}
        for i, cat in enumerate(category_type):
            expense = cost_spent_per_category[i]
            expense_dictionary[cat] = expense
        sorted_expenses = sorted(expense_dictionary.items(), key=operator.itemgetter(1), reverse = True)
        for item in sorted_expenses:
            print(f'{item[0]}: ${item[1]}')
            writer.writerow(item)

if __name__ == "__main__":
    main()