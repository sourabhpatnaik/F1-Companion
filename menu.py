from f1_features import get_next_race, get_current_Driverstanding, get_full_seasonSchedule,get_DriverDetails,get_constructor_standings,get_fullRacesession_Info,recentRaceResult
from tabulate import tabulate

# Cache variable
driver_standings_cache = None

def main_menu():
    global driver_standings_cache

    while True:
        print("\n============================")
        print("   F1 CLI Companion 🏎️")
        print("============================")
        print("1. Show Upcoming Race")
        print("2. Show Current Driver Standings")
        print("3. Show Full Year Schedule")
        print("4. Show Driver Detail")
        print("5. Show Current Constructor Standings")
        print("6. Show Full Race Session Schedule")
        print("7. Show Last Race Result")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("\n" + get_next_race())
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            if driver_standings_cache is None:
                print("\nLoading standings... (first time may take ~10s)")
                driver_standings_cache = get_current_Driverstanding()

            print(driver_standings_cache)
            input("\nPress Enter to return to menu...")

        elif choice == "3":
            print(get_full_seasonSchedule())
        
        elif choice == "4":
            print(get_DriverDetails())
        
        elif choice == "5":
            print(get_constructor_standings())
        
        elif choice == "6":
            print(get_fullRacesession_Info())

        elif choice == "7":
            print("\nLAST RACE RESULT:")
            print(recentRaceResult())

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
