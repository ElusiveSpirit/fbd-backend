from app.guard.playbooks import run_close_public_playbook, run_open_public_playbook
from app.guard.repositories import GuardRepository


def get_public_access_status(guard_repo: GuardRepository) -> bool:
    return guard_repo.get_opened()


def open_public_access(guard_repo: GuardRepository) -> None:
    run_open_public_playbook()
    guard_repo.set_opened(opened=True)


def close_public_access(guard_repo: GuardRepository) -> None:
    run_close_public_playbook()
    guard_repo.set_opened(opened=False)
