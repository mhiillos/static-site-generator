#!/usr/bin/env python3

from textnode import TextNode, TextType


def main():
    test = TextNode("test", TextType.URL, "https://www.boot.dev")
    print(test)


if __name__ == "__main__":
    main()
