from visualization.visualizer import user_input, infinite_well, finite_well, compare_wells, animate_superposition

def main():
    params = user_input()
    
    while True:
        print("\nQuantumBox Menu:")
        print("1. Plot Infinite Square Well")
        print("2. Plot Finite Square Well")
        print("3. Compare Wells")
        print("4. Animate Superposition")
        print("5. Change Parameters")
        print("6. Exit")
        
        choice = input("\nSelect option [1-6]: ").strip()
        
        if choice == '1':
            infinite_well(params)
        elif choice == '2':
            finite_well(params)
        elif choice == '3':
            compare_wells(params)
        elif choice == '4':
            animate_superposition(params)
        elif choice == '5':
            params = user_input()
        elif choice == '6':
            print("Exiting QuantumBox...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()