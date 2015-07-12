# Use while loops to pick out the ogre

loop:
    enemies = self.findEnemies() # 1
    enemyIndex = 0               # 2

    # Attack all enemies.
    while enemyIndex < len(enemies): # 3
        enemy = enemies[enemyIndex]  # 4
        enemyIndex = enemyIndex + 1  # 5
        # If enemy isn't Sand Yak
        if enemy.type != "sand-yak":
            # While the enemy's health
            # is more than 0
            while enemy.health > 0:
                # Attack!
                if self.isReady("cleave"):
                    self.cleave(enemy)
                else:
                    self.attack(enemy)
                    self.bash(enemy)

        # Between waves, move to center.
        self.moveXY(40, 33)


#### Q: Explain why enemyIndex variable is set

#### Q: Explain how we're using len(enemyIndex) to check if there's any enemies
#       while enemyIndex < len(enemies):
#       1. First we're getting a list of all our `enemies`
#       2. Next we're setting the `enemyIndex = 0`
#       3. While `enemyIndex` less than `enemies` list length
#       4. Set `enemy` to the first enemy `enemies[0]`
#       5. Every time the while loop runs, increment enemyIndex by 1
#          - This could also be places after the `if` statement
#          - But it does look cleaner this way!!
#       6: If the enemy has health, attack

#### Q: Explain how we're incrementing the enemyIndex