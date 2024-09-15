import arduinoRPi.Messenger as arduino 
from line_detection import count_error, apply_thresh

import time


class PID:
    def __init__(self,
        k_p=0.3, k_d=0.025, k_i=0, delta=0.05,
        base_speed=180, min_speed=0, max_speed=250
    ):
        self.base_speed = base_speed
        self.min_speed, self.max_speed = min_speed, max_speed

        self.prev_error = 0
        self.delta = delta

        self.k_p, self.k_d, self.k_i = k_p, k_d, k_i


    def iteration(self, frame, serializer):
        start_iter = time.time()

        new_error = count_error(frame)

        derivative_error = (new_error - self.prev_error) / self.delta
        integral_error = (self.prev_error + new_error) * (self.delta / 2)

        output_signal =  self.k_p * new_error
        output_signal += self.k_d * derivative_error
        output_signal += self.k_i * integral_error

        left_motor = int(self.__crop_speed(self.base_speed + output_signal))
        right_motor = int(self.__crop_speed(self.base_speed - output_signal))

        arduino.send_message(serializer, right_motor, left_motor)

        end_iter = time.time()
        duration_iter = end_iter - start_iter
        if duration_iter < self.delta:
            time.sleep(self.delta - duration_iter)


    def __crop_speed(self, val):
        return max(self.min_speed, min(val, self.max_speed))
