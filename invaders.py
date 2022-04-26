#!/usr/bin/env python3
# Richard Cruz
# CPSC 386-01
# 2021-12-01
# rcruz99@csu.fullerton.edu
# @rcrz10
#
# Lab 05-01
#
# Space Invader game implemented in python with pygame
#
"""Main function that starts loop for Space Invader Game"""

from space_invaders import InvaderGame


def main():
    """Main function for Space Invader Game, starts game loop"""
    game = InvaderGame()
    exit_code = game.run()
    exit(exit_code)
    return 0


if __name__ == '__main__':
    main()
