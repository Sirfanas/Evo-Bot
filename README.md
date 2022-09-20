# Evo-Bot: What is it ?

Evo-Bot is a programming game, the goal is to manage a civilization and grow up against (or with) other player's code.

This is a kind of simulation where the world and bot (player's code) will evolve and survive. Bots have to manage their ressources (like primary ressource, food...) in a "randomly" generated world.

# Game rule

This is a turn by turn game: every player's give all their instructions, then signals they've finished.

When every bot's end their instructions, the game run execute all of them in the given order.

In the case of two (or more) instructions may give a conflict, then specific rules are applied (see more // TODO)

# Game entities

Everything in the game is considered as an Entity. Some can move (Mob), some are static (Wall, Ressources sources).
