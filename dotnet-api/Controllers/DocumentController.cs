using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/document")]
public class DocumentController : ControllerBase
{
    private readonly PythonService _pythonService;

    public DocumentController(PythonService pythonService)
    {
        _pythonService = pythonService;
    }

    [HttpPost("upload")]
    public async Task<IActionResult> Upload(IFormFile file)
    {
        if (file == null || file.Length == 0)
            return BadRequest("Invalid file");

        var result = await _pythonService.UploadDocumentAsync(file);

        return Ok(result);
    }
}