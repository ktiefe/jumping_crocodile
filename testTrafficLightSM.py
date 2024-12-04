import unittest
import os
from TrafficLightSM import TrafficLightMachine

class TrafficLightSMTest(unittest.TestCase):
    def setUp(self):
        """Set up the TrafficLightSM instance for testing."""
        self.traffic_light = TrafficLightMachine()

    def test_initial_state(self):
        """Test the initial state of the traffic light."""
        self.assertEqual(self.traffic_light.current_state.id, 'green')

    def test_go_to_yellow_state(self):
        """  Test to check if sm transits to next state"""
        self.traffic_light.send('cycle')
        self.assertEqual(self.traffic_light.current_state.id, 'yellow')

    def test_go_to_red_state(self):
        """  Test to check if sm transits to next state"""
        self.traffic_light.send('cycle')
        self.traffic_light.send('cycle')
        self.assertEqual(self.traffic_light.current_state.id, 'red')

    def tearDown(self) -> None:
        return super().tearDown()
    
def generate_docs():
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    img_path = f"{current_folder_path}/docs/readme_trafficlightmachine.png"
    sm = TrafficLightMachine()
    sm._graph().write_png(img_path)

if __name__ == '__main__':
    unittest.main()
    generate_docs()

