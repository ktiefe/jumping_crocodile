import unittest
import os
from FruitSM import Fruit, FruitOrder

class FruitSMTest(unittest.TestCase):
    def setUp(self):
        """Set up the TrafficLightSM instance for testing."""
        self.fruit = Fruit()
        self.fruitOrder = FruitOrder(Fruit)

    def test_initial_state(self):
        """Test the initial state of the fruit."""
        self.assertEqual(self.fruitOrder.current_state.id, 'fruit')

    def test_next_state(self):
        """ Test for next state"""
        self.fruitOrder.send('eat')
        self.assertEqual(self.fruitOrder.current_state.id, 'collect')

    # def test_end_state(self):
    #     """ Test for end state"""
    #     self.fruitOrder.send('eat')
    #     self.assertEqual(self.fruitOrder.current_state.id, 'collect')
    #     self.fruitOrder.send('eat')
    #     self.assertEqual(self.fruitOrder.current_state.id, 'end')

    def tearDown(self) -> None:
        return super().tearDown()
    
def generate_docs():
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    img_path = f"{current_folder_path}/docs/readme_fruitSm.png"
    fruit = Fruit()
    fruitOrder = FruitOrder(Fruit)
    fruitOrder._graph().write_png(img_path)

if __name__ == '__main__':
    unittest.main()
    generate_docs()

