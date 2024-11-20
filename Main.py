from ModelNeighborhood import ModelNeighborhood
import psycopg
import datetime


def main():
    password = input("Input PostgreSQL password: ")
    model = ModelNeighborhood()
    with psycopg.connect("dbname=Pittsburgh_Neighborhoods user=postgres password=" + password + " host=localhost port=5432") as conn:
            with conn.cursor() as cur:
                print("Welcome to the Pittsburgh neighborhood dataset!")
                while True:
                    choice = int(input("Type 1 for the ethnic population ratio, 2 for getting the income per capita, 3 for comparing average retirement and self-employment incomes, 4 for inserting new data, and 0 exits: "))
                    if choice == 1:
                        print("Check the ethnic population ratio!")
                        model.population_race_ratio_query(cur)
                    if choice == 2:
                        print("Check the per capita income!")
                        model.per_capita_income_query(cur)
                    if choice == 3:
                        print("Compare retirement and self-emloyment incomes!")
                        model.population_retirement_vs_self_query(cur)
                    if choice == 4:
                         model.take_user_input()
                         model.insert_data(cur)
                    if choice == 0:
                         break
                    
                conn.commit()
                cur.close()
                conn.close()

if __name__=="__main__":   
    main()