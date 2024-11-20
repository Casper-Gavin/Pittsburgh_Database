import psycopg
import datetime



class ModelNeighborhood:    
    def __init__(self):
        self.dataList = []
        self.neighborhood = ''
        self.id = 0
        self.income = ''
        self.margin_error = 0
        self.total_pop = ''
        self.margin_error_total = 0
        self.white_only_population = 1
        self.black_only_population = 1
        self.total_income = 1
        self.retirement_income = 1
        self.no_retirement_income = 1
        self.with_self_income = 1
        self.no_self_income = 1


    # individual population / total population for a neighborhood
    def population_race_ratio_query(self, cur):
        # white ratio
        queryLine2 = """SELECT total_population.neighborhood,
                race_income.white_only_population / total_population.total_pop AS white_population_ratio
                FROM total_population
                JOIN race_income ON total_population.id = race_income.id
                WHERE total_population.id = %s;"""
        
        # black ratio
        queryLine1 = """
                SELECT total_population.neighborhood,
                race_income.black_only_population / total_population.total_pop AS black_population_ratio
                FROM total_population
                JOIN race_income ON total_population.id = race_income.id
                WHERE total_population.id = %s;"""
        
        id = int(input("Choose a neighborhood id (between 1 and 91 approximately): "))
        ethnicity = input("Type 1 for black ratio or 2 for white ratio: ")

        if ethnicity == '2':
            cur.execute(queryLine2, (id,))
        if ethnicity == '1':
            cur.execute(queryLine1, (id,))
        self.dataList = cur.fetchall()
        print(self.dataList)
    
    # income per capita for a neighborhood
    def per_capita_income_query(self, cur):
        queryLine = """
            SELECT a.neighborhood_name,
            a.income / p.total_pop AS income_per_capita
            FROM aggregate_income a
            JOIN total_population p ON a.id_name = p.id
            WHERE a.id_name = %s;"""
        
        id = int(input("Choose a neighborhood id (between 1 and 91 approximately): "))

        cur.execute(queryLine, (id,))
        self.dataList = cur.fetchall()
        print(self.dataList)

    # comparison (-) between retirement and self employment income
    def population_retirement_vs_self_query(self, cur):
        id = int(input("Choose a neighborhood id (between 1 and 91 approximately): "))
        cur.execute("""
            SELECT r.neighborhood, r.retirement_income - s.with_self_income AS income_difference
            FROM retirement_income r
            JOIN self_employment_income s ON r.id = s.id
            WHERE r.id = %s;""", (id,)) # adding ',' after id makes the program work; gets rid of int has no attribute len error
        
        self.dataList = cur.fetchall()
        print(self.dataList)


    def insert_aggregate_income(self, cur):
        cur.execute("""
            INSERT INTO aggregate_income (neighborhood_name, id_name, income, margin_error)
            VALUES (%s, %s, %s, %s)
            """, (self.neighborhood, self.id, self.income, self.margin_error))
        
    def insert_total_population(self, cur):
        cur.execute("""
            INSERT INTO total_population (neighborhood, id, total_pop, margin_error_total)
            VALUES (%s, %s, %s, %s)
            """, (self.neighborhood, self.id, self.total_pop, self.margin_error_total))
        
    def insert_race_income(self, cur):
        cur.execute("""
            INSERT INTO race_income (neighborhood, id, population, white_only_population, black_only_population)
            VALUES (%s, %s, %s, %s, %s)
            """, (self.neighborhood, self.id, self.total_pop, self.white_only_population, self.black_only_population))
    
    def insert_retirement_income(self, cur):
        cur.execute("""
            INSERT INTO retirement_income (neighborhood, id, total_income, retirement_income, no_retirement_income)
            VALUES (%s, %s, %s, %s, %s)
            """, (self.neighborhood, self.id, self.total_income, self.retirement_income, self.no_retirement_income))
        
    def insert_self_employment_income(self, cur):
        cur.execute("""
            INSERT INTO self_employment_income (neighborhood, id, total_income, with_self_income, no_self_income)
            VALUES (%s, %s, %s, %s, %s)
            """, (self.neighborhood, self.id, self.total_income, self.with_self_income, self.no_self_income))
        
    def insert_data(self, cur):
        self.insert_aggregate_income(cur)
        self.insert_total_population(cur)
        self.insert_race_income(cur)
        self.insert_retirement_income(cur)
        self.insert_self_employment_income(cur)
        

    def take_user_input(self):
        self.neighborhood = input("Give the new neighborhood name (str): ")
        self.id = int(input("Give the id (int): "))
        self.income = float(input("Give the aggregate income (float): "))
        self.margin_error = float(input("Give the margin of error (float): "))
        self.total_pop = float(input("Give the total population (int): "))
        self.margin_error_total = float(input("Give the total margin of error (float): "))
        self.white_only_population = float(input("Give the white population (int): "))
        self.black_only_population = float(input("Give the black population (int): "))
        self.total_income = float(input("Give the total income (float): "))
        self.retirement_income = float(input("Give the retirement income portion (float): "))
        self.no_retirement_income = float(input("Give the no retirement income portion (float): "))
        self.with_self_income = float(input("Give the self employment income portion (float): "))
        self.no_self_income = float(input("Give the no self employment income portion (float): "))
