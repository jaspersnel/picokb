import time
from math import log, floor

from machine import Pin

row_wait_time = 0.00050
debounce_no = 5

class PicoKB():
    def __init__(self, layout, row_pins, col_pins):
        self.layout = layout
        self.old_mat = []
        self.cur_mat = []
        self.rows = len(row_pins)
        self.cols = len(col_pins)

        self.row_pins = [Pin(id, Pin.OUT, value=1) for id in row_pins]
        self.col_pins = [Pin(id, Pin.IN, pull=Pin.PULL_UP) for id in col_pins]


        # initialize matrices
        for _ in layout:
            self.old_mat.append(0)

        self.cur_mat = self.old_mat.copy()
        self.EMPTY_MAT = self.old_mat.copy()

    def run(self):
        while(True):
            self.old_mat = self.cur_mat
            self.cur_mat = self._scan_matrix()

            # (naive) debounce
            if self._handle_change():
                time.sleep(0.001 * debounce_no)

    def _scan_matrix(self):
        new_mat = self.EMPTY_MAT.copy()

        for row in range(self.rows):
            self.row_pins[row].off()
            time.sleep(row_wait_time)
            for col in range(self.cols):
                pressed = not self.col_pins[col].value()
                if pressed:
                    new_mat[row] = new_mat[row] | 1 << col

            self.row_pins[row].on()

        return new_mat

    def _handle_change(self):
        change = False

        for i in range(self.rows):
            change_mask = self.old_mat[i] ^ self.cur_mat[i]
            while change_mask > 0:
                j = floor(log(change_mask, 2))
                change_mask = change_mask - (1 << j)
                self._handle_key(i, j)
                change = True

        return change

    def _handle_key(self, row, column):
        print(self.layout[row][column])

if __name__ == '__main__':
    kb = PicoKB(
        [list(range(14)) for _ in range(5)],
        [0, 1, 2, 3, 4],
        [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    kb.run()