from crew import stock_crew

if __name__ == "__main__":
    stock_name = input("Enter stock name or ticker: ")

    result = stock_crew.kickoff(
        inputs={"stock": stock_name}
    )

    print("\n" + "="*50)
    print("FINAL STOCK RESEARCH REPORT")
    print("="*50)
    print(result)
