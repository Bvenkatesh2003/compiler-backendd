import sys

def main():
    code = sys.stdin.read()
    try:
        exec(code, {})
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
