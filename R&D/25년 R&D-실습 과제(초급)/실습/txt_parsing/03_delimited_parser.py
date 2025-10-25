"""
[*] [*] [*] [*] [*] [*]

[*] [*] CSV, TSV, [*](|) [*] [*] [*] [*] [*] [*] [*] [*] [*] [*].

[*] [*]:
1. [*] [*] [*] [*] [*]
2. [*] [*]/[*] [*] [*]
3. [*] [*] [*] [*] [*]
"""

import os
import csv
from typing import List, Dict, Optional


class DelimitedFileParser:
    """
    [*] [*] [*] [*] [*] [*]

    [*] [*]:
        - CSV (Comma-Separated Values): [*](,) [*]
        - TSV (Tab-Separated Values): [*](\\t) [*]
        - PSV (Pipe-Separated Values): [*](|) [*]
        - [*] [*] [*]
    """

    def __init__(self, delimiter='|', has_header=True, encoding='utf-8'):
        """
        [*] [*]

        Args:
            delimiter (str): [*] [*] ([*]: '|')
            has_header (bool): [*] [*] [*] [*] ([*]: True)
            encoding (str): [*] [*] ([*]: 'utf-8')
        """
        self.delimiter = delimiter
        self.has_header = has_header
        self.encoding = encoding

        # [*] [*]
        self.total_rows = 0
        self.valid_rows = 0
        self.invalid_rows = 0

    def parse_simple(self, file_path) -> List[List[str]]:
        """
        [*] 2[*] [*] [*] ([*] [*] [*])

        Args:
            file_path (str): [*] [*]

        Returns:
            List[List[str]]: [*] [*] [*] [*] 2[*] [*]

        [*]:
            [
                ['[*]', '30', '[*]'],
                ['[*]', '25', '[*]']
            ]
        """
        data = []

        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                # [*] [*] [*]
                if self.has_header:
                    header = f.readline()
                    print(f"[LIST] [*]: {header.strip()}")

                # [*] [*]
                for line in f:
                    # [*] [*] [*]
                    if not line.strip():
                        continue

                    # [*] [*]
                    fields = line.strip().split(self.delimiter)
                    data.append(fields)

            self.total_rows = len(data)
            print(f"[OK] {self.total_rows}[*] [*] [*].")
            return data

        except Exception as e:
            print(f"[ERROR] [*] [*]: {e}")
            return []

    def parse_to_dict(self, file_path) -> List[Dict[str, str]]:
        """
        [*] [*] [*] [*] ([*] [*])

        Args:
            file_path (str): [*] [*]

        Returns:
            List[Dict[str, str]]: [*] [*] [*] [*] [*]

        [*]:
            [
                {'[*]': '[*]', '[*]': '30', '[*]': '[*]'},
                {'[*]': '[*]', '[*]': '25', '[*]': '[*]'}
            ]
        """
        if not self.has_header:
            print("[WARN]  [*]: [*] [*] [*] [*] [*] [*] [*].")
            return []

        data = []

        try:
            with open(file_path, 'r', encoding=self.encoding) as f:
                # [*] [*]
                header_line = f.readline().strip()
                headers = header_line.split(self.delimiter)

                print(f"[LIST] [*]: {headers}")

                # [*] [*]
                for line_num, line in enumerate(f, start=2):  # [*] [*]
                    if not line.strip():
                        continue

                    fields = line.strip().split(self.delimiter)

                    # [*] [*] [*] [*] [*] [*]
                    if len(fields) != len(headers):
                        print(f"[WARN]  [*] {line_num}: [*] [*] [*] "
                              f"([*]: {len(headers)}, [*]: {len(fields)})")
                        self.invalid_rows += 1
                        continue

                    # [*] [*] [*] [*] [*]
                    row_dict = dict(zip(headers, fields))
                    data.append(row_dict)
                    self.valid_rows += 1

            self.total_rows = self.valid_rows + self.invalid_rows
            print(f"[OK] [*] {self.total_rows}[*] [*] [*] {self.valid_rows}[*] [*] [*]")

            return data

        except Exception as e:
            print(f"[ERROR] [*] [*]: {e}")
            return []

    def parse_with_types(self, file_path, type_map: Dict[str, type]) -> List[Dict]:
        """
        [*] [*] [*] [*] ([*] [*] [*])

        Args:
            file_path (str): [*] [*]
            type_map (Dict[str, type]): {'[*]': [*]} [*] [*] [*]

        Returns:
            List[Dict]: [*] [*] [*] [*]

        [*]:
            type_map = {
                '[*]': str,
                '[*]': int,
                '[*]': float,
                '[*]': str
            }
        """
        # [*] [*] [*]
        raw_data = self.parse_to_dict(file_path)

        if not raw_data:
            return []

        # [*] [*]
        typed_data = []

        for row_num, row in enumerate(raw_data, start=2):
            typed_row = {}

            try:
                for field, value in row.items():
                    # [*] [*] [*] [*], [*] [*] [*]
                    if field in type_map:
                        target_type = type_map[field]

                        # None[*] [*] [*] [*]
                        if not value or value.strip() == '':
                            typed_row[field] = None
                        else:
                            # [*] [*] [*]
                            typed_row[field] = target_type(value.strip())
                    else:
                        typed_row[field] = value

                typed_data.append(typed_row)

            except ValueError as e:
                print(f"[WARN]  [*] {row_num}: [*] [*] [*] - {e}")
                continue

        print(f"[OK] {len(typed_data)}[*] [*] [*] [*] [*]")
        return typed_data

    def validate_data(self, data: List[Dict], rules: Dict) -> List[Dict]:
        """
        [*] [*] [*] [*]

        Args:
            data (List[Dict]): [*] [*]
            rules (Dict): [*] [*]
                [*]: {
                    '[*]': lambda x: 0 <= x <= 150,
                    '[*]': lambda x: '@' in x
                }

        Returns:
            List[Dict]: [*] [*] [*]
        """
        valid_data = []

        for row_num, row in enumerate(data, start=2):
            is_valid = True

            for field, validator in rules.items():
                if field in row:
                    try:
                        if not validator(row[field]):
                            print(f"[WARN]  [*] {row_num}: '{field}' [*] [*] - [*]: {row[field]}")
                            is_valid = False
                            break
                    except Exception as e:
                        print(f"[WARN]  [*] {row_num}: '{field}' [*] [*] [*] - {e}")
                        is_valid = False
                        break

            if is_valid:
                valid_data.append(row)

        print(f"[OK] [*] [*]: {len(valid_data)}/{len(data)}[*] [*]")
        return valid_data

    def save_to_csv(self, data: List[Dict], output_path: str):
        """
        [*] [*] CSV [*] [*]

        Args:
            data (List[Dict]): [*] [*]
            output_path (str): [*] [*] [*]
        """
        if not data:
            print("[WARN]  [*] [*] [*].")
            return

        try:
            # [*] [*] ([*] [*] [*] [*])
            fieldnames = list(data[0].keys())

            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # [*] [*]
                writer.writeheader()

                # [*] [*]
                writer.writerows(data)

            print(f"[OK] CSV [*] [*] [*]: {output_path}")

        except Exception as e:
            print(f"[ERROR] CSV [*] [*]: {e}")


def create_sample_files():
    """
    [*] [*] [*] [*]
    """
    os.makedirs("data", exist_ok=True)

    # 1. Pipe-separated user data file
    users_file = "data/sample_users.txt"
    users_data = """name|age|address|phone|join_date
Kim|30|Seoul|010-1234-5678|2023-01-15
Lee|25|Busan|010-2345-6789|2023-03-20
Park|28|Incheon|010-3456-7890|2023-05-10
Choi|35|Daegu|010-4567-8901|2023-02-28
Jung|32|Daejeon|010-5678-9012|2023-04-05
"""
    with open(users_file, 'w', encoding='utf-8') as f:
        f.write(users_data)
    print(f"[OK] Created sample file: {users_file}")

    # 2. CSV product data file
    products_file = "data/sample_products.csv"
    products_data = """product_name,price,stock,category,rating
Laptop,1500000,50,Electronics,4.5
Keyboard,25000,200,Accessories,4.2
Mouse,75000,150,Accessories,4.7
Monitor,350000,80,Electronics,4.6
Headphones,200000,30,Accessories,4.3
Webcam,150000,45,Electronics,4.4
"""
    with open(products_file, 'w', encoding='utf-8') as f:
        f.write(products_data)
    print(f"[OK] Created sample file: {products_file}")

    # 3. TSV order data file
    orders_file = "data/sample_orders.tsv"
    orders_data = """order_id\tcustomer\tproduct\tquantity\tamount\torder_date
ORD-001\tKim\tLaptop\t1\t1500000\t2025-10-01 10:30:00
ORD-002\tLee\tMouse\t3\t75000\t2025-10-02 14:20:00
ORD-003\tPark\tWebcam\t2\t150000\t2025-10-03 09:15:00
ORD-004\tChoi\tMonitor\t1\t350000\t2025-10-04 16:45:00
ORD-005\tJung\tHeadphones\t1\t200000\t2025-10-05 11:00:00
"""
    with open(orders_file, 'w', encoding='utf-8') as f:
        f.write(orders_data)
    print(f"[OK] Created sample file: {orders_file}")


def main():
    """
    [*] [*]: [*] [*] [*] [*] [*]
    """
    print("=" * 60)
    print("[*] [*] [*] [*] [*] [*]")
    print("=" * 60)

    # [*] [*] [*]
    sample_files = ["data/sample_users.txt", "data/sample_products.csv", "data/sample_orders.tsv"]
    if not os.path.exists("data") or not all(os.path.exists(f) for f in sample_files):
        print("\n[INFO] [*] [*] [*]...\n")
        create_sample_files()

    # ===== 1. [*](|) [*] [*] [*] =====
    print("\n" + "=" * 60)
    print("1. [*](|) [*] [*] [*]")
    print("=" * 60)

    parser = DelimitedFileParser(delimiter='|', has_header=True)
    users = parser.parse_to_dict("data/sample_users.txt")

    if users:
        print("\nFirst 3 users:")
        for user in users[:3]:
            print(f"  - {user['name']} ({user['age']} years old, {user['address']})")

    # ===== 2. CSV [*] [*] ([*] [*]) =====
    print("\n" + "=" * 60)
    print("2. CSV [*] [*] ([*] [*] [*])")
    print("=" * 60)

    csv_parser = DelimitedFileParser(delimiter=',', has_header=True)

    # Define type mapping for product fields
    product_types = {
        'product_name': str,
        'price': int,
        'stock': int,
        'category': str,
        'rating': float
    }

    products = csv_parser.parse_with_types("data/sample_products.csv", product_types)

    if products:
        print("\nProduct list:")
        for prod in products:
            name = str(prod['product_name']) if 'product_name' in prod else 'Unknown'
            price = prod.get('price', 0)
            stock = prod.get('stock', 0)
            rating = prod.get('rating', 0)
            print(f"  - {name:15s}: "
                  f"{price:,} won (stock: {stock}, rating: {rating})")

        # Calculate total inventory value
        total_value = sum(p['price'] * p['stock'] for p in products)
        print(f"\n  [STATS] Total inventory value: {total_value:,} won")

    # ===== 3. TSV [*] [*] [*] [*] =====
    print("\n" + "=" * 60)
    print("3. TSV [*] [*] [*] [*] [*]")
    print("=" * 60)

    tsv_parser = DelimitedFileParser(delimiter='\t', has_header=True)

    # Define type mapping for order fields
    order_types = {
        'order_id': str,
        'customer': str,
        'product': str,
        'quantity': int,
        'amount': int,
        'order_date': str
    }

    orders = tsv_parser.parse_with_types("data/sample_orders.tsv", order_types)

    # Define validation rules
    validation_rules = {
        'quantity': lambda x: x > 0 and x <= 100,  # quantity 1-100
        'amount': lambda x: x > 0,                 # amount must be positive
    }

    valid_orders = tsv_parser.validate_data(orders, validation_rules)

    if valid_orders:
        print("\nValid orders list:")
        for order in valid_orders:
            print(f"  - {order['order_id']}: {order['customer']} - "
                  f"{order['product']} x{order['quantity']} = {order['amount']:,} won")

    # ===== 4. [*] [*] [*] [*] =====
    print("\n" + "=" * 60)
    print("4. [*] [*] [*] CSV [*]")
    print("=" * 60)

    # Add age group field to users
    if users:
        for user in users:
            age = int(user['age'])
            if age < 30:
                user['age_group'] = '20s'
            elif age < 40:
                user['age_group'] = '30s'
            else:
                user['age_group'] = '40s+'

        # Save as CSV
        csv_parser.save_to_csv(users, "data/users_with_age_group.csv")

    # ===== 5. [*] [*] =====
    print("\n" + "=" * 60)
    print("5. [*] [*]")
    print("=" * 60)

    if users:
        print(f"\n[>] User statistics:")
        print(f"  - Total users: {len(users)}")

        ages = [int(u['age']) for u in users]
        print(f"  - Average age: {sum(ages) / len(ages):.1f} years")
        print(f"  - Youngest: {min(ages)} years")
        print(f"  - Oldest: {max(ages)} years")

    if products:
        print(f"\n[>] Product statistics:")
        print(f"  - Total products: {len(products)}")

        total_stock = sum(p['stock'] for p in products)
        print(f"  - Total stock: {total_stock:,} items")

        avg_price = sum(p['price'] for p in products) / len(products)
        print(f"  - Average price: {avg_price:,.0f} won")

    if valid_orders:
        print(f"\n[>] Order statistics:")
        print(f"  - Valid orders: {len(valid_orders)}")

        total_revenue = sum(o['amount'] for o in valid_orders)
        print(f"  - Total revenue: {total_revenue:,} won")

        total_items = sum(o['quantity'] for o in valid_orders)
        print(f"  - Total items ordered: {total_items}")

    print("\n" + "=" * 60)
    print("[*] [*]!")
    print("=" * 60)

    print("\n[TIP] [*] [*] [*]:")
    print("  1. pandas [*] [*] [*] [*]")
    print("  2. [*] [*] (matplotlib, seaborn)")
    print("  3. [*] [*] [*] [*] [*] [*]")
    print("  4. Excel [*] [*]/[*] (openpyxl)")


if __name__ == "__main__":
    main()
