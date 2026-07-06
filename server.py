from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


mcp = FastMCP(
    name="ReceiptMCP",
    instructions="ReceiptMCP(영수증MCP) provides tools to analyze receipt text and format spending records.",
    host="0.0.0.0",
    port=8000,
    stateless_http=True,
)


@mcp.tool(
    name="health_check",
    description="Checks whether ReceiptMCP(영수증MCP) is running correctly.",
    annotations=ToolAnnotations(
        title="Health Check",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def health_check() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "ReceiptMCP(영수증MCP)",
    }


@mcp.tool(
    name="analyze_receipt_text",
    description="Extracts simple receipt information from plain text for ReceiptMCP(영수증MCP).",
    annotations=ToolAnnotations(
        title="Analyze Receipt Text",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def analyze_receipt_text(receipt_text: str) -> dict[str, Any]:
    lines = [line.strip() for line in receipt_text.splitlines() if line.strip()]

    return {
        "store_name": lines[0] if lines else None,
        "raw_text": receipt_text,
        "line_count": len(lines),
        "items": [
            {
                "line_no": index + 1,
                "text": line,
            }
            for index, line in enumerate(lines)
        ],
        "message": "Receipt text was parsed into simple structured rows.",
    }


@mcp.tool(
    name="format_receipt_table",
    description="Formats receipt items as a compact markdown table for ReceiptMCP(영수증MCP).",
    annotations=ToolAnnotations(
        title="Format Receipt Table",
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=False,
    ),
)
def format_receipt_table(receipt_text: str) -> str:
    lines = [line.strip() for line in receipt_text.splitlines() if line.strip()]

    if not lines:
        return "No receipt text was provided."

    table_lines = [
        "| No | Receipt line |",
        "|---:|---|",
    ]

    for index, line in enumerate(lines, start=1):
        safe_line = line.replace("|", "\\|")
        table_lines.append(f"| {index} | {safe_line} |")

    return "\n".join(table_lines)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
