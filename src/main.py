from textnode import TextType, TextNode

def main():
    work = TextNode("Bob was Here", TextType.bold, "www.bob.com")
    print(work)


if __name__ == "__main__":
    main()
