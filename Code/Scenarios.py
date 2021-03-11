# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 11:49:46 2021

@author: benel
"""

# All Scenarios have the structure [waiting time, arrival time, expected waiting times] for every vehicle

#import random as r
from numpy import random as r

# Always 20 vehicles so Benchmark running time is reasonable
scenario1_rush = {'entry_times': [0, 1, 4, 5, 7, 8, 9, 11, 12, 13, 15, 17, 21, 22, 24, 25, 26, 27, 28, 29], 
                  'actual_waiting_times': [3, 5, 5, 3, 6, 3, 5, 3, 4, 4, 5, 4, 3, 3, 4, 3, 4, 4, 5, 3], 
                  'expected_waiting_times': [5, 5, 4, 3, 5, 5, 5, 5, 3, 5, 6, 4, 3, 3, 3, 2, 3, 3, 6, 1]}

scenario2_rush = {'entry_times': [0, 1, 4, 5, 8, 9, 10, 12, 13, 15, 17, 18, 19, 20, 22, 24, 26, 27, 28, 29], 'actual_waiting_times': [3, 6, 5, 4, 3, 4, 7, 3, 4, 3, 4, 6, 5, 4, 4, 4, 5, 3, 3, 6], 'expected_waiting_times': [3, 8, 6, 4, 2, 4, 8, 6, 4, 2, 4, 6, 5, 3, 5, 5, 4, 6, 2, 7]}

scenario3_rush = {'entry_times': [0, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 14, 15, 18, 21, 22, 23, 24, 26, 27], 'actual_waiting_times': [3, 4, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 4, 5, 4, 4, 4, 3, 4, 6], 'expected_waiting_times': [2, 4, 4, 3, 3, 1, 4, 2, 3, 4, 5, 5, 4, 6, 5, 4, 4, 2, 3, 6]}

scenario4_rush = {'entry_times': [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13, 16, 17, 18, 19, 22, 23, 26, 28], 'actual_waiting_times': [7, 3, 3, 4, 4, 5, 5, 3, 3, 4, 5, 4, 3, 4, 5, 3, 3, 4, 3, 4],'expected_waiting_times': [6, 2, 3, 4, 5, 6, 8, 3, 2, 5, 4, 4, 4, 5, 6, 4, 3, 6, 6, 3]}

scenario5_rush = {'entry_times': [0, 1, 3, 4, 7, 10, 11, 12, 13, 15, 16, 18, 20, 21, 23, 24, 25, 26, 27, 29], 'actual_waiting_times': [4, 3, 5, 5, 5, 4, 5, 3, 3, 3, 3, 3, 3, 4, 4, 6, 3, 3, 5, 5], 'expected_waiting_times': [5, 3, 6, 4, 5, 4, 4, 2, 3, 1, 2, 2, 3, 3, 3, 6, 1, 5, 5, 5]}

scenario6_rush = {'entry_times': [0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 15, 16, 17, 19, 20, 21, 22, 23], 'actual_waiting_times': [4, 3, 5, 5, 3, 3, 5, 4, 4, 4, 4, 5, 6, 4, 4, 4, 3, 4, 6, 3], 'expected_waiting_times': [3, 5, 2, 6, 2, 2, 6, 6, 5, 5, 5, 5, 5, 1, 4, 3, 3, 4, 5, 2]}

scenario7_rush = {'entry_times': [0, 2, 4, 6, 7, 9, 11, 13, 14, 15, 16, 18, 20, 22, 23, 25, 26, 27, 28, 31], 'actual_waiting_times': [3, 3, 4, 5, 5, 3, 4, 5, 3, 3, 4, 4, 3, 4, 5, 3, 3, 6, 3, 4], 'expected_waiting_times': [1, 4, 6, 6, 6, 4, 3, 4, 3, 3, 4, 6, 3, 4, 5, 3, 4, 5, 3, 6]}

scenario8_rush = {'entry_times': [0, 1, 2, 3, 5, 7, 8, 11, 12, 13, 14, 16, 17, 18, 22, 25, 27, 29, 30, 31], 'actual_waiting_times': [4, 5, 3, 3, 4, 3, 4, 6, 4, 4, 4, 4, 5, 3, 4, 4, 4, 3, 7, 4], 'expected_waiting_times': [6, 6, 1, 3, 6, 1, 5, 6, 4, 3, 6, 5, 6, 4, 4, 3, 3, 3, 8, 5]}

scenario9_rush = {'entry_times': [0, 2, 5, 7, 9, 10, 12, 13, 14, 16, 18, 20, 21, 24, 26, 29, 30, 31, 32, 33], 'actual_waiting_times': [4, 4, 4, 5, 5, 4, 4, 4, 3, 4, 4, 4, 5, 3, 4, 7, 4, 4, 5, 4], 'expected_waiting_times': [3, 3, 4, 4, 5, 4, 4, 5, 3, 6, 4, 2, 2, 1, 4, 8, 4, 7, 4, 5]}

scenario10_rush = {'entry_times': [0, 1, 3, 5, 8, 9, 10, 12, 13, 15, 16, 18, 20, 21, 22, 24, 26, 28, 29, 31], 'actual_waiting_times': [4, 4, 5, 4, 4, 3, 3, 5, 4, 4, 5, 3, 5, 3, 4, 3, 3, 4, 5, 5], 'expected_waiting_times': [3, 3, 5, 3, 3, 2, 4, 5, 5, 4, 4, 2, 7, 4, 5, 4, 4, 3, 5, 5]}

scenario11_rush = {'entry_times': [0, 1, 2, 4, 6, 8, 10, 12, 13, 15, 17, 18, 19, 20, 21, 22, 25, 27, 28, 30], 'actual_waiting_times': [3, 6, 6, 3, 5, 3, 3, 6, 4, 3, 4, 3, 5, 5, 4, 4, 6, 4, 4, 4], 'expected_waiting_times': [2, 8, 6, 4, 7, 3, 3, 6, 4, 0, 4, 4, 5, 7, 4, 5, 8, 4, 3, 4]}

scenario12_rush = {'entry_times': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 15, 17, 18, 20, 21, 22, 24, 25], 'actual_waiting_times': [4, 3, 4, 4, 5, 3, 5, 5, 3, 4, 3, 5, 6, 5, 4, 6, 5, 3, 4, 4], 'expected_waiting_times': [4, 2, 6, 3, 7, 3, 5, 5, 2, 5, 3, 6, 8, 8, 5, 7, 5, 2, 4, 5]}

scenario13_rush = {'entry_times': [0, 2, 4, 6, 7, 9, 10, 11, 12, 15, 17, 19, 20, 21, 22, 23, 24, 25, 27, 28], 'actual_waiting_times': [3, 4, 3, 3, 3, 4, 4, 4, 3, 4, 5, 5, 3, 3, 5, 3, 4, 4, 3, 6], 'expected_waiting_times': [4, 3, 3, 2, 2, 4, 4, 4, 2, 6, 7, 6, 4, 4, 7, 3, 5, 7, 2, 5]}

scenario14_rush = {'entry_times': [0, 2, 3, 6, 7, 9, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23, 25, 27], 'actual_waiting_times': [4, 5, 3, 4, 5, 4, 4, 3, 5, 4, 5, 4, 5, 3, 5, 4, 3, 4, 4, 4], 'expected_waiting_times': [2, 4, 1, 3, 5, 5, 4, 2, 5, 4, 6, 3, 5, 2, 5, 3, 3, 2, 5, 6]}

scenario15_rush = {'entry_times': [0, 2, 3, 5, 7, 8, 10, 12, 13, 15, 16, 18, 20, 22, 24, 25, 26, 29, 31, 32], 'actual_waiting_times': [4, 3, 3, 4, 3, 6, 4, 3, 4, 6, 3, 4, 4, 3, 4, 3, 4, 4, 4, 4], 'expected_waiting_times': [4, 2, 3, 4, 5, 6, 4, 4, 5, 7, 1, 3, 5, 3, 3, 3, 3, 6, 4, 5]}

scenario16_rush = {'entry_times': [0, 1, 3, 4, 5, 7, 9, 13, 14, 16, 17, 18, 19, 21, 24, 26, 27, 28, 29, 31], 'actual_waiting_times': [5, 5, 5, 5, 4, 5, 4, 3, 3, 5, 5, 4, 4, 4, 3, 3, 3, 4, 5, 4], 'expected_waiting_times': [4, 6, 6, 6, 3, 4, 5, 4, 2, 5, 6, 4, 5, 3, 3, 4, 3, 3, 5, 3]}

scenario17_rush = {'entry_times': [0, 1, 4, 6, 8, 9, 11, 13, 14, 16, 18, 20, 23, 24, 26, 28, 30, 31, 32, 34], 'actual_waiting_times': [4, 5, 3, 3, 4, 4, 3, 3, 4, 4, 3, 3, 4, 4, 4, 3, 7, 4, 4, 3], 'expected_waiting_times': [4, 4, 4, 2, 5, 3, 2, 4, 4, 5, 4, 1, 5, 3, 4, 4, 9, 2, 5, 3]}

scenario18_rush = {'entry_times': [0, 1, 3, 5, 7, 8, 10, 13, 14, 15, 17, 19, 20, 21, 23, 25, 26, 28, 30, 31], 'actual_waiting_times': [4, 4, 3, 3, 3, 4, 3, 4, 5, 4, 4, 5, 4, 3, 4, 3, 4, 3, 3, 3], 'expected_waiting_times': [4, 2, 5, 2, 4, 5, 4, 5, 5, 4, 3, 4, 4, 2, 5, 3, 3, 2, 3, 4]}

scenario19_rush = {'entry_times': [0, 1, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 21, 22, 23, 24], 'actual_waiting_times': [4, 4, 3, 5, 3, 6, 4, 4, 5, 3, 3, 3, 3, 3, 5, 4, 4, 3, 4, 5], 'expected_waiting_times': [4, 6, 3, 3, 5, 6, 4, 2, 4, 2, 5, 2, 3, 3, 6, 5, 4, 3, 3, 4]}

scenario20_rush = {'entry_times': [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 16, 17, 20, 22, 23, 26, 27, 29, 31], 'actual_waiting_times': [6, 5, 4, 3, 3, 4, 4, 5, 5, 4, 5, 3, 4, 6, 3, 5, 6, 4, 6, 5], 'expected_waiting_times': [5, 3, 5, 3, 5, 2, 5, 4, 3, 4, 6, 3, 2, 5, 4, 4, 9, 5, 7, 7]}


# Relaxed scenario: randint(3,15) for waiting time, arrival time randint(2,15)
scenario1_relax = {'entry_times': [0, 1, 9, 13, 14, 19, 23, 24, 26, 30, 36, 38, 42, 47, 50, 54, 58, 63, 67, 73], 
                   'actual_waiting_times': [4, 5, 6, 3, 4, 4, 4, 3, 7, 5, 3, 6, 6, 4, 8, 3, 4, 3, 5, 4], 
                   'expected_waiting_times': [4, 5, 6, 1, 6, 5, 3, 5, 8, 5, 3, 7, 6, 4, 7, 3, 4, 2, 4, 4]}

scenario2_relax = {'entry_times': [0, 3, 6, 10, 14, 17, 19, 25, 28, 33, 36, 38, 44, 48, 51, 56, 63, 65, 68, 72], 'actual_waiting_times': [4, 3, 4, 4, 5, 4, 5, 4, 4, 5, 4, 5, 4, 6, 5, 4, 7, 4, 5, 3], 'expected_waiting_times': [3, 3, 4, 5, 3, 3, 5, 2, 4, 6, 5, 5, 5, 5, 6, 4, 10, 4, 4, 4]}

scenario3_relax = {'entry_times': [0, 2, 4, 8, 10, 12, 16, 21, 26, 31, 34, 39, 44, 46, 50, 54, 59, 61, 65, 69], 'actual_waiting_times': [4, 4, 3, 4, 3, 4, 4, 6, 4, 3, 7, 5, 6, 5, 5, 5, 4, 4, 3, 3], 'expected_waiting_times': [5, 5, 3, 4, 1, 4, 4, 5, 5, 3, 6, 7, 5, 5, 6, 3, 6, 4, 3, 0]}

scenario4_relax = {'entry_times': [0, 3, 7, 10, 15, 17, 22, 26, 28, 35, 38, 39, 42, 47, 48, 53, 60, 64, 68, 72], 'actual_waiting_times': [4, 3, 3, 5, 5, 3, 4, 4, 6, 5, 6, 6, 3, 5, 7, 3, 5, 4, 5, 5], 'expected_waiting_times': [4, 4, 2, 7, 5, 1, 5, 6, 9, 3, 5, 8, 4, 4, 8, 2, 5, 5, 7, 6]}

scenario5_relax = {'entry_times': [0, 3, 7, 10, 13, 14, 16, 21, 23, 25, 29, 33, 39, 43, 48, 51, 54, 56, 61, 66], 'actual_waiting_times': [6, 3, 5, 6, 3, 5, 4, 6, 4, 3, 5, 4, 7, 5, 4, 5, 4, 5, 4, 3], 'expected_waiting_times': [6, 2, 5, 7, 2, 6, 3, 7, 5, 2, 4, 3, 5, 4, 3, 4, 4, 3, 2, 5]}

scenario6_relax = {'entry_times': [0, 4, 9, 11, 15, 21, 23, 27, 29, 33, 37, 41, 46, 52, 55, 59, 64, 68, 71, 75], 'actual_waiting_times': [4, 3, 4, 5, 3, 3, 4, 6, 6, 4, 3, 3, 6, 6, 4, 3, 5, 5, 4, 7], 'expected_waiting_times': [3, 5, 4, 5, 2, 1, 2, 6, 5, 4, 3, 0, 6, 6, 5, 2, 4, 7, 3, 6]}

scenario7_relax = {'entry_times': [0, 3, 6, 9, 12, 16, 20, 22, 26, 30, 33, 38, 40, 42, 46, 48, 52, 56, 57, 61], 'actual_waiting_times': [4, 5, 4, 4, 3, 6, 5, 5, 5, 6, 3, 5, 5, 6, 4, 4, 5, 6, 3, 5], 'expected_waiting_times': [6, 5, 4, 6, 3, 8, 5, 4, 7, 5, 2, 2, 4, 6, 3, 5, 6, 6, 4, 6]}

scenario8_relax = {'entry_times': [0, 4, 10, 14, 18, 22, 25, 29, 34, 38, 42, 46, 51, 54, 60, 62, 66, 69, 72, 74], 'actual_waiting_times': [4, 4, 5, 5, 5, 5, 6, 4, 5, 4, 6, 3, 4, 3, 3, 6, 3, 3, 7, 5], 'expected_waiting_times': [5, 4, 5, 5, 4, 6, 6, 3, 6, 4, 6, 3, 6, 1, 3, 8, 1, 4, 9, 6]}

scenario9_relax = {'entry_times': [0, 2, 7, 9, 12, 15, 21, 26, 29, 34, 40, 42, 46, 48, 51, 56, 60, 62, 66, 68], 'actual_waiting_times': [7, 7, 4, 3, 4, 4, 3, 4, 3, 3, 3, 4, 4, 4, 3, 5, 5, 5, 5, 4], 'expected_waiting_times': [7, 8, 5, 2, 3, 5, 3, 5, 3, 3, 3, 4, 4, 3, 2, 5, 5, 6, 4, 3]}

scenario10_relax = {'entry_times': [0, 3, 6, 9, 13, 18, 20, 25, 30, 33, 37, 42, 46, 49, 52, 55, 61, 64, 69, 71], 'actual_waiting_times': [5, 5, 4, 3, 4, 5, 5, 4, 4, 5, 5, 5, 4, 4, 6, 4, 4, 3, 5, 4], 'expected_waiting_times': [7, 4, 4, 3, 4, 6, 5, 3, 6, 6, 6, 6, 4, 4, 8, 2, 5, 2, 5, 5]}

scenario11_relax = {'entry_times': [0, 1, 6, 9, 11, 14, 17, 20, 25, 30, 32, 37, 41, 46, 51, 55, 59, 63, 64, 67], 'actual_waiting_times': [4, 5, 7, 5, 3, 3, 5, 5, 6, 5, 5, 4, 4, 4, 3, 4, 4, 7, 3, 4], 'expected_waiting_times': [3, 6, 7, 8, 5, 2, 5, 4, 8, 5, 6, 2, 4, 5, 3, 6, 4, 8, 4, 4]}

scenario12_relax = {'entry_times': [0, 3, 6, 11, 19, 22, 27, 29, 33, 35, 39, 44, 48, 50, 55, 60, 64, 69, 75, 78], 'actual_waiting_times': [4, 3, 4, 3, 4, 8, 5, 6, 5, 5, 3, 5, 5, 4, 4, 5, 6, 6, 4, 4], 'expected_waiting_times': [2, 3, 2, 6, 6, 10, 4, 4, 3, 4, 2, 7, 5, 3, 4, 4, 5, 7, 3, 4]}

scenario13_relax = {'entry_times': [0, 6, 7, 13, 18, 23, 28, 31, 34, 38, 43, 46, 53, 55, 60, 66, 69, 75, 82, 86], 'actual_waiting_times': [3, 3, 4, 4, 4, 3, 5, 4, 4, 4, 5, 5, 4, 5, 3, 6, 3, 4, 4, 6], 'expected_waiting_times': [2, 3, 3, 3, 6, 5, 5, 4, 3, 5, 5, 5, 6, 5, 2, 6, 3, 5, 6, 5]}

scenario14_relax = {'entry_times': [0, 2, 8, 12, 17, 20, 22, 26, 29, 32, 37, 42, 45, 51, 57, 59, 61, 65, 72, 76], 'actual_waiting_times': [5, 6, 5, 5, 5, 3, 4, 6, 4, 4, 7, 5, 3, 5, 3, 4, 3, 4, 3, 4], 'expected_waiting_times': [5, 5, 3, 4, 5, 1, 4, 6, 6, 5, 7, 3, 3, 5, 4, 2, 1, 4, 3, 4]}

scenario15_relax = {'entry_times': [0, 2, 5, 7, 11, 15, 20, 23, 28, 32, 38, 41, 43, 44, 45, 49, 50, 56, 62, 66], 'actual_waiting_times': [3, 4, 5, 4, 6, 3, 4, 4, 4, 3, 5, 5, 4, 4, 4, 3, 5, 4, 6, 4], 'expected_waiting_times': [3, 5, 6, 4, 5, 3, 4, 2, 5, 3, 7, 7, 3, 7, 5, 2, 6, 2, 7, 3]}

scenario16_relax = {'entry_times': [0, 4, 8, 10, 13, 15, 18, 23, 26, 32, 36, 41, 46, 51, 58, 62, 66, 69, 75, 78], 'actual_waiting_times': [3, 5, 4, 7, 4, 4, 3, 4, 4, 5, 5, 4, 4, 5, 3, 4, 6, 7, 5, 4], 'expected_waiting_times': [4, 5, 4, 7, 3, 4, 5, 3, 2, 5, 5, 5, 4, 6, 2, 3, 6, 8, 6, 4]}

scenario17_relax = {'entry_times': [0, 5, 8, 13, 19, 21, 25, 29, 31, 33, 36, 42, 47, 48, 51, 55, 58, 60, 62, 64], 'actual_waiting_times': [4, 4, 3, 4, 4, 5, 4, 5, 5, 3, 5, 4, 5, 4, 5, 5, 5, 3, 4, 5], 'expected_waiting_times': [4, 5, 4, 3, 1, 5, 4, 4, 7, 5, 5, 6, 7, 3, 5, 4, 6, 4, 3, 4]}

scenario18_relax = {'entry_times': [0, 3, 7, 11, 14, 19, 22, 28, 30, 34, 39, 44, 49, 50, 55, 58, 63, 66, 73, 76], 'actual_waiting_times': [4, 6, 3, 3, 4, 3, 4, 4, 3, 3, 4, 3, 7, 6, 5, 3, 3, 5, 4, 3], 'expected_waiting_times': [5, 5, 2, 3, 5, 3, 6, 6, 3, 4, 6, 4, 5, 4, 5, 3, 3, 4, 3, 3]}

scenario19_relax = {'entry_times': [0, 5, 7, 12, 17, 18, 24, 26, 32, 36, 40, 43, 47, 53, 58, 64, 68, 73, 76, 82], 'actual_waiting_times': [4, 4, 4, 4, 5, 3, 4, 6, 4, 5, 6, 5, 5, 5, 5, 5, 6, 4, 6, 6], 'expected_waiting_times': [5, 4, 4, 5, 6, 2, 2, 6, 6, 5, 6, 4, 4, 5, 5, 6, 5, 4, 6, 6]}

scenario20_relax = {'entry_times': [0, 4, 5, 8, 11, 16, 19, 24, 29, 33, 35, 39, 40, 43, 45, 49, 51, 52, 57, 60], 'actual_waiting_times': [4, 4, 4, 5, 3, 3, 5, 4, 6, 5, 7, 4, 5, 5, 5, 5, 5, 4, 4, 5], 'expected_waiting_times': [3, 5, 3, 6, 4, 3, 7, 5, 8, 5, 8, 5, 5, 5, 4, 5, 6, 5, 3, 5]}


# Generate a new scenario
def new_scenario(rush = True):
    scenario = {}
    scenario['entry_times'] = []
    scenario['entry_times'].append(0)
    
    if rush:
        for i in range(1,20):
            scenario['entry_times'].append(scenario['entry_times'][i-1]+r.binomial(n=5, p=0.1)+1)
    else:
        for i in range(1,20):
            scenario['entry_times'].append(scenario['entry_times'][i-1]+r.binomial(n=10, p=0.25)+1)
    
    if rush:
        scenario['actual_waiting_times'] = []
        for i in range(20):
            scenario['actual_waiting_times'].append(r.binomial(7,0.15)+3)
        
    else:
        scenario['actual_waiting_times'] = []
        for i in range(20):
            scenario['actual_waiting_times'].append(r.binomial(7,0.2)+3)
        
    scenario['expected_waiting_times'] = []
    for i in range(20):
        scenario['expected_waiting_times'].append(scenario['actual_waiting_times'][i] + r.binomial(6,0.5)-3)
        
    print(scenario)
    return

# new_scenario(False)

# Generate a new retirement scenario
def new_scenario_retirement():
    scenario = {}
    scenario['entry_times'] = []
    scenario['entry_times'].append(0)
    scenario['actual_waiting_times'] = []
    old_1 = True
    old_2 = True
    
    for i in range(20):
       old_1 = old_2
       old_2 = r.choice([True, True, True, False, False])
       
       if old_1 and old_2:
           if i != 0:
               scenario['entry_times'].append(scenario['entry_times'][i-1]+2)
           scenario['actual_waiting_times'].append(r.binomial(6,0.5)+12)
           
       elif old_2:
           if i != 0:
               scenario['entry_times'].append(scenario['entry_times'][i-1]+r.binomial(n=10, p=0.25)+2)
           scenario['actual_waiting_times'].append(r.binomial(6,0.5)+12)
           
       else:
           if i != 0:
               scenario['entry_times'].append(scenario['entry_times'][i-1]+r.binomial(n=10, p=0.25)+2)
           scenario['actual_waiting_times'].append(r.binomial(6,0.5)+2)
    
    
    print(scenario)
    return

# Retirement scenarios generated with new_scenario_retirement()
scenario1_retirement = {'entry_times': [0, 2, 4, 8, 13, 19, 26, 28, 30, 34, 38, 42, 47, 51, 54, 59, 61, 63, 65, 67], 
                        'actual_waiting_times': [14, 16, 14, 5, 7, 7, 15, 16, 16, 7, 6, 4, 5, 6, 3, 15, 15, 14, 16, 15]}

scenario2_retirement = {'entry_times': [0, 7, 12, 16, 22, 25, 27, 29, 31, 33, 39, 43, 45, 53, 57, 59, 61, 67, 73, 75], 
                        'actual_waiting_times': [5, 14, 6, 14, 6, 13, 15, 14, 16, 4, 4, 15, 14, 6, 16, 15, 13, 4, 14, 15]}

scenario3_retirement = {'entry_times': [0, 2, 9, 12, 14, 16, 22, 27, 32, 36, 42, 44, 46, 48, 52, 56, 58, 60, 66, 69], 
                        'actual_waiting_times': [15, 13, 6, 14, 15, 14, 5, 15, 5, 15, 3, 15, 12, 16, 5, 14, 16, 14, 4, 17]}

scenario4_retirement = {'entry_times': [0, 2, 4, 6, 11, 14, 17, 22, 28, 34, 40, 46, 50, 55, 57, 60, 64, 69, 74, 77], 
                        'actual_waiting_times': [15, 16, 15, 16, 5, 14, 4, 16, 5, 15, 3, 4, 6, 15, 16, 5, 5, 16, 5, 18]}

scenario5_retirement = {'entry_times': [0, 2, 8, 13, 19, 22, 25, 30, 34, 40, 44, 46, 51, 53, 60, 66, 68, 71, 73, 75], 
                        'actual_waiting_times': [15, 15, 4, 16, 6, 17, 4, 6, 16, 5, 14, 13, 6, 16, 5, 17, 14, 6, 17, 16]}

scenario6_retirement = {'entry_times': [0, 7, 10, 12, 17, 20, 23, 30, 33, 38, 43, 46, 51, 55, 57, 65, 67, 71, 73, 75], 
                        'actual_waiting_times': [14, 4, 4, 15, 5, 6, 14, 7, 5, 6, 6, 14, 4, 17, 15, 4, 6, 16, 14, 18]}

scenario7_retirement = {'entry_times': [0, 2, 4, 6, 12, 16, 18, 20, 26, 32, 37, 39, 42, 47, 54, 58, 60, 64, 71, 75], 
                        'actual_waiting_times': [12, 16, 15, 17, 6, 17, 15, 14, 6, 4, 16, 16, 6, 14, 6, 15, 15, 5, 14, 5]}

scenario8_retirement = {'entry_times': [0, 7, 13, 17, 23, 27, 31, 33, 35, 40, 47, 52, 57, 59, 61, 67, 72, 75, 77, 81], 
                        'actual_waiting_times': [14, 5, 14, 6, 5, 6, 15, 13, 15, 4, 13, 4, 16, 15, 15, 5, 4, 15, 13, 5]}

scenario9_retirement = {'entry_times': [0, 3, 7, 9, 15, 21, 25, 30, 32, 36, 42, 47, 49, 51, 55, 61, 66, 69, 72, 76], 
                        'actual_waiting_times': [3, 4, 15, 14, 6, 16, 4, 15, 16, 6, 4, 13, 14, 17, 3, 5, 15, 4, 14, 5]}

scenario10_retirement = {'entry_times': [0, 2, 4, 6, 8, 13, 17, 19, 21, 23, 25, 30, 34, 39, 44, 50, 52, 56, 58, 60], 
                         'actual_waiting_times': [16, 14, 18, 13, 14, 4, 6, 17, 17, 14, 14, 4, 5, 4, 5, 14, 15, 5, 14, 14]}



