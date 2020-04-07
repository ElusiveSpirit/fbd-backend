from app.core.repositories import EntityDoesNotExist
from app.severs.models import ServerStatus
from app.severs.playbooks import run_clean_playbook
from app.severs.repositories import ServerIsBusy, ServersRepository


async def check_server_exists(servers_repo: ServersRepository, slug: str) -> bool:
    try:
        servers_repo.get_server_by_slug(slug=slug)
    except EntityDoesNotExist:
        return False

    return True


def clean_server(servers_repo: ServersRepository, server_slug: str) -> None:
    """Run's clean server ansible playbook"""
    server = servers_repo.get_server_by_slug(server_slug)
    if server.is_busy:
        raise ServerIsBusy
    servers_repo.update_server(server=server, status=ServerStatus.pending)

    run_clean_playbook(server.slug)

    servers_repo.delete_server(server=server)
