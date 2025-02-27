import time
import sys
from typing import overload


class ProgressIter:
    """
    小侠专用进度条，需要和pipeline配合使用，可以用于包裹所有支持迭代的对象，一般用于最外层循环。
    """
    def __init__(self, iterable=None, total=None, print_end="\r", min_interval: float =0.1):
        self.last_time = None
        self.iterable = iterable
        self.print_end = print_end
        self.progress = 0
        self.min_interval = min_interval  # 最小打印间隔
        self.total = total if total else (len(iterable) if hasattr(iterable, '__len__') else total)
        self.last_print_time = time.time()  # 上次打印的时间
        self.time_series = [time.time()]

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def report_progress(self, increment):
        self.progress = min(self.total, self.progress + increment)
        self.__print_progress(self.progress)

    def __iter__(self):
        if self.iterable is None:
            raise ValueError("Iterable item is empty")
        for i, item in enumerate(self.iterable):
            yield item
            current_time = time.time()
            if current_time - self.last_print_time >= self.min_interval or i + 1 == self.total:
                self.progress += 1
                self.__print_progress(self.progress)
                self.last_print_time = current_time

    def __print_progress(self, iteration):
        # Current time and elapsed time

        self.time_series.append(time.time())
        self.time_series = self.time_series[-5:]

        if self.total is not None:
            percent = ("{0:.1f}").format(100 * (iteration / float(self.total)))

            # Calculate remaining time
            avg_step_time = (self.time_series[-1] - self.time_series[0]) / (len(self.time_series) - 1)
            remaining_steps = self.total - iteration - 1
            remaining_time = max(avg_step_time * (remaining_steps + 1), 0)

            # Print progress
            print(f"{{percent}}{percent}")
            print(f"{{avg_step_time}}{avg_step_time:.2f}")
            print(f"{{remaining_time}}{remaining_time:.2f}")
        else:
            print(f'\rIteration {iteration} ', end=self.print_end)

        # flush stdout
        sys.stdout.flush()

        if iteration == self.total:
            time.sleep(0.5)


# 示例用法
if __name__ == "__main__":
    import time

    items = list(range(100))
    for item in ProgressIter(items, min_interval=0.01):
        time.sleep(0.1)  # 模拟工作负载
