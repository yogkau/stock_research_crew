from crew import stock_crew
from cache import get_cached, save_cache


if __name__ == "__main__":
    stock_name = input("Enter stock name or ticker: ")

    # Check cache: avoid re-running expensive agent pipeline for same stock
    cached = get_cached(stock_name)
    if cached:
        print("Using cached result (fast).")
        print("\n" + "="*50)
        print("FINAL STOCK RESEARCH REPORT")
        print("="*50)
        print(cached.get("result") if isinstance(cached, dict) else cached)
    else:
        result = stock_crew.kickoff(
            inputs={"stock": stock_name}
        )

        out = str(result)
        save_cache(stock_name, out)

        print("\n" + "="*50)
        print("FINAL STOCK RESEARCH REPORT")
        print("="*50)
        print(result)
