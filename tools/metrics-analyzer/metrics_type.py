import abc


class MetricsType(abc.ABC):
    window_size = ''
    window_slide = ''
    threshold = ''

    @abc.abstractmethod
    def process_stream(self, df):
        pass