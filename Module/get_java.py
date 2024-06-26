import os


def get_java():
    java_dir = os.listdir("C:\Program Files\Java")
    java_dir = [x for x in java_dir if x.startswith("jdk")]
    java_dir.insert(0, "기본")
    return java_dir
