"""
Base classes for the restaurant management system
"""
from abc import ABC, abstractmethod
from typing import List, Optional


class Subject(ABC):
    """Abstract Subject class for Observer Pattern"""
    def __init__(self):
        self._observers: List['Observer'] = []
    
    def attach(self, observer: 'Observer') -> None:
        """Attach an observer to the subject"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Observer {type(observer).__name__} attached")
    
    def detach(self, observer: 'Observer') -> None:
        """Detach an observer from the subject"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Observer {type(observer).__name__} detached")
    
    def notify(self, event_type: str, data: Optional[dict] = None) -> None:
        """Notify all observers about an event"""
        if data is None:
            data = {}
        for observer in self._observers:
            observer.update(event_type, data)


class Observer(ABC):
    """Abstract Observer class for Observer Pattern"""
    @abstractmethod
    def update(self, event_type: str, data: dict) -> None:
        """Update method called by Subject when an event occurs"""
        pass
