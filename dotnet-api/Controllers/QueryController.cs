using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/query")]
public class QueryController : ControllerBase
{
    private readonly PythonService _pythonService;

    public QueryController(PythonService pythonService)
    {
        _pythonService = pythonService;
    }

    [HttpPost]
    public async Task<IActionResult> Query([FromBody] QueryRequest request)
    {
        var result = await _pythonService.QueryAsync(request);
        return Ok(result);
    }
}