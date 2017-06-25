# pylint: disable=locally-disabled,missing-docstring,invalid-name
# -*- coding: utf-8 -*-

from myclassa import myclassa
from myclassb import myclassb


def cb_action_one():
    return "External callback for action_one"


def cb_action_two():
    return "External callback for action_two"


def main():
    mc1 = myclassa(5, 10)
    mc2 = myclassb(13)

    print("mc1.x: ", mc1.x)
    mc1.x = 10
    print("mc1.x: ", mc1.x)
    print("mc1.cb: ", mc1.cb())
    mc1.cb1 = cb_action_one
    print("mc1.cb: ", mc1.cb())
    print("mc2.x: ", mc2.x)
    print("mc2.y: ", mc2.y)
    print("mc2.z: ", mc2.z)
    mc2.x = 15
    mc2.y = 30
    print("mc2.x: ", mc2.x)
    print("mc2.y: ", mc2.y)
    print("mc2.z: ", mc2.z)
    print("mc2.cb: ", mc2.cb())


if __name__ == "__main__":
    main()
