import fighter as ft
import fightEvent as fe
import sys


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
fighter_name = fighter
# allows easy access to fighters near the top
if 'ffighter' in locals():
    fighter_name = ffighter

event = fe.FightEvent(event)
event.print_name()
event.print_events()

sys.exit()
# --- handle fighter ---
fighter = ft.Fighter(fighter_name)
fighter.print_name()
fighter.print_records()

print("Fin")
