# Spoiler-free UFC
![build status](https://github.com/scrasmussen/spoiler-free-UFC/.github/workflows/main.yml/badge.svg)


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
 - TUI: because [why not](https://graydon2.dreamwidth.org/193447.html)?
<!-- Handle `make Andre Ward` or `make UFC 250` input. -->
 - Improve input parsing
 - Prevent output from being too wide

## Known Bugs
 - Some fight cards don't work.
 - If a fighter has done boxing and MMA it might get wrong information.
<!-- https://news.ycombinator.com/item?id=26090243 -->
