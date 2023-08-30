from dataclasses import dataclass

from localsearch.__spi__.model import RankedDocument, StructuredSource


@dataclass
class ContextSpan:
    source_id: str
    source_part: int | None
    start_idx: int
    end_idx: int


def filter_common_context(
        results: list[RankedDocument],
        chars_before: int,
        chars_after: int,
        source_id_field: str = "source_id",
        source_part_field: str = "source_part",
        text_start_idx_field: str = "text_start_idx"
) -> list[RankedDocument]:

    context_spans: list[ContextSpan] = []
    filtered_results = []
    for res in results:
        source_id = res.document.fields[source_id_field]
        source_part = res.document.fields.get(source_part_field)
        text_start_idx = res.document.fields[text_start_idx_field]
        in_existing_context = False
        for cs in context_spans:
            if (
                source_id == cs.source_id
                and source_part == source_part
                and cs.start_idx < text_start_idx < cs.end_idx
            ):
                in_existing_context = True
                break

        if not in_existing_context:
            context_spans.append(
                ContextSpan(source_id, source_part, text_start_idx-chars_before, text_start_idx+chars_after)
            )
            filtered_results.append(res)

    return filtered_results


def get_full_context(
        result: RankedDocument,
        source: StructuredSource,
        chars_before: int,
        chars_after: int,
        source_id_field: str = "source_id",
        source_part_field: str = "source_part",
        text_start_idx_field: str = "text_start_idx",
        doc_title_prefix: str = "Document title:",
        section_title_prefix: str = "Section_title:"
) -> str:

    source_part: int = result.document.fields[source_part_field]
    text_start_idx: int = result.document.fields[text_start_idx_field]

    part = source.parts[source_part]
    start_idx = max(0, text_start_idx-chars_before)
    end_idx = text_start_idx+chars_after
    text = part.text[start_idx: end_idx]
    title = ""
    title += f"{doc_title_prefix} {source.title}.\n\n" if source.title.strip() else ""
    title += f"{section_title_prefix} {part.title}.\n\n" if part.title.strip() else ""

    return f"{title}{text}"
