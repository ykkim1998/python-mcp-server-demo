from mcp.server.fastmcp import FastMCP
from zoneinfo import ZoneInfo
from datetime import datetime

# 'America/New_York'와 같이 표준 시간대 이름을 사용합니다.
timezone_name = 'Asia/Seoul'
timezone_name = 'America/New_York'  # 예시로 뉴욕의 시간대를 사용합니다.
timezone = ZoneInfo(timezone_name)

# 현재 시간을 특정 타임존으로 변환
current_time = datetime.now(timezone)

# 원하는 형식으로 시간을 포맷팅
formatted_time = current_time.strftime('%Y년 %m월 %d일 %H시 %M분 %S초')

print(f"Current time in {timezone_name}: {formatted_time}")

# FastMCP 서버를 생성합니다.
mcp = FastMCP("Timezone Server")

'''
​resources/list 요청 시 빈 배열이 반환되는 문제는 MCP 서버에서 동적 리소스만 정의되어 있을 때 발생할 수 있습니다. 현재 코드에서는 @mcp.resource("timezones://{timezone_name}") 데코레이터를 사용하여 동적 리소스를 등록하고 있습니다. 이러한 동적 리소스는 특정 URI 패턴에 따라 동작하지만, resources/list와 같은 메서드로는 자동으로 나열되지 않습니다.​
이 문제는 MCP Inspector에서 동적 리소스를 인식하지 못하는 현재의 제한사항 때문입니다. GitHub 이슈에서도 이와 관련된 논의가 있으며, 동적 리소스가 resources/list에 포함되지 않는다는 보고가 있습니다 .​
'''
# 동적 리소스: 사용자가 입력한 시간대에 대한 현재 시간
@mcp.resource("timezones://{timezone_name}")
def get_timezone(timezone_name: str) -> str:
    """Timezone data"""
    return f"Timezone: {timezone_name}, Current time: {datetime.now(ZoneInfo(timezone_name)).strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}"

# 정적 리소스: Asia/Seoul 시간대
@mcp.resource("timezones://Asia/Seoul")
def get_seoul_time() -> str:
    """Asia/Seoul 시간대의 현재 시간"""
    return datetime.now(ZoneInfo("Asia/Seoul")).strftime('%Y년 %m월 %d일 %H시 %M분 %S초')

# 정적 리소스: America/New_York 시간대
@mcp.resource("timezones://America/New_York")
def get_newyork_time() -> str:
    """America/New_York 시간대의 현재 시간"""
    return datetime.now(ZoneInfo("America/New_York")).strftime('%Y년 %m월 %d일 %H시 %M분 %S초')

# Tool: Get current time in a specific timezone
@mcp.tool()
def get_time_in_timezone(timezone_name: str) -> str:
    """Get current time in a specific timezone"""
    return f"Current time in {timezone_name}: {datetime.now(ZoneInfo(timezone_name)).strftime('%Y년 %m월 %d일 %H시 %M분 %S초')}"

# Prompt: Ask for a timezone name
@mcp.prompt()
def ask_for_timezone() -> str:
    """Ask for a timezone name"""
    return "Please enter a timezone name."

# Run the server
if __name__ == "__main__":
    mcp.run()