from abc import ABCMeta, abstractmethod

class layers():
    @abstractmethod
    def __init__(self):
        pass
    
    ### defines whether a feature meets the condition of the current layer
    @abstractmethod
    def condition(self, feature):
        pass
    
    ### update the feature and make sure the necessary values
    @abstractmethod
    def update_feature(self, feature):
        pass