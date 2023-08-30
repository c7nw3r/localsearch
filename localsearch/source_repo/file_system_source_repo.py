from dataclasses import asdict
from pathlib import Path

from localsearch.__spi__.model import Source, SourcePart, StructuredSource, TextSource
from localsearch.__util__.io_utils import read_json, write_json
from localsearch.source_repo.source_repo import SourceRepo


class FileSystemSourceRepo(SourceRepo):

    def __init__(self, source_dir: str) -> None:
        self._source_dir = source_dir

    def add(self, source: Source) -> None:
        write_json(Path(self._source_dir) / f"{source.id}.json", asdict(source))

    def get(self, id: str) -> Source:
        source = read_json(Path(self._source_dir) / f"{id}.json")
        type = source.get("type")

        if type == "TextSource":
            return TextSource(**source)
        elif type == "StructuredSource":
            parts = [SourcePart(**part) for part in source.pop("parts")]
            return StructuredSource(**source, parts=parts)

        return Source(**source)
