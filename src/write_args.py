def write_args(file_path, *args):
    with open(file_path, "a+", encoding="utf-8") as f:
        for arg in args[:-1]:
            f.write(str(arg))
            f.write(",")
        f.write(str(args[-1]))
        f.write("\n")
