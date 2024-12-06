import unittest
import os
from FruitSM import FruitSM

class FruitSMTest(unittest.TestCase):
    def setUp(self):
        """Set up the TrafficLightSM instance for testing."""
        self.fruit_sm = FruitSM()

    def test_initial_state(self):
        """Test the initial state of the fruit."""
        self.assertEqual(self.fruit_sm.current_state.id, 'idle')

    def test_go_to_next_state(self):
        """  Test to check if sm transits to next state"""
        self.fruit_sm.send('action')
        self.fruit_sm.send('animate')
        self.assertEqual(self.fruit_sm.current_state.id, 'collect')

    def test_go_to_end_state(self):
        """  Test to check if sm transits to next state"""
        self.fruit_sm.send('action')
        self.fruit_sm.send('animate')
        self.fruit_sm.send('action')
        self.fruit_sm.send('animate')
        self.assertEqual(self.fruit_sm.current_state.id, 'end')
        self.fruit_sm.send('animate')
        self.fruit_sm.send('animate')

    def tearDown(self) -> None:
        return super().tearDown()
    
def generate_docs():
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    img_path = f"{current_folder_path}/docs/readme_fruitSm.png"
    sm = FruitSM()
    sm._graph().write_png(img_path)

if __name__ == '__main__':
    unittest.main()
    generate_docs()

