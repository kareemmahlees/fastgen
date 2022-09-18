from abc import ABC, abstractmethod


class Manager(ABC):
    @abstractmethod
    def nav_to_dir(self):
        ...

    @abstractmethod
    def create_project(self):
        ...

    @abstractmethod
    def init_env(self):
        ...
