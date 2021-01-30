# Spoiler-free UFC

A Python tool for printing spoiler-free fight cards or fighter schedules.
When printing fight cards, the tool randomly chooses which fighter to output
  first.


## Example

Edit spoiler_free.py to choose event.
Such as `event = 'UFC 252'`.
Type `make`, `make e`, or `make event` to print fight card.

``` bash
$ make event
```

![event_example](https://raw.githubusercontent.com/scrasmussen/spoiler-free-UFC/main/images/event_example.png)



Edit spoiler_free.py to choose a fighter, be it MMA or boxer.
Such as `fighter = 'Andre Ward'`.
Type `make`, `make f`, or `make fighter` to print fighter schedule.

``` bash
$ make fighter
```



![fighter_schedule](https://raw.githubusercontent.com/scrasmussen/spoiler-free-UFC/main/images/fighter_schedule_example.png)


## Todo
 - Handle `make Andre Ward` or `make UFC 250` input.

## Known Bugs
 - Some fight cards don't work.
 - If a fighter has done boxing and MMA it might get wrong information.
