# -*- coding: utf-8 -*-
from find import assess_optimal
from find_feature_change import findchange
from features_matrix import FeaturesMatrix

fm = FeaturesMatrix()

def guess_problem_1():
  lines = [line.strip() for line in open("./validation/problem_1_dev")]
  guesses_log_list = []

  def format_guess_1(guess_dict, chars=[]):
    ret = "%s %s" % (chars[0], chars[1])
    for char, guess_list in guess_dict.iteritems():
      ret += "\t%s is %s" % (char, guess_list)

    return ret

  for line in lines:
    p1, p2 = [p for p in line.split(" ")]
    guesses_log_list.append(format_guess_1(findchange(p1, p2), [p1, p2]))

  with open("./validation/problem_1_guesses.txt", "w") as outfile:
    outfile.write('\n'.join(guesses_log_list))



def guess_problem_3():
  lines = [line.strip() for line in open("./validation/problem_1_dev")]
  guesses_log_list = []

  def format_guess_3(guess_list, chars=[]):
    ret = " ".join(chars)
    ret += "\t%s" % guess_list

    return ret

  for line in lines:
    chars = line.split(" ")
    guesses_log_list.append(format_guess_3(assess_optimal(chars), chars))

  with open("./validation/problem_3_guesses.txt", "w") as outfile:
    outfile.write('\n'.join(guesses_log_list))

guess_problem_1()
guess_problem_3()