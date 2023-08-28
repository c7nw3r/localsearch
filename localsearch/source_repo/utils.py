from dataclasses import dataclass

from localsearch.__spi__.model import RankedDocument


@dataclass
class ContextSpan:
    doc_id: str
    start_idx: int
    end_idx: int


def filter_common_context(
        results: list[RankedDocument],
        chars_before: int,
        chars_after: int,
        source_id_field: str,
        text_start_idx_field: str
) -> list[RankedDocument]:

    context_spans: list[ContextSpan] = []
    filtered_results = []
    for res in results:
        doc_id = res.document.fields[source_id_field]
        text_start_idx = res.document.fields[text_start_idx_field]
        in_existing_context = False
        for cs in context_spans:
            if (
                doc_id == cs.doc_id
                and cs.start_idx < text_start_idx < cs.end_idx
            ):
                in_existing_context = True
                break

        if not in_existing_context:
            context_spans.append(
                ContextSpan(doc_id, text_start_idx-chars_before, text_start_idx+chars_after)
            )
            filtered_results.append(res)

    return filtered_results
