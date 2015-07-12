#
# While loop
# - Codecombat: Desert (Lurkers)


# findEnemies returns a list of all your enemies.
# Only attack shamans. Don't attack yaks!

enemies = self.findEnemies()
enemyIndex = 0

# Edit 1:
# - Wrap this section in a while loop
#   to iterate over all enemies
# - check where we are in the enemyIndex
#   If it's less than 6 (there are 6 enemies)
#   run the code ...
while enemyIndex < 6:
    # Locate the first enemy (Index 0)
    enemy = enemies[enemyIndex]
    # If the enemy is a 'shaman' ...
    if enemy.type == 'shaman':
        # And their health is more than 0
        while enemy.health > 0:
            # Toast that sucker
            self.attack(enemy)
    # Edit 2:
    # - Increase the index everytime
    #   we kill one of those bitches.
    enemyIndex += 1