import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import numpy as np

class My_Signal_Processor(Node):
    def __init__(self):
        super().__init__('process')
        self.signal_subscription = self.create_subscription(Float32, '/signal', self.signal_callback, 10)
        self.time_subscription = self.create_subscription(Float32, '/time', self.time_callback, 10)
        self.process_signal_publisher = self.create_publisher(Float32, '/proc_signal',10)
        self.get_logger().info('Signal Processor Node initialized')
        
        self.alpha = 0.5
        self.shift = 0.1
        self.time = 0.0

    def process_signal(self, signal):
        offset = signal + self.alpha
        amp = 0.5 * offset
        phase = amp * np.sin(self.time + self.shift)
        return Float32(data = phase)

    def signal_callback(self, msg):
        processed_signal = self.process_signal(msg.data)
        self.process_signal_publisher.publish(processed_signal)
        self.get_logger().info(f'Processed Signal: {processed_signal.data}')

    def time_callback(self, msg):
        self.time = msg.data

def main(args = None):
    rclpy.init(args=args)
    m_sp = My_Signal_Processor()
    rclpy.spin(m_sp)
    m_sp.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
