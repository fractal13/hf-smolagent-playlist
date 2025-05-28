# Information sources are key

- DuckDuckGo has an unpublished anonymous rate limiting algorithm.
  [source](https://duckduckgo.com/duckduckgo-help-pages/duckai/usage-limits)
- Google has API rate limits. [Need more details]()
- Tools for identifying domain useful sites should be handy.
- Tools for scraping and crawling specific sites should be handy.
- Tools for generically finding good sites and crawling them should be handy.
- Can a tool be made to find and use search bars on lots of sites?
- List of [huggingface tools](https://huggingface.co/docs/smolagents/v1.17.0/en/reference/tools)

- Large services should be building their own API, or even better, MCP server for access.


# Tools (HuggingFace)

- Best practices with tools
  * use clear name for function
  * use type hints for arguments and returns (inputs and outputs)
  * use descriptive docstring, with Args: section
- @tool decorator on functions

    @tool
    def my_music_tool(band: str, decade: int) -> List[str]:
        """Find songs for the given band and decade.
        Args:
            band: The name of the band. If empty, search for bands.
            decade: The decade of the songs (1980, 2010, etc.). If empty, search for all decades.
        Returns:
            A list of strings; each string is a song name.
        """
        
        # code here
        return here

- Subclass of Tool

    from smoltools import Tool
    class MyMusicTool(Tool):
        name = "my_music_tool"
        description = """
        Find songs for the given band and decade.
        Args:
            band: The name of the band. If empty, search for bands.
            decade: The decade of the songs (1980, 2010, etc.). If empty, search for all decades.
        Returns:
            A list of strings; each string is a song name.
        """
        inputs = {
            "band": { "type": "str", "description": "The name of the band. If empty, search for bands." },
            "decade": { "type": "int", "description": "The decade of the songs (1980, 2010, etc.). If empty, search for all decades." }
        }
        output_type = List[str]

        def forward(self, band: str, decade: int) -> List[str]:
            # code here
            return here

