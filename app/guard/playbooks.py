import os


def run_clean_playbook(slug: str) -> None:
    raise NotImplementedError


def run_open_public_playbook() -> None:
    os.system(  # noqa: S605, S607
        "cd /app/ansible && /usr/local/bin/ansible-playbook --private-key=/.id_rsa open_public.yml"
    )


def run_close_public_playbook() -> None:
    os.system(  # noqa: S605, S607
        "cd /app/ansible && /usr/local/bin/ansible-playbook --private-key=/.id_rsa close_public.yml"
    )
