from mcp.server import MCPServer
from mcp.types import ToolAnnotations
from typing import Annotated
from pydantic import Field, BaseModel
import sqlite3

mcp = MCPServer(
    name="rentals_api_mcp",
    title="rentals_api_mcp",
    version="1.0.0",
    instructions=(
        "On-call assistant for the Magic stones Rentals API, Start with service_overview, then narrow down"
        "with compare_windows, latency_trend, error_breakdown, search_logs, rencent_deploys and"
        "errors_by_version, Quote every number with its time window, Ask the person before rollback deploy"
    )
)

class RouteStatus(BaseModel):
    route: str
    requests: int
    error_rate_pct: float
    p95_ms: float

class Overview(BaseModel):
    as_of: str
    window_minutes: int
    version: str
    requests_per_min: float
    error_rate_pct: float
    p50_ms: float
    p95_ms: float
    slo_breaches: list[str]
    data_warning: str | None
    routes: list[RouteStatus]


SLO = {"p95_ms": 300, "errors_rate_pct": 1.0 }
READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)
Minutes = Annotated[int, Field(ge=1, le=120)]





from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "telemetry.db"


@mcp.tool(annotations=READ_ONLY)
def service_overview(minutes: Minutes = 5) -> Overview:
    """Is it broken, The Service's health right now:  traffic, error rate, latency
    SLO breaches and worst routes first.
    Start every investigation
    """
    pass


@mcp.resource(uri="mcp://rentals/version")
def get_version() -> str | None:
    """This resource will return the deployed version

    Returns:
        str | None: str if deployed None in all other cases.
    """
    query = "SELECT version FROM deploys ORDER BY ts DESC LIMIT 1"
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(query).fetchone()

    return str(row[0]) if row else None


@mcp.resource(uri="mcp://rentals/allversions")
def get_all_versions_deployed_so_far() -> str | None:
    """This resource will return All the versions deployed so far in a 
    comma seperated style
    """
    query = """
        SELECT DISTINCT version
        FROM deploys
        ORDER BY ts DESC
    """

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(query).fetchall()

    return ", ".join(str(row[0]) for row in rows)


def when_was_latest_version_deployed():
    pass


def number_of_requests_between(start, end):
    pass




@mcp.tool()
def healthz():
    pass


if __name__ == "__main__":
    #mcp.run(transport="streamable-http", host="0.0.0.0", port=9090)
    mcp.run(transport="stdio")