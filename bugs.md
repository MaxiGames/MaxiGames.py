### SERIOUS BUGS:
- connect4 winning system broke down, as there is apparently unreachable code for "if success..." (line 348, etc.)
- same file (connect4), weird unreachable code due to a break in line 254
- hangman broke due to whole word being guessed (check heroku logs? what problem could it be)
- hourly slash command broken
- can't press next button on help slash command
- hangmanlist paginator broke (no buttons)

## Less serious bugs/future implementations:
- should implement error message for perms not given for stuff like clear 
- cooldowns for command are activated before they are even used
- should implement exitgame for connect4/scramble/hangman etc.
- actually finish the shop and make it have globalised items :D 
- implement the se luck boost and expand (maybe vote reward?)