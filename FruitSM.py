from statemachine import StateMachine, State

class Fruit:
    def __init__(self):
        pass

    def animate(self):
        print("animate")

    def eat(self):
        print("eat")

    def is_eaten(self):
        return False

class FruitOrder(StateMachine):
    "A fruit machine"
    fruit = State(initial=True)
    collect = State()
    deth = State(final=True)

    animate = (fruit.to.itself() | collect.to.itself())
    eat = fruit.to(collect)
    is_eaten = collect.to(deth)
    

    def on_enter_idle(self):
        pass

    def on_enter_collect(self):
        pass

    def on_enter_end(self):
        pass

