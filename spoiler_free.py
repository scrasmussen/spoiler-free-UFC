import fighter as ft
import fightEvent as fe
import sys

print_event = True
# print_event = False

# ----------------------------------------------------------------------------
# ---                       choose event                                   ---
# ----------------------------------------------------------------------------
event = 'UFC 250'
# event = 'UFC Fight Night: Ortega vs. The Korean Zombie'


# ----------------------------------------------------------------------------
# ---                       choose fighter                                 ---
# ----------------------------------------------------------------------------
fighter = 'Andre Ward'



# ----------------------------------------------------------------------------
# ---                          process                                     ---
# ----------------------------------------------------------------------------
if print_event is True:
    event = fe.FightEvent(event)
    event.print_name()
    event.print_events()
else:
    # --- handle fighter ---
    fighter_name = fighter
    fighter = ft.Fighter(fighter_name)
    fighter.print_name()
    fighter.print_records()

print("Fin")
