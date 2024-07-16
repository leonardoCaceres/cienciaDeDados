from typing import Type
from Report.reportInterface import ReportInterface
from Graphic.graphicsInterface import GraphicsInterface

class Generate:

    def generateGraphic(self, graphic: Type[GraphicsInterface]) -> None:
        graphic.createGraphics()
    
    def generateReport(self, report: Type[ReportInterface]) -> None:
        report.createReport()