from typing import List
from python_gedcom_2.element.element import Element
from python_gedcom_2.element.individual import IndividualElement
from python_gedcom_2.element.family import FamilyElement
from python_gedcom_2.element.event_detail import EventDetail
from python_gedcom_2.element.date import DateElement
from python_gedcom_2.parser import Parser
from typing import TypeVar
import python_gedcom_2.tags as tags

T = TypeVar("T", bound="Individual")

class Event:
    """Klasse die ein Event in Gedcom darstellt, also ein Tag mit einem Datum und oder Ort
    """
    def __init__(self, event: EventDetail):
        self.__event = event
        
    def get_raw_event(self) -> EventDetail:
        return self.__event
    
    def has_date(self) -> bool:
        return self.__event._is_tag_present(tags.GEDCOM_TAG_DATA)

    def get_date(self) -> DateElement | None:
        """Gibt ein DateElement oder None zurück falls das Event ein Date besitzt

        Returns:
            DateElement | None: Das Date Tag
        """
        if not self.has_date():
            return None
        
        for child in self.__event.get_child_elements():
            if isinstance(child, DateElement):
                return child
        

class Family:
    def __init__(self, element: FamilyElement):
        self.__element = element
        self.__events: List[Event] = []
        self.__husband_pointer: str = ""
        self.__wife_pointer: str = ""
        self.__husband: Individual | None = None
        self.__wife: Individual | None = None
        child_elements: List[Element] = self.__element.get_child_elements()
        
        for tag in child_elements:
            if isinstance(tag, EventDetail):
                self.__events.append(Event(tag))
                
            if tag.get_tag() == tags.GEDCOM_TAG_HUSBAND:
                self.__husband_pointer = tag.get_value()
            
            if tag.get_tag() == tags.GEDCOM_TAG_WIFE:
                self.__wife_pointer = tag.get_value()

    def get_husband(self, parser) -> T | None:
        if self.__husband:
            return self.__husband
        
        if self.__husband_pointer == "":
            return None
        self.__husband = Individual.from_pointer(parser, self.__husband_pointer)
        return self.__husband
    
    def get_wife(self, parser) -> T | None:
        if self.__wife:
            return self.__wife
        
        if self.__wife_pointer == "":
            return None

        self.__wife = Individual.from_pointer(parser, self.__wife_pointer)
        return self.__wife
    
    def get_raw_element(self) -> FamilyElement:
        return self.__element


class Individual:
    """Klasse aller einzelner Menschen
    """
    def __init__(self, element: IndividualElement):
        self.__element = element 
    
    def get_raw_element(self) -> IndividualElement:
        return self.__element

    @classmethod
    def from_pointer(cls: T, parser: Parser, pointer: str) -> T | None:
        """Erstellt ein Individual aus einem Pointer `@I0@`. 

        Args:
            parser (Parser): Eine Instanz des des Parser
            pointer (str): Den Pointer String
        """
        if not "I" in pointer:
            return None
        
        element = parser.get_element_by_pointer(pointer)
        if not isinstance(element, IndividualElement):
            return None
        
        return cls(element)    

    @staticmethod
    def is_individual(element: Element) -> bool:
        return isinstance(element, IndividualElement)
