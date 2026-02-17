import json
import re
from pathlib import Path

ALLOWED_TOP_LEVEL_KEYS = {
    'project',
    'total_papers',
    'completed',
    'in_progress',
    'not_started',
    'published',
    'current_batch',
    'current_paper',
    'papers',
}

EXPECTED_BATCH = {
    'P1a': 1, 'P1b': 1, 'P1c': 1, 'P2A': 1,
    'P-DC': 2, 'CKG-1': 2, 'SC-1': 2, 'BAK-1': 2, 'HZF-1': 2,
    'CKG-2': 3, 'YBK-1': 3, 'P2B': 3, 'P2C': 3, 'WHM-1': 3, 'HZF-2': 3,
    'CKG-3': 4, 'SC-2': 4, 'P2D': 4, 'P2E': 4, 'HZF-3': 4, 'WHM-2': 4,
}

PUBLISHED = {'Lei2025a', 'Lei2025b', 'Lei2025c', 'Lei2025d'}
STATUS_ONLY_PAPERS = PUBLISHED
COMPLETED_PREFIXES = ('accepted_', 'existing_draft_')
COMPLETED_STATUS_RE = re.compile(r'^(accepted_v\d+(_iter\d+(_completed)?)?|existing_draft_v\d+)$')


def _load_progress() -> dict:
    return json.loads(Path('progress.json').read_text(encoding='utf-8'))


def _status_bucket(status: str) -> str:
    if status == 'published':
        return 'published'
    if status == 'not_started':
        return 'not_started'
    if status.startswith('in_progress'):
        return 'in_progress'
    if status.startswith(COMPLETED_PREFIXES):
        return 'completed'
    raise AssertionError(f'unsupported status value: {status}')


def test_progress_top_level_schema_and_counts_are_consistent():
    progress = _load_progress()
    papers = progress['papers']

    assert set(progress) == ALLOWED_TOP_LEVEL_KEYS
    assert isinstance(progress['papers'], dict)

    for key in ('total_papers', 'completed', 'in_progress', 'not_started', 'published', 'current_batch'):
        assert isinstance(progress[key], int), f'{key} must be int'
        assert progress[key] >= 0, f'{key} must be non-negative'

    buckets = {'published': 0, 'in_progress': 0, 'not_started': 0, 'completed': 0}
    for payload in papers.values():
        status = payload.get('status')
        assert isinstance(status, str) and status, f'invalid status payload: {payload}'
        buckets[_status_bucket(status)] += 1

    assert progress['total_papers'] == len(papers)
    assert progress['total_papers'] == (
        progress['completed'] + progress['published'] + progress['in_progress'] + progress['not_started']
    )
    assert progress['completed'] == buckets['completed']
    assert progress['published'] == buckets['published']
    assert progress['in_progress'] == buckets['in_progress']
    assert progress['not_started'] == buckets['not_started']


def test_progress_paper_payload_schema_and_batch_mapping():
    progress = _load_progress()
    papers = progress['papers']

    assert set(papers) == set(EXPECTED_BATCH) | STATUS_ONLY_PAPERS

    for paper_id, payload in papers.items():
        assert isinstance(payload, dict), f'{paper_id} payload must be object'
        assert 'status' in payload, f'{paper_id} missing status'

        if paper_id in STATUS_ONLY_PAPERS:
            assert payload == {'status': 'published'}, f'{paper_id} should be status-only published entry'
        else:
            assert payload.get('batch') == EXPECTED_BATCH[paper_id], (
                f"{paper_id} batch mismatch: expected {EXPECTED_BATCH[paper_id]}, got {payload.get('batch')}"
            )
            assert isinstance(payload['batch'], int), f"{paper_id} batch must be int"
            assert set(payload) == {'status', 'batch'}, f'{paper_id} has unexpected fields: {set(payload)}'


def test_current_pointer_is_valid_and_consistent_with_batch():
    progress = _load_progress()
    papers = progress['papers']

    current_paper = progress['current_paper']
    assert isinstance(current_paper, str) and current_paper, 'current_paper must be non-empty string'
    assert 1 <= progress['current_batch'] <= 4, 'current_batch must be in [1,4]'
    assert current_paper in papers

    current_payload = papers[current_paper]
    assert 'batch' in current_payload, 'current_paper must refer to an active paper with batch metadata'
    assert progress['current_batch'] == current_payload['batch']


def test_completed_status_strings_follow_expected_patterns():
    progress = _load_progress()
    for paper_id, payload in progress['papers'].items():
        if paper_id in STATUS_ONLY_PAPERS:
            continue
        status = payload['status']
        bucket = _status_bucket(status)
        if bucket == 'completed':
            assert COMPLETED_STATUS_RE.match(status), f'{paper_id} has malformed completed status: {status}'
