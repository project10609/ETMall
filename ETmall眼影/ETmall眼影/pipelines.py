import pymysql

class EtmallPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect("projectdatabase.ccew5rh7vbmj.us-east-1.rds.amazonaws.com", "michael", "Baesuzy1", "Project")
        self.cursor = self.connection.cursor()
        #self.create_table()

    def process_item(self, item, spider):
        self.cursor.execute(
            "INSERT INTO Product(product_images, product_name, product_price, product_url, product_category,product_subcategory, product_source) VALUES (%s,%s, %s, %s, %s, %s, %s)",
            (item['product_images'], item['product_name'], item['product_price'], item['product_url'],
             item['product_category'],item['product_subcategory'],item['product_source']))
        self.connection.commit()
        return item

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE Product(product_images text, product_name varchar(512), product_price text, product_url text, product_category text,  product_subcategory text,product_source text)""")

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
