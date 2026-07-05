from utils import get_model_from_gcp



def main():
    llm=get_model_from_gcp()
    result=llm.invoke("how rag working!")
    result.pretty_print()


if __name__ == "__main__":
    main()
