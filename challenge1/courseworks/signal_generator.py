import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import numpy as np


class My_Signal_Generator(Node):
    def __init__(self):
        super().__init__('signal_generator')
        self.signal_publisher = self.create_publisher(Float32,'/signal',10)
        self.time_publisher = self.create_publisher(Float32,'/time',10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.time = 0.0
        self.get_logger().info('Signal generator node initialized!!!')

    def timer_callback(self):
        signal_msg = Float32()
        time_msg = Float32()

        signal = self.generate_signal()
        signal_msg.data = signal

        time_msg.data = self.time

        self.signal_publisher.publish(signal_msg)
        self.time_publisher.publish(time_msg)

        self.get_logger().info(f'Time:{time_msg}, Signal:{signal_msg.data}')

        self.time += 0.1

    def generate_signal(self):
        amplitude = 1.0
        freq = 1.0
        return amplitude * np.sin(2 * np.pi * freq * self.time)

def main(args = None):
    rclpy.init(args=args)
    m_sg = My_Signal_Generator()
    rclpy.spin(m_sg)
    m_sg.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
