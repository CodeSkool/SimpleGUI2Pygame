#!/usr/local/bin/python

#-------------------------------------------------------------------------------
# Name:        pgxtra
# Purpose:     Provides extra controls for pygame.
# Author:      Jules
# Created:     06/29/2013
# Copyright:   (c) Julie Ann Stoltz 2013
# Licence:     DBAD (refer to http://www.dbad-license.org/)
#-------------------------------------------------------------------------------

import pygame

LEGAL_KEYS = {pygame.K_q: 'q', pygame.K_w: 'w', pygame.K_e: 'e',
              pygame.K_r: 'r', pygame.K_t: 't', pygame.K_y: 'y',
              pygame.K_u: 'u', pygame.K_i: 'i', pygame.K_o: 'o',
              pygame.K_p: 'p', pygame.K_a: 'a', pygame.K_s: 's',
              pygame.K_d: 'd', pygame.K_f: 'f', pygame.K_g: 'g',
              pygame.K_h: 'h', pygame.K_j: 'j', pygame.K_k: 'k',
              pygame.K_l: 'l', pygame.K_z: 'z', pygame.K_x: 'x',
              pygame.K_c: 'c', pygame.K_v: 'v', pygame.K_b: 'b',
              pygame.K_n: 'n', pygame.K_m: 'm', pygame.K_SPACE: ' '}

def main():
    ## Basic tests
    print LEGAL_KEYS

if __name__ == '__main__':
    main()











