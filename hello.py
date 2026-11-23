"""练手用的小文件：只有一个函数和一个入口。"""

GREETING = "hello, ci/cd"


def greet(name: str, excited: bool = False) -> str:
    """拼一句问候语。

    excited=True 时用感叹号，方便练习"改一行代码触发一次 CI"。
    """
    name = name.strip() or "你好"
    end = "!" if excited else "."
    return f"hi {name}{end}"


def main() -> None:
    print(greet("rj-pro"))
    print(greet("  reviewer  ", excited=True))


if __name__ == "__main__":
    main()
