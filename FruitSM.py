from statemachine import StateMachine, State

class Fruit:
    def __init__(self):
        self.bites = 0

    def on_animate(self):
        pass

    def on_eat(self):
        self.bites+=1

    def is_eaten(self):
        return self.bites == 2

class FruitControl(StateMachine):
    "A fruit machine"
    fruit = State(initial=True)
    eaten = State()
    death = State(final=True)

    animate = (fruit.to.itself() | eaten.to.itself())
    eat = ( fruit.to(eaten) | eaten.to.itself(unless="is_eaten") | eaten.to(death) )

